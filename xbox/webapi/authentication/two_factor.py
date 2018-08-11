"""
Two Factor Authentication extension, called within AuthenticationManager if needed
"""
import struct
import logging
import time

from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.common.enum import IntEnum
from xbox.webapi.common.exceptions import AuthenticationException

log = logging.getLogger('authentication-2factor')


class TwoFactorAuthentication(object):
    def __init__(self, session, email, server_data):
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
            email (str): Email address
            server_data (dict): Parsed js object from windows live auth request
        """
        self.session = session
        self.server_data = server_data
        self.email = email
        self.flowtoken = server_data.get('sFT')
        self.post_url = server_data.get('urlPost')
        self.session_lookup_key = None
        self._auth_strategies = self.parse_auth_strategies(server_data)

    @property
    def auth_strategies(self):
        """
        Get available authentication strategies

        Returns: list
        """
        return self._auth_strategies

    @staticmethod
    def parse_auth_strategies(server_data):
        """
        Parses the list of supported authentication strategies

        Auth variants position changes from time to time, so instead of accessing a fixed, named field,
        heuristic detection is used

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

        Returns:
            list: List of available auth strategies
        """
        for k, v in server_data.items():
            if isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict) and 'otcEnabled' in v[0] and 'data' in v[0]:
                return v

        raise AuthenticationException('No 2fa auth strategies found!')

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

    def _request_otc(self, auth_type, proof, auth_data):
        """
        Request OTC (One-Time-Code) if 2FA via Email, Mobile phone or MS Authenticator v2 is desired.

        Args:
            auth_type (TwoFactorAuthMethods): Member of :class:`TwoFactorAuthMethods`
            proof (str/NoneType): Proof Verification, used by mobile phone and email-method, for MS Authenticator provide `None`
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
            'login': self.email,
            'flowtoken': self.flowtoken,
            'purpose': 'eOTT_OneTimePassword',
            'UIMode': '11',
            'channel': channel,
            post_field: auth_data,
        }

        if proof:
            post_data.update(dict(ProofConfirmation=proof))

        return self.session.post(get_onetime_code_url, data=post_data, allow_redirects=False)

    def _finish_auth(self, auth_type, auth_data, otc, proof_confirmation):
        """
        Finish the Two-Factor-Authentication. If it succeeds we are provided with Access and Refresh-Token.

        Args:
            auth_type (TwoFactorAuthMethods): Member of :class:`TwoFactorAuthMethods`
            auth_data (str/NoneType): Authentication data for this provided, specific authorization method
            otc (str/NoneType): One-Time-Code, required for every method except MS Authenticator v2
            proof_confirmation (str/NoneType): Confirmation of Email or mobile phone number, if that method was chosen

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
            'login': self.email,
            'PPFT': self.flowtoken,
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
        if self.session_lookup_key:
            post_data.update(dict(slk=self.session_lookup_key))
        if proof_confirmation:
            post_data.update(dict(ProofConfirmation=proof_confirmation))

        return self.session.post(self.post_url, data=post_data, allow_redirects=False)

    def _poll_session_state(self):
        """
        Poll MS Authenticator v2 SessionState.

        Polling happens for maximum of 120 seconds if Authorization is not approved by the Authenticator App.
        It will return earlier if request gets approved/rejected.

        Returns:
            AuthSessionState: Current Session State
        """
        polling_url = None
        for k, v in self.server_data.items():
            if isinstance(v, str) and v.startswith('https://login.live.com/GetSessionState.srf'):
                polling_url = v
        if not polling_url:
            raise AuthenticationException('Cannot find polling URL for TOTPv2 session state')

        max_time_seconds = 120.0
        time_now = time.time()
        time_end = time_now + max_time_seconds

        params = dict(slk=self.session_lookup_key)
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

    def get_method_verification_prompt(self, strategy_index):
        """
        If auth strategy needs verification of method, get userprompt string

        For example:
        * Mobile phone verification (SMS, Voice) needs last 4 digits of mobile #
        * Email verification needs whole address

        Args:
            strategy_index (int): Index of chosen auth strategy

        Returns:
            str: Userinput prompt string if proof is needed, `None` otherwise
        """
        strategy = self.auth_strategies[strategy_index]
        auth_type = strategy.get('type')
        display_string = strategy.get('display')

        if TwoFactorAuthMethods.SMS == auth_type or TwoFactorAuthMethods.Voice == auth_type:
            return "Enter last four digits of following phone number '{}'".format(display_string)
        elif TwoFactorAuthMethods.Email == auth_type:
            return "Enter the full mail address '{}'".format(display_string)

    def check_otc(self, strategy_index, proof):
        """
        Check if OneTimeCode is required. If it's required, request it.

        Args:
            strategy_index (int): Index of chosen auth strategy
            proof (str/NoneType): Verification / proof of chosen auth strategy

        Returns:
            bool: `True` if OTC is required, `False` otherwise
        """
        strategy = self.auth_strategies[strategy_index]
        auth_type = strategy.get('type')
        auth_data = strategy.get('data')
        response = None

        if auth_type != TwoFactorAuthMethods.TOTPAuthenticator:
            '''
            TOTPAuthenticator V1 works without requesting anything (offline OTC generation)
            TOTPAuthenticator V2 needs a cached `Session Lookup Key`, not OTC, we handle it here
            '''
            response = self._request_otc(auth_type, proof, auth_data)
            if response.status_code != 200:
                raise AuthenticationException(
                    "Error requesting OTC, HTTP Code: %i" % response.status_code
                )
            state = response.json()
            log.debug('State from Request OTC: %s' % state.get('State'))

        if auth_type == TwoFactorAuthMethods.TOTPAuthenticatorV2:
            # Smartphone push notification
            self.session_lookup_key = response.json().get('SessionLookupKey')
            return False
        else:
            return True

    def authenticate(self, strategy_index, proof, otc):
        """
        Perform chain of Two-Factor-Authentication (2FA) with the Windows Live Server.

        Args:
            strategy_index (int): Index of chosen auth strategy
            server_data (dict): Parsed javascript-object `serverData`, obtained from Windows Live Auth Request
            otc (str): One Time Code

        Returns:
            tuple: If authentication succeeds, `tuple` of (AccessToken, RefreshToken) is returned
        """
        strategy = self.auth_strategies[strategy_index]
        auth_type = strategy.get('type')
        auth_data = strategy.get('data')
        log.debug('Using Method: {!s}'.format(TwoFactorAuthMethods(auth_type)))

        if TwoFactorAuthMethods.TOTPAuthenticatorV2 == auth_type:
            if not self.session_lookup_key:
                raise AuthenticationException('Did not receive SessionLookupKey from Authenticator V2 request!')

            session_state = self._poll_session_state()
            if session_state != AuthSessionState.APPROVED:
                raise AuthenticationException('Authentication by Authenticator V2 failed!'
                                              ' State: %s' % AuthSessionState(session_state))

            # Do not send auth_data when finishing TOTPv2 authentication
            auth_data = None
        response = self._finish_auth(auth_type, auth_data, otc, proof)

        try:
            return AuthenticationManager.parse_redirect_url(response.headers.get('Location'))
        except Exception as e:
            log.debug('Parsing redirection url failed, error: {0}'.format(str(e)))
            raise AuthenticationException("2FA: Location header does not hold access/refresh tokens!")


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
