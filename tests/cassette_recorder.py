import sys
import os
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

    """
    EDIT TO RECORD NEW API ENDPOINT
    """
    filename = 'usersearch_test'

    def dump_response(resp):
        print(resp.status_code)
        if resp.status_code != 200:
            print(resp.headers)
            print(resp.content)
            os.remove(CASSETTE_LIBRARY_DIR + filename + ".json")
            sys.exit(1)
        print(json.dumps(resp.json(), indent=2))
        print('!!! SUCCESS !!!')

    recorder = betamax.Betamax(client.session)
    with recorder.use_cassette(filename):
        """
        EDIT TO RECORD NEW API ENDPOINT
        """
        ret = client.usersearch.get_live_search('<>')
        dump_response(ret)


if __name__ == '__main__':
    main()
