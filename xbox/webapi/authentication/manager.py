"""
Authentication Manager

Authenticate with Windows Live Server and Xbox Live.
In case Two-Factor authentication is requested from provided account,
the user is asked for input via standard-input.
"""
import json
import requests
import re
import demjson
import logging
import io

import xml.dom.minidom as minidom

try:
    # Python 3
    from urllib.parse import urlparse, parse_qs
except ImportError:
    # Python 2
    from urlparse import urlparse, parse_qs

from xbox.webapi.authentication.two_factor import TwoFactorAuthentication
from xbox.webapi.authentication.token import Token
from xbox.webapi.authentication.token import AccessToken, RefreshToken, UserToken, DeviceToken, TitleToken, XSTSToken
from xbox.webapi.common.exceptions import AuthenticationException
from xbox.webapi.common.userinfo import XboxLiveUserInfo

log = logging.getLogger('authentication')


class AuthenticationManager(object):
    def __init__(self):
        """
        Initialize an instance of :class:`AuthenticationManager`
        """
        self.session = requests.session()
        self.authenticated = False

        self._email_address = None
        self._password = None

        self._userinfo = None
        self._refresh_token = None
        self._access_token = None
        self._user_token = None
        self._xsts_token = None
        self._title_token = None
        self._device_token = None

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def email_address(self):
        """
        Get or set Microsoft Account email address

        Returns:
            str: `None` if not set
        """
        return self._email_address

    @email_address.setter
    def email_address(self, email_address):
        self._email_address = email_address

    @property
    def password(self):
        """
        Get or set Microsoft Account password

        Returns:
            str: `None` if not set
        """
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def userinfo(self):
        """
        Get or set Userinfo

        Returns:
            :class:`XboxLiveUserInfo`: `None` if not set
        """
        return self._userinfo

    @userinfo.setter
    def userinfo(self, userinfo):
        self._userinfo = userinfo

    @property
    def refresh_token(self):
        """
        Get or set Refresh token

        Returns:
            :class:`RefreshToken`: `None` if not set
        """
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, refresh_token):
        self._refresh_token = refresh_token

    @property
    def access_token(self):
        """
        Get or set Access token

        Returns:
            :class:`AccessToken`: `None` if not set
        """
        return self._access_token

    @access_token.setter
    def access_token(self, access_token):
        self._access_token = access_token

    @property
    def user_token(self):
        """
        Get or set User token

        Returns:
            :class:`UserToken`: `None` if not set
        """
        return self._user_token

    @user_token.setter
    def user_token(self, user_token):
        self._user_token = user_token

    @property
    def xsts_token(self):
        """
        Get or set XSTS token

        Returns:
            :class:`XSTSToken`: `None` if not set
        """
        return self._xsts_token

    @xsts_token.setter
    def xsts_token(self, xsts_token):
        self._xsts_token = xsts_token

    @property
    def title_token(self):
        """
        Get or set Title token

        Returns:
            :class:`TitleToken`: `None` if not set
        """
        return self._title_token

    @title_token.setter
    def title_token(self, title_token):
        self._title_token = title_token

    @property
    def device_token(self):
        """
        Get or set Device token

        Returns:
            :class:`DeviceToken`: `None` if not set
        """
        return self._device_token

    @device_token.setter
    def device_token(self, device_token):
        self._device_token = device_token

    def load_tokens_from_file(self, filepath):
        """
        Load tokens and userinfo from file and replace old tokens IF NEEDED

        Args:
            filepath (str): Filepath of json tokenfile
        """

        with io.open(filepath, 'rt') as f:
            json_file = json.load(f)

        def should_replace(token_arg, token_file):
            """Check if token from file is newer than from tokenstore"""
            if (not token_arg or not token_arg.is_valid) and \
                    token_file and token_file.is_valid:
                return True

        file_tokens = json_file.get('tokens')
        for token in file_tokens:
            t = Token.from_dict(token)
            log.info('Loaded token %s from file' % type(t))
            if isinstance(t, AccessToken) and should_replace(self.access_token, t):
                self.access_token = t
            elif isinstance(t, RefreshToken) and should_replace(self.refresh_token, t):
                self.refresh_token = t
            elif isinstance(t, UserToken) and should_replace(self.user_token, t):
                self.user_token = t
            elif isinstance(t, DeviceToken) and should_replace(self.device_token, t):
                self.device_token = t
            elif isinstance(t, TitleToken) and should_replace(self.title_token, t):
                self.title_token = t
            elif isinstance(t, XSTSToken) and should_replace(self.xsts_token, t):
                self.xsts_token = t

        file_userinfo = json_file.get('userinfo')
        if not self.userinfo and file_userinfo:
            self.userinfo = XboxLiveUserInfo.from_dict(file_userinfo)

    def save_tokens_to_file(self, filepath):
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

        with io.open(filepath, 'wt') as f:
            json.dump(json_file, f, indent=2)

    def authenticate(self, do_refresh=True):
        """
        Authenticate with Xbox Live using either tokens or user credentials.

        After being called, its property `is_authenticated` should be checked for success.

        Args:
            do_refresh (bool): Refresh Access- and Refresh Token even if still valid, default: True

        Raises:
            AuthenticationException: When neither token and credential authentication is successful
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
                self.authenticated = True
            else:
                self.xsts_token, self.userinfo = self._xbox_live_authorize(self.user_token)
                self.authenticated = True
        except AuthenticationException:
            full_authentication_required = True

        # Authentication via credentials
        if full_authentication_required and self.email_address and self.password:
            self.access_token, self.refresh_token = self._windows_live_authenticate(self.email_address, self.password)
            self.user_token = self._xbox_live_authenticate(self.access_token)
            '''
            TODO: Fix
            ts.device_token = self._xbox_live_device_auth(ts.access_token)
            ts.title_token = self._xbox_live_title_auth(ts.device_token, ts.access_token)
            '''
            self.xsts_token, self.userinfo = self._xbox_live_authorize(self.user_token)
            self.authenticated = True

        if not self.authenticated:
            raise AuthenticationException("AuthenticationManager was not able to authenticate "
                                          "with provided tokens or user credentials!")

    def _extract_js_object(self, body, obj_name):
        """
        Find a javascript object inside a html-page via regex.

        When it is found, convert it to a python-compatible dict.

        Args:
            body (str): The raw HTTP body to parse
            obj_name (str): The name of the javascript-object to find

        Returns:
            dict: Parsed javascript-object on success, otherwise `None`
        """
        server_data_re = r"%s(?:.*?)=(?:.*?)({(?:.*?)});" % (obj_name)
        matches = re.findall(server_data_re, body, re.MULTILINE | re.IGNORECASE | re.DOTALL)
        if len(matches):
            return demjson.decode(matches[0])

    def _windows_live_authenticate(self, email_address, password):
        """
        Internal method to authenticate with Windows Live, called by `self.authenticate`

        In case of required two-factor-authentication the respective routine is initialized and user gets asked for
        input of verification details.

        Args:
            email_address (str): Microsoft Account Email address
            password (str):  Microsoft Account password

        Raises:
            AuthenticationException: When two-factor-authentication fails or returned headers do not contain
            Access-/Refresh-Tokens.

        Returns:
            tuple: If authentication succeeds, `tuple` of (AccessToken, RefreshToken) is returned
        """
        response = self.__window_live_authenticate_request(email_address, password)

        proof_type = self._extract_js_object(response.content.decode("utf-8"), "PROOF.Type")
        if proof_type:
            log.info("Two Factor Authentication required!")
            twofactor = TwoFactorAuthentication(self.session)
            server_data = self._extract_js_object(response.content.decode("utf-8"), "ServerData")
            response = twofactor.authenticate(email_address, server_data)
            if not response:
                raise AuthenticationException("Two Factor Authentication failed!")

        if 'Location' not in response.headers:
            # we can only assume the login failed
            raise AuthenticationException("Could not log in with supplied credentials")

        # the access token is included in fragment of the location header
        location = urlparse(response.headers['Location'])
        fragment = parse_qs(location.fragment)

        access_token = AccessToken(fragment['access_token'][0], fragment['expires_in'][0])
        refresh_token = RefreshToken(fragment['refresh_token'][0])
        return access_token, refresh_token

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
        if refresh_token and refresh_token.is_valid:
            resp = self.__window_live_token_refresh_request(refresh_token)
            response = json.loads(resp.content.decode('utf-8'))

            if 'access_token' not in response:
                raise AuthenticationException("Could not refresh token via RefreshToken")

            access_token = AccessToken(response['access_token'], response['expires_in'])
            refresh_token = RefreshToken(response['refresh_token'])
            return access_token, refresh_token
        else:
            raise AuthenticationException("No valid RefreshToken")

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
        if access_token and access_token.is_valid:
            json_data = self.__xbox_live_authenticate_request(access_token).json()
            return UserToken(json_data['Token'], json_data['IssueInstant'], json_data['NotAfter'])
        else:
            raise AuthenticationException("No valid AccessToken")

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
        if access_token and access_token.is_valid:
            json_data = self.__device_authenticate_request(access_token)
            print(json_data.status_code)
            print(json_data.headers)
            print(json_data.content)
            json_data = json_data.json()
            return DeviceToken(json_data['Token'], json_data['IssueInstant'], json_data['NotAfter'])
        else:
            raise AuthenticationException("No valid AccessToken")

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
        if access_token and access_token.is_valid and device_token and device_token.is_valid:
            json_data = self.__title_authenticate_request(device_token, access_token).json()
            return TitleToken(json_data['Token'], json_data['IssueInstant'], json_data['NotAfter'])
        else:
            raise AuthenticationException("No valid AccessToken/DeviceToken")

    def _xbox_live_authorize(self, user_token, device_token=None, title_token=None):
        """
        Internal method to authorize with Xbox Live, called by `self.authenticate`

        Args:
            user_token (:class:`UserToken`): User token
            device_token (:class:`DeviceToken`): Optional Device token
            title_token (:class:`TitleToken`): Optional Title token

        Returns:
            tuple: If authentication succeeds, returns tuple of (:class:`XSTSToken`, :class:`XboxLiveUserInfo`)
        """
        if user_token and user_token.is_valid:
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

        base_url = 'https://login.live.com/oauth20_authorize.srf?'

        params = {
            'client_id': '0000000048093EE3',
            'redirect_uri': 'https://login.live.com/oauth20_desktop.srf',
            'response_type': 'token',
            'display': 'touch',
            'scope': 'service::user.auth.xboxlive.com::MBI_SSL',
            'locale': 'en',
        }
        resp = self.session.get(base_url, params=params)

        # Extract ServerData javascript-object via regex, convert it to proper JSON
        server_data = self._extract_js_object(resp.content.decode("utf-8"), "ServerData")
        # Extract PPFT value
        ppft = server_data.get('sFTTag')
        ppft = minidom.parseString(ppft).getElementsByTagName("input")[0].getAttribute("value")

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
