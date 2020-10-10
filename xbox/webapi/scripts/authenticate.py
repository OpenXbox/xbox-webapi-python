"""
Example scripts that performs XBL authentication
"""
import argparse
import asyncio
import os
import webbrowser

from aiohttp import ClientSession, web

from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.models import OAuth2TokenResponse
from xbox.webapi.scripts import TOKENS_FILE

CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://localhost:8080/auth/callback"
TOKENS = ""

queue = asyncio.Queue(1)


async def auth_callback(request):
    error = request.query.get("error")
    if error:
        description = request.query.get("error_description")
        print(f"Error in auth_callback: {description}")
        return
    # Run in task to not make unsuccessful parsing the HTTP response fail
    asyncio.create_task(queue.put(request.query["code"]))
    return web.Response(
        headers={"content-type": "text/html"},
        text="<script>window.close()</script>",
    )


async def async_main():

    async with ClientSession() as session:
        auth_mgr = AuthenticationManager(
            session, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
        )

        # Refresh tokens if we have them
        if os.path.exists(TOKENS):
            with open(TOKENS, mode="r") as f:
                tokens = f.read()
            auth_mgr.oauth = OAuth2TokenResponse.parse_raw(tokens)
            await auth_mgr.refresh_tokens()

        # Request new ones if they are not valid
        if not (auth_mgr.xsts_token and auth_mgr.xsts_token.is_valid()):
            auth_url = auth_mgr.generate_authorization_url()
            webbrowser.open(auth_url)
            code = await queue.get()
            await auth_mgr.request_tokens(code)

        with open(TOKENS, mode="w") as f:
            f.write(auth_mgr.oauth.json())


def main():
    global CLIENT_ID, CLIENT_SECRET, TOKENS
    parser = argparse.ArgumentParser(description="Authenticate with XBL")
    parser.add_argument(
        "--tokens",
        "-t",
        default=TOKENS_FILE,
        help=f"Token filepath. Default: '{TOKENS_FILE}'",
    )
    parser.add_argument("--client-id", "-cid", help="OAuth2 Client ID")
    parser.add_argument("--client-secret", "-cs", help="OAuth2 Client Secret")

    args = parser.parse_args()

    # pylint: disable=unused-variable
    CLIENT_ID = args.client_id or os.environ.get("CLIENT_ID", "")
    CLIENT_SECRET = args.client_secret or os.environ.get("CLIENT_SECRET", "")
    TOKENS = args.tokens

    app = web.Application()
    app.add_routes([web.get("/auth/callback", auth_callback)])
    runner = web.AppRunner(app)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, "localhost", 8080)
    loop.run_until_complete(site.start())
    loop.run_until_complete(async_main())


if __name__ == "__main__":
    main()
