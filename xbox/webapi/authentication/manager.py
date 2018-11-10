"""
Authentication Manager

Authenticate with Windows Live Server and Xbox Live.
In case Two-Factor authentication is requested from provided account,
the user is asked for input via standard-input.
"""
import re
import json
import logging
import demjson
import requests
import xml.dom.minidom as minidom

from urllib.parse import urlparse, parse_qs

from xbox.webapi.authentication.token import Token
from xbox.webapi.authentication.token import AccessToken, RefreshToken, UserToken, DeviceToken, TitleToken, XSTSToken
from xbox.webapi.common.exceptions import AuthenticationException, TwoFactorAuthRequired
from xbox.webapi.common.userinfo import XboxLiveUserInfo

log = logging.getLogger('authentication')


class AuthenticationManager(object):
    def __init__(self):
        """
        Initialize an instance of :class:`AuthenticationManager`
        """
        self.session = requests.session()

        self.email_address = None
        self.password = None

        self.userinfo = None
        self.refresh_token = None
        self.access_token = None
        self.user_token = None
        self.xsts_token = None
        self.title_token = None
        self.device_token = None

    @property
    def authenticated(self):
        return bool(self.xsts_token and self.xsts_token.is_valid and
                    self.refresh_token and self.refresh_token.is_valid)

    # Backward compatibility
    @property
    def is_authenticated(self):
        return self.authenticated

    @classmethod
    def from_file(cls, filepath):
        mgr = cls()
        mgr.load(filepath)
        return mgr

    @classmethod
    def from_redirect_url(cls, redirect_url):
        mgr = cls()
        mgr.access_token, mgr.refresh_token = mgr.parse_redirect_url(redirect_url)
        return mgr

    def load(self, filepath):
        """
        Load tokens and userinfo from file and replace old tokens IF NEEDED

        Args:
            filepath (str): Filepath of json tokenfile
        """

        with open(filepath, 'r') as f:
            json_file = json.load(f)

        def should_replace(token_arg):
            """Check if stored token is non-existant or invalid"""
            if not token_arg or not token_arg.is_valid:
                return True

        file_tokens = json_file.get('tokens')
        for token in file_tokens:
            t = Token.from_dict(token)
            log.info('Loaded token %s from file' % type(t))
            if isinstance(t, AccessToken) and should_replace(self.access_token):
                self.access_token = t
            elif isinstance(t, RefreshToken) and should_replace(self.refresh_token):
                self.refresh_token = t
            elif isinstance(t, UserToken) and should_replace(self.user_token):
                self.user_token = t
            elif isinstance(t, DeviceToken) and should_replace(self.device_token):
                self.device_token = t
            elif isinstance(t, TitleToken) and should_replace(self.title_token):
                self.title_token = t
            elif isinstance(t, XSTSToken) and should_replace(self.xsts_token):
                self.xsts_token = t

        file_userinfo = json_file.get('userinfo')
        if not self.userinfo and file_userinfo:
            self.userinfo = XboxLiveUserInfo.from_dict(file_userinfo)

    def dump(self, filepath):
        """
        Save tokens and userinfo as json file

        Args:
            ts (object): Instance of :class:`Tokenstore`

        Returns:
            None
        """
        json_file = dict(tokens=list(), userinfo=None)

        tokens = [self.access_token, self.refresh_token, self.user_token,
                  self.xsts_token, self.title_token, self.device_token]
        for token in tokens:
            if not token:
                continue
            json_file['tokens'].append(token.to_dict())

        if self.userinfo:
            json_file['userinfo'] = self.userinfo.to_dict()

        with open(filepath, 'w') as f:
            json.dump(json_file, f, indent=2)

    @staticmethod
    def generate_authorization_url(response_type='token', client_id='0000000048093EE3',
                                   scope='service::user.auth.xboxlive.com::MBI_SSL',
                                   redirect_uri='https://login.live.com/oauth20_desktop.srf',
                                   state=None):
        """
        Generate Windows Live Authorization URL.

        Either standard values can be used, to authentication to XBL and get a XToken, or use custom
        parameters to authenticate with a specific service (Halo, Forza ... you name it)

        Args:
            response_type (str): Required authorization response, either 'code' or 'token'
            client_id (str): Client ID of service to authenticate with
            scope (str): Authorization scope
            redirect_uri (str): URL to redirect to when authentication succeeds
            state (str): Optional, OAuth2 state url

        Returns:
            str: Assembled URL, including query parameters
        """

        base_url = 'https://login.live.com/oauth20_authorize.srf'
        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': response_type,
            'display': 'touch',
            'scope': scope,
            'locale': 'en',
        }

        if state:
            params.update(state=state)

        return requests.Request('GET', base_url, params=params).prepare().url

    def authenticate(self, do_refresh=True):
        """
        Authenticate with Xbox Live using either tokens or user credentials.

        Args:
            do_refresh (bool): Refresh Access- and Refresh Token even if still valid, default: True

        Raises:
            AuthenticationException: When neither token and credential authentication is successful
            TwoFactorAuthRequired: If 2FA is required for this account
        """

        full_authentication_required = False

        try:
            # Refresh and Access Token
            if not do_refresh and self.access_token and self.refresh_token and \
                    self.access_token.is_valid and self.refresh_token.is_valid:
                pass
            else:
                self.access_token, self.refresh_token = self._windows_live_token_refresh(self.refresh_token)

            # User Token
            if self.user_token and self.user_token.is_valid:
                pass
            else:
                self.user_token = self._xbox_live_authenticate(self.access_token)

            '''
            TODO: Fix
            # Device Token
            if ts.device_token and ts.device_token.is_valid:
                pass
            else:
                ts.device_token = self._xbox_live_device_auth(ts.access_token)

            # Title Token
            if ts.title_token and ts.title_token.is_valid:
                pass
            else:
                ts.title_token = self._xbox_live_title_auth(ts.device_token, ts.access_token)
            '''

            # XSTS Token
            if self.xsts_token and self.xsts_token.is_valid and self.userinfo:
                pass
            else:
                self.xsts_token, self.userinfo = self._xbox_live_authorize(self.user_token)
        except AuthenticationException as e:
            log.warning('Token Auth failed: %s. Attempting auth via credentials' % e)
            full_authentication_required = True

        # Authentication via credentials
        if full_authentication_required and self.email_address and self.password:
            log.info('Attempting user credentials auth')
            self.access_token, self.refresh_token = self._windows_live_authenticate(self.email_address, self.password)
            self.user_token = self._xbox_live_authenticate(self.access_token)
            '''
            TODO: Fix
            ts.device_token = self._xbox_live_device_auth(ts.access_token)
            ts.title_token = self._xbox_live_title_auth(ts.device_token, ts.access_token)
            '''
            self.xsts_token, self.userinfo = self._xbox_live_authorize(self.user_token)

        if not self.authenticated:
            raise AuthenticationException("AuthenticationManager was not able to authenticate "
                                          "with provided tokens or user credentials!")

    def authenticate_with_service(self, authorization_url):
        """
        Authenticate with partnered service, requires a successful Windows Live Authentication.

        It works because stored cookies from the Windows Live Auth are used, entering the credentials
        again is unnecessary.

        Args:
            authorization_url (str): Authorization URL

        Returns:
            requests.Response: Response of the final request
        """
        if not self.authenticated:
            raise AuthenticationException("Not authenticated with Windows Live, please do that first, "
                                          "before attempting a service authentication")

        response = self.session.get(authorization_url, allow_redirects=False)
        if response.status_code != 302:
            raise AuthenticationException("Failed to authenticate with partner service")

        return self.session.get(response.headers['Location'])

    @staticmethod
    def extract_js_object(body, obj_name):
        """
        Find a javascript object inside a html-page via regex.

        When it is found, convert it to a python-compatible dict.

        Args:
            body (str/bytes): The raw HTTP body to parse
            obj_name (str): The name of the javascript-object to find

        Returns:
            dict: Parsed javascript-object on success, otherwise `None`
        """
        if isinstance(body, bytes):
            body = body.decode("utf-8")

        server_data_re = r"%s(?:.*?)=(?:.*?)({(?:.*?)});" % obj_name
        matches = re.findall(server_data_re, body, re.MULTILINE | re.IGNORECASE | re.DOTALL)
        if len(matches):
            return demjson.decode(matches[0])

    @staticmethod
    def parse_redirect_url(redirect_url):
        """
        Parse url query from redirection url to extract AccessToken and RefreshToken

        Args:
            redirect_url (str): Redirect URL returned from OAUTH

        Raises:
            Exception: When extraction of tokens fails

        Returns:
            On success `tuple` of (AccessToken, RefreshToken) is returned
        """
        location = urlparse(redirect_url)
        fragment = parse_qs(location.fragment)

        access_token = AccessToken(fragment['access_token'][0], fragment['expires_in'][0])
        refresh_token = RefreshToken(fragment['refresh_token'][0])
        return access_token, refresh_token

    def _windows_live_authenticate(self, email_address, password):
        """
        Internal method to authenticate with Windows Live, called by `self.authenticate`

        In case of required two-factor-authentication the respective routine is initialized and user gets asked for
        input of verification details.

        Args:
            email_address (str): Microsoft Account Email address
            password (str):  Microsoft Account password

        Raises:
            AuthenticationException: When returned headers do not contain Access-/Refresh-Tokens.
            TwoFactorAuthRequired: If 2FA is required for this account

        Returns:
            tuple: If authentication succeeds, `tuple` of (AccessToken, RefreshToken) is returned
        """
        response = self.__window_live_authenticate_request(email_address, password)

        proof_type = self.extract_js_object(response.content, "PROOF.Type")
        if proof_type:
            log.debug('Following 2fa proof-types gathered: {!s}'.format(proof_type))
            server_data = self.extract_js_object(response.content, "var ServerData")
            raise TwoFactorAuthRequired("Two Factor Authentication is required", server_data)

        try:
            # the access token is included in fragment of the location header
            return self.parse_redirect_url(response.headers.get('Location'))
        except Exception as e:
            log.debug('Parsing redirection url failed, error: {0}'.format(str(e)))
            raise AuthenticationException("Could not log in with supplied credentials")

    def _windows_live_token_refresh(self, refresh_token):
        """
        Internal method to refresh Windows Live Token, called by `self.authenticate`

        Raises:
            AuthenticationException: When provided Refresh-Token is invalid.

        Args:
            refresh_token (:class:`RefreshToken`): Refresh token

        Returns:
            tuple: If authentication succeeds, `tuple` of (AccessToken, RefreshToken) is returned
        """
        if not refresh_token or not refresh_token.is_valid:
            raise AuthenticationException("No valid RefreshToken")

        resp = self.__window_live_token_refresh_request(refresh_token)
        response = json.loads(resp.content.decode('utf-8'))

        if 'access_token' not in response:
            raise AuthenticationException("Could not refresh token via RefreshToken")

        access_token = AccessToken(response['access_token'], response['expires_in'])
        refresh_token = RefreshToken(response['refresh_token'])
        return access_token, refresh_token

    def _xbox_live_authenticate(self, access_token):
        """
        Internal method to authenticate with Xbox Live, called by `self.authenticate`

        Args:
            access_token (:class:`AccessToken`): Access token

        Raises:
            AuthenticationException: When provided Access-Token is invalid

        Returns:
            object: If authentication succeeds, returns :class:`UserToken`
        """
        if not access_token or not access_token.is_valid:
            raise AuthenticationException("No valid AccessToken")

        json_data = self.__xbox_live_authenticate_request(access_token).json()
        return UserToken(json_data['Token'], json_data['IssueInstant'], json_data['NotAfter'])

    def _xbox_live_device_auth(self, access_token):
        """
         Internal method to authenticate Device with Xbox Live, called by `self.authenticate`

         Args:
             access_token (:class:`AccessToken`): Access token

         Raises:
             AuthenticationException: When provided Access-Token is invalid

         Returns:
             object: If authentication succeeds, returns :class:`DeviceToken`
         """
        if not access_token or not access_token.is_valid:
            raise AuthenticationException("No valid AccessToken")

        json_data = self.__device_authenticate_request(access_token)
        json_data = json_data.json()
        return DeviceToken(json_data['Token'], json_data['IssueInstant'], json_data['NotAfter'])

    def _xbox_live_title_auth(self, device_token, access_token):
        """
         Internal method to authenticate Device with Xbox Live, called by `self.authenticate`

         Args:
             device_token (:class:`DeviceToken`): Device token
             access_token (:class:`AccessToken`): Access token

         Raises:
             AuthenticationException: When provided Access-Token is invalid

         Returns:
             object: If authentication succeeds, returns :class:`TitleToken`
         """
        if not access_token or not access_token.is_valid or \
           not device_token or not device_token.is_valid:
            raise AuthenticationException("No valid AccessToken/DeviceToken")

        json_data = self.__title_authenticate_request(device_token, access_token).json()
        return TitleToken(json_data['Token'], json_data['IssueInstant'], json_data['NotAfter'])

    def _xbox_live_authorize(self, user_token, device_token=None, title_token=None):
        """
        Internal method to authorize with Xbox Live, called by `self.authenticate`

        Args:
            user_token (:class:`UserToken`): User token
            device_token (:class:`DeviceToken`): Optional Device token
            title_token (:class:`TitleToken`): Optional Title token

         Raises:
             AuthenticationException: When provided User-Token is invalid

        Returns:
            tuple: If authentication succeeds, returns tuple of (:class:`XSTSToken`, :class:`XboxLiveUserInfo`)
        """
        if not user_token or not user_token.is_valid:
            raise AuthenticationException("No valid UserToken")

        json_data = self.__xbox_live_authorize_request(user_token, device_token, title_token).json()
        userinfo = json_data['DisplayClaims']['xui'][0]
        userinfo = XboxLiveUserInfo.from_dict(userinfo)

        xsts_token = XSTSToken(json_data['Token'], json_data['IssueInstant'], json_data['NotAfter'])
        return xsts_token, userinfo

    def __window_live_authenticate_request(self, email, password):
        """
        Authenticate with Windows Live Server.

        First, the Base-URL gets queried by HTTP-GET from a static URL. The resulting response holds a javascript-object
        containing Post-URL and PPFT parameter - both get used by the following HTTP-POST to attempt authentication by
        sending user-credentials in the POST-data.

        If the final POST-Response holds a 'Location' field in it's headers, the authentication can be considered
        successful and Access-/Refresh-Token are available.

        Args:
            email (str): Microsoft account email-address
            password (str): Corresponding password

        Returns:
            requests.Response: Response of the final POST-Request
        """

        authorization_url = AuthenticationManager.generate_authorization_url()
        resp = self.session.get(authorization_url, allow_redirects=False)

        if resp.status_code == 302 and \
           resp.headers['Location'].startswith('https://login.live.com/oauth20_desktop.srf'):
            # We are already authenticated by cached cookies
            return resp

        # Extract ServerData javascript-object via regex, convert it to proper JSON
        server_data = self.extract_js_object(resp.content, "var ServerData")
        # Extract PPFT value (flowtoken)
        ppft = server_data.get('sFTTag')
        ppft = minidom.parseString(ppft).getElementsByTagName("input")[0].getAttribute("value")

        credential_type_url = None
        for k, v in server_data.items():
            if isinstance(v, str) and v.startswith('https://login.live.com/GetCredentialType.srf'):
                credential_type_url = v
        if not credential_type_url:
            raise AuthenticationException('Did not find GetCredentialType URL')

        post_data = {
            'username': email,
            'uaid': self.session.cookies['uaid'],
            'isOtherIdpSupported': False,
            'checkPhones': False,
            'isRemoteNGCSupported': True,
            'isCookieBannerShown': False,
            'isFidoSupported': False,
            'flowToken': ppft
        }
        resp = self.session.post(credential_type_url, json=post_data, headers=dict(Referer=resp.url))
        credential_type = resp.json()

        post_data = {
            'login': email,
            'passwd': password,
            'PPFT': ppft,
            'PPSX': 'Passpor',
            'SI': 'Sign in',
            'type': '11',
            'NewUser': '1',
            'LoginOptions': '1'
        }

        if 'Credentials' not in credential_type:
            raise AuthenticationException('Did not find Credentials in CredentialType respose, auth likely failed!')
        elif credential_type['Credentials']['HasRemoteNGC'] == 1:
            ngc_params = credential_type['Credentials']['RemoteNgcParams']
            post_data.update({
                'ps': 2,
                'psRNGCEntropy': ngc_params['SessionIdentifier'],
                'psRNGCDefaultType': ngc_params['DefaultType']
            })

        return self.session.post(server_data.get('urlPost'), data=post_data, allow_redirects=False)

    def __window_live_token_refresh_request(self, refresh_token):
        """
        Refresh the Windows Live Token by sending HTTP-GET Request containing Refresh-token in query to a static URL.

        Args:
            refresh_token (:class:`RefreshToken`): Refresh token from a previous Windows Live Authentication

        Returns:
            requests.Response: Response of HTTP-GET
        """
        base_url = 'https://login.live.com/oauth20_token.srf?'
        params = {
            'grant_type': 'refresh_token',
            'client_id': '0000000048093EE3',
            'scope': 'service::user.auth.xboxlive.com::MBI_SSL',
            'refresh_token': refresh_token.jwt,
        }

        return self.session.get(base_url, params=params)

    def __xbox_live_authenticate_request(self, access_token):
        """
        Authenticate with Xbox Live by sending HTTP-POST containing Windows-Live Access-Token to User-Auth endpoint.

        Args:
            access_token (:class:`AccessToken`): Access token from the Windows-Live-Authentication

        Returns:
           requests.Response: Response of HTTP-POST
        """
        url = 'https://user.auth.xboxlive.com/user/authenticate'
        headers = {"x-xbl-contract-version": "1"}
        data = {
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT",
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": access_token.jwt,
            }
        }

        return self.session.post(url, json=data, headers=headers)

    def __xbox_live_authorize_request(self, user_token, device_token=None, title_token=None):
        """
        Authorize with Xbox Live by sending Xbox-Live User-Token via HTTP Post to the XSTS-Authorize endpoint.

        Args:
            user_token (:class:`UserToken`): User token from the Xbox-Live Authentication
            device_token (:class:`DeviceToken`): Optional Device token from Xbox-Live Device Authentication
            title_token (:class:`TitleToken`): Optional Title token from Xbox-Live Title Authentication

        Returns:
            requests.Response: Response of HTTP-POST
        """
        url = 'https://xsts.auth.xboxlive.com/xsts/authorize'
        headers = {"x-xbl-contract-version": "1"}
        data = {
            "RelyingParty": "http://xboxlive.com",
            "TokenType": "JWT",
            "Properties": {
                "UserTokens": [user_token.jwt],
                "SandboxId": "RETAIL",
            }
        }

        if device_token:
            data["Properties"].update({"DeviceToken": device_token.jwt})
        if title_token:
            data["Properties"].update({"TitleToken": title_token.jwt})

        return self.session.post(url, json=data, headers=headers)

    def __title_authenticate_request(self, device_token, access_token):
        """
        Authenticate Title / App with Xbox Live.

        On successful authentication it might show as "Currently playing" to friends or followers.

        Args:
            device_token (:class:`DeviceToken`): Device token obtained by Device Authentication.
            access_token (:class:`AccessToken`): Access token

        Returns:
            requests.Response: Response of HTTP-POST
        """
        url = "https://title.auth.xboxlive.com"
        headers = {"x-xbl-contract-version": "1"}
        data = {
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT",
            "Properties": {
                "AuthMethod": "RPS",
                "DeviceToken": device_token.jwt,
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": access_token.jwt
            }
        }

        return self.session.post(url, json=data, headers=headers)

    def __device_authenticate_request(self, access_token):
        """
        Authenticate your current device with Xbox Live.

        Args:
            access_token (:class:`AccessToken`): Access token

        Returns:
            requests.Response: Response of HTTP-POST`
        """
        url = "https://device.auth.xboxlive.com/device/authenticate"
        headers = {"x-xbl-contract-version": "1"}
        data = {
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT",
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": access_token.jwt,
            }
        }

        return self.session.post(url, json=data, headers=headers)
