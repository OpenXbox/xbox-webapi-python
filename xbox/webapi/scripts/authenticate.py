"""
Example scripts that performs XBL authentication
"""
import asyncio
import os
from pprint import pprint
import webbrowser

from aiohttp import ClientSession, web

from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = "http://localhost:8080/auth/callback"

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
        auth_url = auth_mgr.generate_authorization_url()
        webbrowser.open(auth_url)
        code = await queue.get()
        await auth_mgr.request_tokens(code)

        client = XboxLiveClient(auth_mgr)
        # profile = await client.profile.get_profile_by_xuid(client.xuid)
        profile = await client.account.claim_gamertag(client.xuid, "EAppx")

        pprint(profile.status)
        pprint(profile.headers)
        pprint(await profile.text())


def main():
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
