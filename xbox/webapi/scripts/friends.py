"""
Example script that enables using your one-time-free gamertag change
"""
import argparse
import asyncio
import os
from pprint import pprint
import sys

from aiohttp import ClientResponseError, ClientSession

from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.models import OAuth2TokenResponse
from xbox.webapi.scripts import TOKENS_FILE


async def async_main():
    parser = argparse.ArgumentParser(description="Change your gamertag")
    parser.add_argument(
        "--tokens",
        "-t",
        default=TOKENS_FILE,
        help=f"Token filepath. Default: '{TOKENS_FILE}'",
    )
    parser.add_argument(
        "--client-id",
        "-cid",
        default=os.environ.get("CLIENT_ID", ""),
        help="OAuth2 Client ID",
    )
    parser.add_argument(
        "--client-secret",
        "-cs",
        default=os.environ.get("CLIENT_SECRET", ""),
        help="OAuth2 Client Secret",
    )

    args = parser.parse_args()

    if not os.path.exists(args.tokens):
        print("No token file found, run xbox-authenticate")
        sys.exit(-1)

    async with ClientSession() as session:
        auth_mgr = AuthenticationManager(
            session, args.client_id, args.client_secret, ""
        )

        with open(args.tokens, mode="r") as f:
            tokens = f.read()
        auth_mgr.oauth = OAuth2TokenResponse.parse_raw(tokens)
        try:
            await auth_mgr.refresh_tokens()
        except ClientResponseError:
            print("Could not refresh tokens")
            sys.exit(-1)

        with open(args.tokens, mode="w") as f:
            f.write(auth_mgr.oauth.json())

        xbl_client = XboxLiveClient(auth_mgr)

        try:
            resp = await xbl_client.people.get_friends_own()
        except ClientResponseError:
            print("Invalid HTTP response")
            sys.exit(-1)

        pprint(resp.dict())


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())


if __name__ == "__main__":
    main()
