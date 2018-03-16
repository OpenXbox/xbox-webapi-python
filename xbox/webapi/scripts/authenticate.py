"""
Example scripts that performs XBL authentication
"""
import sys
import argparse
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.common.exceptions import AuthenticationException


def main():
    parser = argparse.ArgumentParser(description="Authenticate with xbox live")
    parser.add_argument('--tokenfile', '-t',
                        help="Token file, if file doesnt exist it gets created")
    parser.add_argument('--email', '-e',
                        help="Microsoft Account Email address")
    parser.add_argument('--password', '-p',
                        help="Microsoft Account password")

    args = parser.parse_args()

    if not args.tokenfile and not args.email and not args.password:
        print('No data to authenticate with passed!')
        print('Try the --help switch!')
        sys.exit(1)

    auth_mgr = AuthenticationManager()
    if args.tokenfile:
        try:
            auth_mgr.load_tokens_from_file(args.tokenfile)
        except Exception as e:
            print('Failed to load tokens from %s, Error: %s' % (args.tokenfile, e))

    if args.email and args.password:
        auth_mgr.email_address = args.email
        auth_mgr.password = args.password

    try:
        auth_mgr.authenticate(do_refresh=True)
    except AuthenticationException as e:
        print('Email/Password authentication failed! Err: %s' % e)
        sys.exit(-1)

    if args.tokenfile:
        auth_mgr.save_tokens_to_file(args.tokenfile)

    print('Refresh Token: %s' % auth_mgr.refresh_token)
    print('XSTS Token: %s' % auth_mgr.xsts_token)
    print('Userinfo: %s' % auth_mgr.userinfo)


if __name__ == '__main__':
    main()
