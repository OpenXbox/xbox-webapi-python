"""
Example script that enables using your one-time-free gamertag change
"""
import sys
import argparse

from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.common.exceptions import AuthenticationException
from xbox.webapi.scripts import TOKENS_FILE


def main():
    parser = argparse.ArgumentParser(description="Change your gamertag")
    parser.add_argument('--tokens', '-t', default=TOKENS_FILE,
                        help="Token filepath. Default: \'{}\'".format(TOKENS_FILE))
    parser.add_argument('gamertag',
                        help="Desired Gamertag")

    args = parser.parse_args()

    if len(args.gamertag) > 15:
        print('Desired gamertag exceedes limit of 15 chars')
        sys.exit(-1)

    try:
        auth_mgr = AuthenticationManager.from_file(args.tokens)
    except FileNotFoundError as e:

        print(
            'Failed to load tokens from \'{}\'.\n'
            'ERROR: {}'.format(e.filename, e.strerror)
        )
        sys.exit(-1)

    try:
        auth_mgr.authenticate(do_refresh=True)
    except AuthenticationException as e:
        print('Authentication failed! Err: %s' % e)
        sys.exit(-1)

    xbl_client = XboxLiveClient(auth_mgr.userinfo.userhash,
                                auth_mgr.xsts_token.jwt,
                                auth_mgr.userinfo.xuid)

    print(':: Trying to change gamertag to \'%s\' for xuid \'%i\'...' %
          (args.gamertag, xbl_client.xuid))

    print('Claiming gamertag...')
    resp = xbl_client.account.claim_gamertag(xbl_client.xuid, args.gamertag)
    if resp.status_code == 409:
        print('Claiming gamertag failed - Desired gamertag is unavailable')
        sys.exit(-1)
    elif resp.status_code != 200:
        print('Invalid HTTP response from claim: %i' % resp.status_code)
        print('Headers: %s' % resp.headers)
        print('Response: %s' % resp.content)
        sys.exit(-1)

    print('Changing gamertag...')
    resp = xbl_client.account.change_gamertag(xbl_client.xuid, args.gamertag)
    if resp.status_code == 1020:
        print('Changing gamertag failed - You are out of free changes')
        sys.exit(-1)
    elif resp.status_code != 200:
        print('Invalid HTTP response from change: %i' % resp.status_code)
        print('Headers: %s' % resp.headers)
        print('Response: %s' % resp.content)
        sys.exit(-1)

    print('Gamertag successfully changed to %s' % args.gamertag)


if __name__ == '__main__':
    main()
