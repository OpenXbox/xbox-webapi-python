"""
Example scripts that performs XBL authentication
"""
import sys
import argparse

import getpass

from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.two_factor import TwoFactorAuthentication, TwoFactorAuthMethods
from xbox.webapi.common.exceptions import AuthenticationException, TwoFactorAuthRequired
from xbox.webapi.scripts import TOKENS_FILE


def __input_prompt(prompt, entries=None):
    """
    Args:
        prompt (str): Prompt string
        entries (list): optional, list of entries to choose from

    Returns:
        str: userinput
    """
    prepend = ''

    if entries:
        assert isinstance(entries, list)
        prepend += 'Choose desired entry:\n'
        for num, entry in enumerate(entries):
            prepend += '  {}: {}\n'.format(num, entry)

    return input(prepend + prompt + ': ')


def two_factor_auth(auth_mgr, server_data):
    otc = None
    proof = None

    two_fa = TwoFactorAuthentication(auth_mgr.session, auth_mgr.email_address, server_data)
    strategies = two_fa.auth_strategies

    entries = ['{!s}, Name: {}'.format(
        TwoFactorAuthMethods(strategy.get('type', 0)), strategy.get('display'))
        for strategy in strategies
    ]

    index = int(__input_prompt('Choose desired auth method', entries))

    if index < 0 or index >= len(strategies):
        raise AuthenticationException('Invalid auth strategy index chosen!')

    verification_prompt = two_fa.get_method_verification_prompt(index)
    if verification_prompt:
        proof = __input_prompt(verification_prompt)

    need_otc = two_fa.check_otc(index, proof)
    if need_otc:
        otc = __input_prompt('Enter One-Time-Code (OTC)')

    access_token, refresh_token = two_fa.authenticate(index, proof, otc)
    auth_mgr.access_token = access_token
    auth_mgr.refresh_token = refresh_token
    auth_mgr.authenticate()


def main():
    parser = argparse.ArgumentParser(description="Authenticate with xbox live")
    parser.add_argument('--tokens', '-t', default=TOKENS_FILE,
                        help="Token filepath, file gets created if nonexistent and auth is successful."
                             " Default: {}".format(TOKENS_FILE))
    parser.add_argument('--email', '-e',
                        help="Microsoft Account Email address")
    parser.add_argument('--password', '-p',
                        help="Microsoft Account password")

    args = parser.parse_args()

    tokens_loaded = False
    two_factor_auth_required = False
    server_data = None

    auth_mgr = AuthenticationManager()
    if args.tokens:
        try:
            auth_mgr.load(args.tokens)
            tokens_loaded = True
        except FileNotFoundError as e:
            print('Failed to load tokens from \'{}\'. Error: {}'.format(e.filename, e.strerror))

    auth_mgr.email_address = args.email
    auth_mgr.password = args.password

    if (not args.email or not args.password) and not tokens_loaded:
        print("Please input authentication credentials")
    if not args.email and not tokens_loaded:
        auth_mgr.email_address = input("Microsoft Account Email: ")
    if not args.password and not tokens_loaded:
        auth_mgr.password = getpass.getpass('Microsoft Account Password: ')

    try:
        auth_mgr.authenticate(do_refresh=True)
    except TwoFactorAuthRequired as e:
        print('2FA is required, message: %s' % e)
        two_factor_auth_required = True
        server_data = e.server_data
    except AuthenticationException as e:
        print('Email/Password authentication failed! Err: %s' % e)
        sys.exit(-1)

    if two_factor_auth_required:
        try:
            two_factor_auth(auth_mgr, server_data)
        except AuthenticationException as e:
            print('2FA Authentication failed! Err: %s' % e)
            sys.exit(-1)

    if args.tokens:
        auth_mgr.dump(args.tokens)

    print('Refresh Token: %s' % auth_mgr.refresh_token)
    print('XSTS Token: %s' % auth_mgr.xsts_token)
    print('Userinfo: %s' % auth_mgr.userinfo)


if __name__ == '__main__':
    main()
