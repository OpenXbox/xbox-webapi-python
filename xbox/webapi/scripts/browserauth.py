"""
Semi-automatic XBL authentication

Authentication Flow:
* Execute script to get auth URL
* Visit auth URL in browser
* Authenticate in browser
* Copy REDIRECT URL from browser
* Execute script again, with REDIRECT URL, to finish authentication
"""

import sys
import argparse
import requests
from urllib.parse import urlparse, parse_qs

from xbox.webapi.authentication.token import AccessToken, RefreshToken
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.common.exceptions import AuthenticationException
from xbox.webapi.scripts import TOKENS_FILE


def get_authorization_url():
    base_url = 'https://login.live.com/oauth20_authorize.srf'
    params = {
        'client_id': '0000000048093EE3',
        'redirect_uri': 'https://login.live.com/oauth20_desktop.srf',
        'response_type': 'token',
        'display': 'touch',
        'scope': 'service::user.auth.xboxlive.com::MBI_SSL',
        'locale': 'en',
    }
    return requests.Request('GET', base_url, params=params).prepare().url


def get_tokens_from_url(url):
    location = urlparse(url)
    fragment = parse_qs(location.fragment)

    access_token = AccessToken(fragment['access_token'][0], fragment['expires_in'][0])
    refresh_token = RefreshToken(fragment['refresh_token'][0])
    return access_token, refresh_token


def main():
    parser = argparse.ArgumentParser(description="Authenticate with xbox live, manual webbrowser way")
    parser.add_argument('url', nargs='?', default=None,
                        help="Redirect URL of successful authentication")
    parser.add_argument('--tokens', '-t', default=TOKENS_FILE,
                        help="Token filepath, file gets created if nonexistent and auth is successful."
                             " Default: {}".format(TOKENS_FILE))

    args = parser.parse_args()

    if not args.url:
        print('Visit following URL in your webbrowser and authenticate yourself, then restart'
              ' this script with \'<redirect url>\' argument\n\n'
              '{}'.format(get_authorization_url()))
        sys.exit(0)

    url_begin = 'https://login.live.com/oauth20_desktop.srf?'
    if not args.url.startswith(url_begin):
        print('Wrong redirect url, expected url like: \'{}...\''.format(url_begin))
        sys.exit(1)

    auth_mgr = AuthenticationManager()
    try:
        print('Extracting tokens from URL')
        auth_mgr.access_token, auth_mgr.refresh_token = get_tokens_from_url(args.url)
    except Exception as e:
        print('Failed to get tokens from supplied redirect URL, err: {}'.format(e))
        sys.exit(2)

    try:
        print('Authenticating with Xbox Live')
        auth_mgr.authenticate(do_refresh=False)
    except AuthenticationException as e:
        print('Authentication failed! err: {}'.format(e))
        sys.exit(3)

    auth_mgr.dump(args.tokens)
    print('Success, tokens are stored at \'{}\''.format(args.tokens))


if __name__ == '__main__':
    main()
