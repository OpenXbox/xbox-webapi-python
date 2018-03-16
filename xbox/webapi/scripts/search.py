"""
Example script that utilizes EDSProvider to search XBL marketplace
"""
import sys
import json
import argparse
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.common.exceptions import AuthenticationException
from xbox.webapi.api.client import XboxLiveClient


def main():
    parser = argparse.ArgumentParser(description="Search for Content on XBL")
    parser.add_argument('--tokenfile', '-t',
                        help="Token file, if file doesnt exist it gets created")
    parser.add_argument('--legacy', '-l', action='store_true',
                        help="Search for Xbox 360 content")
    parser.add_argument("--keys", action='append',
                        type=lambda kv: kv.split("="), dest='keyvalues')
    parser.add_argument('search_query',
                        help="Name to search for")

    args = parser.parse_args()

    if not args.tokenfile:
        print('Cannot use XboxLiveClient without tokens!')
        print('Please provide tokenfile with -t / --tokenfile switch')
        sys.exit(-1)

    auth_mgr = AuthenticationManager()
    auth_mgr.load_tokens_from_file(args.tokenfile)

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
