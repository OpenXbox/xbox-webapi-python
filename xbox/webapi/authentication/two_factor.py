"""
Two Factor Authentication extension, called within AuthenticationManager if needed
"""
import struct
import logging
import time

from xbox.webapi.common.enum import IntEnum
from xbox.webapi.common.exceptions import AuthenticationException

log = logging.getLogger('authentication-2factor')


class TwoFactorAuthentication(object):
    def __init__(self, session):
        """
        Handle Windows Live Two-Factor-Authentication (2FA).

        It needs a parsed `serverData`-javascript-object to pull
        it's info from, it is obtained by a previous Windows-Live-Authentication Request - also the respective
        email-address for the Windows Live Account to authenticate is needed.

        Supported Methods:
        * Email
        * Mobile Phone number (SMS)
        * MS Authenticator (Code)
        * MS Authenticator v2 (Push Message)

        Args:
            session (requests.session): Instance of :class:`requests.session`
        """
        self.session = session

    @staticmethod
    def verify_authenticator_v2_gif(response):
        """
        Verify the AuthSessionState GIF-image, returned when polling the `Microsoft Authenticator v2`.

        At first, check if provided bytes really are a GIF image, then check image-dimensions to get Session State.

        Args:
            response (requests.Response): The response holding the GIF image, describing current Authentication Session State.
                              Possible image dimensions:
                                - 2px x 2px - Rejected Authorization
                                - 1px x 1px - Pending Authorization (keep polling)
                                - 1px x 2px - Approved Authorization

        Returns:
            AuthSessionState: The current Authentication State. AuthSessionState.ERROR if provided bytes are not a GIF
            or the image-dimensions are unknown.

        """
        GIF_HEADER_SIZE = 6
        GIF_HEADER = b'GIF87a'
        MIN_GIF_SIZE = 35

        gif = response.content
        if len(gif) < MIN_GIF_SIZE:
            log.error('Got GIF image smaller than expected! Got %d instead of min. %d' % (len(gif), MIN_GIF_SIZE))
            return AuthSessionState.ERROR
        elif gif[:GIF_HEADER_SIZE] != GIF_HEADER:
            log.error('Returned image does not look like GIF -> Header: %s' % gif[:GIF_HEADER_SIZE])
            return AuthSessionState.ERROR

        width, height = struct.unpack('<HH', gif[GIF_HEADER_SIZE:10])
        if width == 1 and height == 2:
            return AuthSessionState.APPROVED
        elif width == 1 and height == 1:
            return AuthSessionState.PENDING
        elif width == 2 and height == 2:
            return AuthSessionState.REJECTED
        else:
            log.warning('Unknown GIF dimensions! W: {}, H: {}'.format(width, height))

        return AuthSessionState.ERROR

    def request_otc(self, email, flowtoken, auth_type, proof, auth_data):
        """
        Request OTC (One-Time-Code) if 2FA via Email, Mobile phone or MS Authenticator v2 is desired.

        Args:
            email (str): Email Address of the Windows Live Account
            flowtoken (str): Flowtoken, obtained from `serverData` (Windows Live Auth Request)
            auth_type (TwoFactorAuthMethods): Member of :class:`TwoFactorAuthMethods`
            proof (str): Proof Verification, used by mobile phone and email-method, for MS Authenticator provide `None`
            auth_data (str): Authentication data for this provided, specific authorization method

        Raises:
            AuthenticationException: If requested 2FA Authentication Type is unsupported

        Returns:
            requests.Response: Instance of :class:`requests.Response`
        """
        get_onetime_code_url = 'https://login.live.com/pp1600/GetOneTimeCode.srf'

        if TwoFactorAuthMethods.Email == auth_type:
            channel = 'Email'
            post_field = 'AltEmailE'
        elif TwoFactorAuthMethods.SMS == auth_type:
            channel = 'SMS'
            post_field = 'MobileNumE'
        elif TwoFactorAuthMethods.Voice == auth_type:
            channel = 'Voice'
            post_field = 'MobileNumE'
        elif TwoFactorAuthMethods.TOTPAuthenticatorV2 == auth_type:
            channel = 'PushNotifications'
            post_field = 'SAPId'
        else:
            raise AuthenticationException(
                'Unsupported TwoFactor Auth-Type: %s' % TwoFactorAuthentication(auth_type)
            )

        post_data = {
            'login': email,
            'flowtoken': flowtoken,
            'purpose': 'eOTT_OneTimePassword',
            'UIMode': '11',
            'channel': channel,
            post_field: auth_data,
        }

        if proof:
            post_data.update(dict(ProofConfirmation=proof))

        return self.session.post(get_onetime_code_url, data=post_data, allow_redirects=False)

    def finish_auth(self, email, flowtoken, post_url, auth_type,
                    auth_data=None, otc=None, slk=None, proof_confirmation=None):
        """
        Finish the Two-Factor-Authentication. If it succeeds we are provided with Access and Refresh-Token.

        Args:
            email (str): Email Address of the Windows Live Account
            flowtoken (str): Flowtoken, obtained from `serverData` (Windows Live Auth Request)
            post_url (str): Post URL, obtained from `serverData` (Windows Live Auth Request)
            auth_type (TwoFactorAuthMethods): Member of :class:`TwoFactorAuthMethods`
            auth_data (str): Authentication data for this provided, specific authorization method
            otc (str): One-Time-Code, required for every method except MS Authenticator v2
            slk (str): Session-Lookup-Key, only needed for auth-method MS Authenticator v2
            proof_confirmation (str): Confirmation of Email or mobile phone number, if that method was chosen

        Returns:
            requests.Response: Instance of :class:`requests.Response`
        """
        if TwoFactorAuthMethods.SMS == auth_type or \
           TwoFactorAuthMethods.Voice == auth_type or \
           TwoFactorAuthMethods.Email == auth_type:
            post_type = '18'
            general_verify = False
        elif TwoFactorAuthMethods.TOTPAuthenticator == auth_type:
            post_type = '19'
            general_verify = False
        elif TwoFactorAuthMethods.TOTPAuthenticatorV2 == auth_type:
            post_type = '22'
            general_verify = None
        else:
            raise AuthenticationException('Unhandled case for submitting OTC')

        post_data = {
            'login': email,
            'PPFT': flowtoken,
            'SentProofIDE': auth_data,
            'sacxt': '1',
            'saav': '0',
            'GeneralVerify': general_verify,
            'type': post_type,
            'purpose': 'eOTT_OneTimePassword',
            'i18': '__DefaultSAStrings|1,__DefaultSA_Core|1,__DefaultSA_Wizard|1'
        }

        if otc:
            post_data.update(dict(otc=otc))
        if slk:
            post_data.update(dict(slk=slk))
        if proof_confirmation:
            post_data.update(dict(ProofConfirmation=proof_confirmation))

        return self.session.post(post_url, data=post_data, allow_redirects=False)

    def poll_session_state(self, polling_url, slk):
        """
        Poll MS Authenticator v2 SessionState.

        Polling happens for maximum of 120 seconds if Authorization is not approved by the Authenticator App.
        It will return earlier if request gets approved/rejected.

        Args:
            polling_url (str): Polling url, obtained from `serverData` (Windows Live Auth Request)
            slk (str): Session-Lookup-Key

        Returns:
            AuthSessionState: Current Session State
        """
        max_time_seconds = 120.0
        time_now = time.time()
        time_end = time_now + max_time_seconds

        params = dict(slk=slk)
        log.info('Polling Authenticator v2 Verification for {} seconds'.format(max_time_seconds))

        session_state = AuthSessionState.PENDING
        while time_now < time_end:
            gif_resp = self.session.get(polling_url, params=params)
            session_state = self.verify_authenticator_v2_gif(gif_resp)
            time.sleep(1)
            time_now = time.time()
            if session_state != AuthSessionState.PENDING:
                break

        return session_state

    def authenticate(self, server_data):
        """
        Perform chain of Two-Factor-Authentication (2FA) with the Windows Live Server.

        NOTE: This method prompts the user for text-input via stdin!

        Args:
            server_data (dict): Parsed javascript-object `serverData`, obtained from Windows Live Auth Request

        Returns:
            requests.Response: Instance of :class:`requests.Response`. Access / Refresh Tokens are contained in the
            Location-Header!
        """
        email = server_data.get('a')
        polling_url = server_data.get('Ac')  # NOQA
        flowtoken = server_data.get('sFT')
        post_url = server_data.get('urlPost')
        auth_variants = None

        '''
        15/04/2018
        Auth variants node changes from time to time, changing to heuristic detection

        Example node:
        [{
            data:'<some data>', type:1, display:'pyxb-testing@outlook.com', otcEnabled:true, otcSent:false,
            isLost:false, isSleeping:false, isSADef:true, isVoiceDef:false, isVoiceOnly:false, pushEnabled:false
          },
          {
            data:'<some data>', type:3, clearDigits:'69', ctryISO:'DE', display:'*********69', otcEnabled:true,
            otcSent:false, voiceEnabled:true, isLost:false, isSleeping:false, isSADef:false, isVoiceDef:false,
            isVoiceOnly:false, pushEnabled:false
          },
          {
            data:'2342352452523414114', type:14, display:'2342352452523414114', otcEnabled:false, otcSent:false,
            isLost:false, isSleeping:false, isSADef:false, isVoiceDef:false, isVoiceOnly:false, pushEnabled:true
        }]
        '''
        for k, v in server_data.items():
            if isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict) and \
                            'otcEnabled' in v[0] and 'data' in v[0]:
                log.debug('Auth variants list found in serverData at \'{}\' node'.format(k))
                auth_variants = v

        if not auth_variants:
            raise AuthenticationException('No TwoFactor Auth Methods available?! That\'s weird!')

        variants = ['Type: {!s}, Name: {}'.format(
            TwoFactorAuthMethods(variant.get('type', 0)), variant.get('display'))
            for variant in auth_variants
        ]
        prompt = 'Available 2FA methods:\n'
        for num, variant in enumerate(variants):
            prompt += '  Index: {}, {}\n'.format(num, variant)

        prompt += 'Input desired auth method index: '
        index = int(input(prompt))

        if index < 0 or index >= len(auth_variants):
            raise AuthenticationException('Invalid auth-method index chosen!')

        auth_variant = auth_variants[index]
        auth_type = auth_variant.get('type')
        auth_data = auth_variant.get('data')
        auth_display = auth_variant.get('display')
        auth_method = TwoFactorAuthMethods(auth_type)
        log.debug('Using Method: {}'.format(auth_method))

        proof = None
        slk = None
        otc = None

        if TwoFactorAuthMethods.SMS == auth_type or TwoFactorAuthMethods.Voice == auth_type:
            proof = input("Enter last four digits of following phone number '{}': ".format(auth_display))
        elif TwoFactorAuthMethods.Email == auth_type:
            proof = input("Enter the full mail address '{}': ".format(auth_display))

        if TwoFactorAuthMethods.TOTPAuthenticator != auth_type:
            # TOTPAuthenticator V1 works without requesting anything
            response = self.request_otc(email, flowtoken, auth_type, proof, auth_data)
            if response.status_code != 200:
                raise AuthenticationException(
                    "Error requesting OTC, HTTP Code: %i" % response.status_code
                )
            state = response.json()
            log.debug('State from Request OTC: %s' % state.get('State'))

        if TwoFactorAuthMethods.TOTPAuthenticatorV2 == auth_type:
            raise AuthenticationException("TOTP v2 is currently broken")
            """
            slk = response.json().get('SessionLookupKey')
            if not slk:
                raise AuthenticationException('Did not receive SessionLookupKey from Authenticator V2 request!')

            session_state = self.poll_session_state(polling_url, slk)
            if session_state != AuthSessionState.APPROVED:
                raise AuthenticationException('Authentication by Authenticator V2 failed!'
                                              ' State: %s' % AuthSessionState[session_state])

            # Do not send auth_data when finishing TOTPv2 authentication
            auth_data = None
            """
        else:
            otc = input("Input received OTC: ")

        return self.finish_auth(email, flowtoken, post_url, auth_type,
                                auth_data, otc, slk, proof)


class AuthSessionState(IntEnum):
    """
    Enumeration of possible Two-Factor-Authentication Session-States
    """
    ERROR = 0
    REJECTED = 1  # GIF 2x2
    PENDING = 2  # GIF 1x1
    APPROVED = 3  # GIF 1x2


class TwoFactorAuthMethods(IntEnum):
    """
    Two Factor Authentication Methods
    """
    Voice = -3
    Unknown = 0
    Email = 1
    AltEmail = 2
    SMS = 3
    DeviceId = 4
    CSS = 5
    SQSA = 6
    HIP = 8
    Birthday = 9
    TOTPAuthenticator = 10
    RecoveryCode = 11
    StrongTicket = 13
    TOTPAuthenticatorV2 = 14
    UniversalSecondFactor = 15
