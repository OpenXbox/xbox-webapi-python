"""
Two Factor Authentication extension, called within AuthenticationManager if needed
"""
import struct
import logging
import time

from xbox.webapi.common.enum import Enum
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

    def verify_authenticator_v2_gif(self, gif):
        """
        Verify the AuthSessionState GIF-image, returned when polling the `Microsoft Authenticator v2`.

        At first, check if provided bytes really are a GIF image, then check image-dimensions to get Session State.

        Args:
            gif (bytes): The GIF image describing current Authentication Session State.
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

    def request_otc(self, email, server_data, auth_type, proof, auth_data):
        """
        Request OTC (One-Time-Code) if 2FA via Email, Mobile phone or MS Authenticator v2 is desired.

        Args:
            email (str): Email Address of the Windows Live Account
            server_data (dict): Parsed javascript-object `serverData`, obtained from Windows Live Auth Request
            auth_type (TwoFactorAuthMethods): Member of :class:`TwoFactorAuthMethods`
            proof (str): Proof Verification, used by mobile phone and email-method, for MS Authenticator provide `None`
            auth_data (str): Authentication data for this provided, specific authorization method

        Raises:
            AuthenticationException: If requested 2FA Authentication Type is unsupported

        Returns:
            requests.Response: Instance of :class:`requests.Response`
        """
        post_url = 'https://login.live.com/pp1600/GetOneTimeCode.srf'

        channel = ''
        post_field = ''
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
        elif TwoFactorAuthMethods.TOTPAuthenticator == auth_type:
            log.warning('Requesting OTC not necessary for Authenticator v2!')
        else:
            raise AuthenticationException('Unsupported TwoFactor Auth-Type: %d' % auth_type)

        post_data = {
            'login': email,
            'flowtoken': server_data.get('sFT'),
            'purpose': 'eOTT_OneTimePassword',
            'UIMode': '11',
            'channel': channel,
            post_field: auth_data,
        }

        if proof:
            post_data.update(dict(ProofConfirmation=proof))

        return self.session.post(post_url, data=post_data, allow_redirects=False)

    def finish_auth(self, email, server_data, auth_type, auth_data=None, otc=None, slk=None, proof_confirmation=None):
        """
        Finish the Two-Factor-Authentication. If it succeeds we are provided with Access and Refresh-Token.

        Args:
            email (str): Email Address of the Windows Live Account
            server_data (dict): Parsed javascript-object `serverData`, obtained from Windows Live Auth Request
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
            'PPFT': server_data.get('sFT'),
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

        return self.session.post(server_data.get('urlPost'), data=post_data, allow_redirects=False)

    def poll_session_state(self, server_data, slk):
        """
        Poll MS Authenticator v2 SessionState.

        Polling happens for maximum of 120 seconds if Authorization is not approved by the Authenticator App.
        It will return earlier if request gets approved/rejected.

        Args:
            server_data (dict): Parsed javascript-object `serverData`, obtained from Windows Live Auth Request
            slk (str): Session-Lookup-Key

        Returns:
            AuthSessionState: Current Session State
        """
        max_time_seconds = 120.0
        time_now = time.time()
        time_end = time_now + max_time_seconds

        polling_url = server_data.get('Ac')
        params = {'slk': slk}
        log.info('Polling Authenticator v2 Verification for {} seconds'.format(max_time_seconds))

        session_state = AuthSessionState.PENDING
        while time_now < time_end:
            gif = self.session.get(polling_url, params=params).content
            session_state = self.verify_authenticator_v2_gif(gif)
            time.sleep(1)
            time_now = time.time()
            if session_state != AuthSessionState.PENDING:
                break

        return session_state

    def authenticate(self, email, server_data):
        """
        Perform chain of Two-Factor-Authentication (2FA) with the Windows Live Server.

        NOTE: This method prompts the user for text-input via stdin!

        Args:
            email (str): Email Address of the Windows Live Account
            server_data (dict): Parsed javascript-object `serverData`, obtained from Windows Live Auth Request

        Returns:
            requests.Response: Instance of :class:`requests.Response`. Access / Refresh Tokens are contained in the
            Location-Header!
        """
        auth_variants = server_data.get('D', [])
        if not len(auth_variants):
            log.error('No TwoFactor Auth Methods available?! That\'s weird!')
            return

        print('Available 2FA methods:')
        for num, variant in enumerate(auth_variants):
            print('  Index: {}, Type: {}, Name: {}'.format(
                num, TwoFactorAuthMethods[variant.get('type', 0)], variant.get('display'))
            )

        try:
            index = int(input("Input desired auth method index: "))
            auth_type = auth_variants[index].get('type')
            auth_data = auth_variants[index].get('data')
            auth_display = auth_variants[index].get('display')
            auth_method = TwoFactorAuthMethods[auth_type]
            log.debug('Using Method: {}'.format(auth_method))
        except Exception:
            log.error('Invalid auth-method index chosen!')
            return

        proof = None
        slk = None
        otc = None

        if TwoFactorAuthMethods.SMS == auth_type or TwoFactorAuthMethods.Voice == auth_type:
            proof = input("Enter last four digits of following phone number '{}': ".format(auth_display))
        elif TwoFactorAuthMethods.Email == auth_type:
            proof = input("Enter the full mail address '{}': ".format(auth_display))

        if TwoFactorAuthMethods.TOTPAuthenticator != auth_type:
            # TOTPAuthenticator V1 works without requesting anything
            req_response = self.request_otc(email, server_data, auth_type, proof, auth_data)

        if TwoFactorAuthMethods.TOTPAuthenticatorV2 == auth_type:
            slk = req_response.json().get('SessionLookupKey')
            if not slk:
                log.error('Did not receive SessionLookupKey from Authenticator V2 request!')
                return
            session_state = self.poll_session_state(server_data, slk)
            if session_state != AuthSessionState.APPROVED:
                log.error('Request was not authenticated by Authenticator V2 App!')
                return
            # Do not send auth_data when submitting OTC
            auth_data = None
        else:
            otc = int(input("Input received OTC: "))

        return self.finish_auth(email, server_data, auth_type, auth_data, otc, slk, proof)


class AuthSessionState(object):
    """
    Enumeration of possible Two-Factor-Authentication Session-States
    """
    ERROR = 0
    REJECTED = 1  # GIF 2x2
    PENDING = 2  # GIF 1x1
    APPROVED = 3  # GIF 1x2


class TwoFactorAuthMethods(Enum):
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
