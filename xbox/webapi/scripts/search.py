"""
Example script that utilizes EDSProvider to search XBL marketplace
"""
import sys
import json
import argparse

from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.common.exceptions import AuthenticationException
from xbox.webapi.scripts import TOKENS_FILE


def main():
    parser = argparse.ArgumentParser(description="Search for Content on XBL")
    parser.add_argument('--tokens', '-t', default=TOKENS_FILE,
                        help="Token filepath. Default: \'{}\'".format(TOKENS_FILE))
    parser.add_argument('--legacy', '-l', action='store_true',
                        help="Search for Xbox 360 content")
    parser.add_argument("--keys", action='append',
                        type=lambda kv: kv.split("="), dest='keyvalues')
    parser.add_argument('search_query',
                        help="Name to search for")

    args = parser.parse_args()

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

    xbl_client = XboxLiveClient(auth_mgr.userinfo.userhash, auth_mgr.xsts_token.jwt, auth_mgr.userinfo.xuid)

    keys = dict(args.keyvalues) if args.keyvalues else dict()
    if not args.legacy:
        resp = xbl_client.eds.get_singlemediagroup_search(args.search_query, 10, "DGame", domain="Modern", **keys)
    else:
        resp = xbl_client.eds.get_singlemediagroup_search(args.search_query, 10, "Xbox360Game", domain="Xbox360", **keys)

    if resp.status_code != 200:
        print("Invalid EDS details response")
        sys.exit(-1)

    print(json.dumps(resp.json(), indent=2))


if __name__ == '__main__':
    main()
