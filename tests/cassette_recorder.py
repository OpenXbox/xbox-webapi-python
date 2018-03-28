import sys
import json
import argparse
import betamax
from betamax_serializers import pretty_json
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.api.client import XboxLiveClient

CASSETTE_LIBRARY_DIR = 'data/cassettes/'

betamax.Betamax.register_serializer(pretty_json.PrettyJSONSerializer)


def main():
    parser = argparse.ArgumentParser(description="Search for Content on XBL")
    parser.add_argument('--tokens', '-t', default='tokens.json',
                        help="Token file, if file doesnt exist it gets created")
    args = parser.parse_args()

    mgr = AuthenticationManager()
    mgr.load_tokens_from_file(args.tokens)

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
    with recorder.use_cassette('gameclips_clips_xuid'):
        ret = client.gameclips.get_clips_by_xuid('2669321029139235', skip_items=0, max_items=25)
        dump_response(ret)

    with recorder.use_cassette('gameclips_own_clips'):
        ret = client.gameclips.get_own_clips(skip_items=0, max_items=25)
        dump_response(ret)

    with recorder.use_cassette('gameclips_community_title_id'):
        ret = client.gameclips.get_recent_community_clips_by_title_id(219630713)
        dump_response(ret)


if __name__ == '__main__':
    main()
