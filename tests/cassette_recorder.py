import sys
import json
import argparse
import betamax
from betamax_serializers import pretty_json
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.scripts import TOKENS_FILE
from xbox.webapi.api.client import XboxLiveClient

CASSETTE_LIBRARY_DIR = 'data/cassettes/'

betamax.Betamax.register_serializer(pretty_json.PrettyJSONSerializer)


def main():
    parser = argparse.ArgumentParser(description="Search for Content on XBL")
    parser.add_argument('--tokens', '-t', default=TOKENS_FILE,
                        help="Token file, if file doesnt exist it gets created")
    args = parser.parse_args()

    mgr = AuthenticationManager.from_file(args.tokens)

    client = XboxLiveClient(mgr.userinfo.userhash,
                            mgr.xsts_token.jwt,
                            mgr.userinfo.xuid)

    with betamax.Betamax.configure() as config:
        config.cassette_library_dir = CASSETTE_LIBRARY_DIR
        config.default_cassette_options['record_mode'] = 'new_episodes'
        config.default_cassette_options['serialize_with'] = 'prettyjson'
        # Make sure to not expose private tokens
        config.define_cassette_placeholder(
            "<UHS>", mgr.userinfo.userhash
        )
        config.define_cassette_placeholder(
            "<JWT>", mgr.xsts_token.jwt
        )
        config.define_cassette_placeholder(
            "<XUID>", str(mgr.userinfo.xuid)
        )

    def dump_response(resp):
        print(resp.status_code)
        if resp.status_code != 200:
            print(resp.headers)
            print(resp.content)
            sys.exit(1)
        print(json.dumps(resp.json(), indent=2))
        print('!!! SUCCESS !!!')

    recorder = betamax.Betamax(client.session)

    """
    EDIT TO RECORD NEW API ENDPOINT
    """

    title_id = '219630713'
    xuid = '2669321029139235'

    # req = [
    #     # client.screenshots.get_recent_own_screenshots(),
    #     # client.screenshots.get_recent_own_screenshots(title_id),
    #     # client.screenshots.get_recent_screenshots_by_xuid(xuid),
    #     client.screenshots.get_recent_screenshots_by_xuid(xuid, title_id),

    #     # client.screenshots.get_saved_community_screenshots_by_title_id(title_id),
    #     # client.screenshots.get_saved_own_screenshots(),
    #     # client.screenshots.get_saved_own_screenshots(title_id),
    #     # client.screenshots.get_saved_screenshots_by_xuid(xuid),
    #     # client.screenshots.get_saved_screenshots_by_xuid(xuid, title_id)
    # ]

    with recorder.use_cassette('screenshots_community'):
        client.screenshots.get_recent_community_screenshots_by_title_id(title_id)
    with recorder.use_cassette('screenshots_specific_user'):
        client.screenshots.get_recent_screenshots_by_xuid(xuid, title_id)

    # for r in req:
    #     dump_response(r)


if __name__ == '__main__':
    main()
