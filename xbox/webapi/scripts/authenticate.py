"""
Example scripts that performs XBL authentication
"""
import asyncio
import os
import webbrowser
from pprint import pprint

from aiohttp import web, ClientSession

from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.api.client import XboxLiveClient

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = "http://localhost:8080/auth/callback"

queue = asyncio.Queue(1)

async def auth_callback(request):
    await queue.put(request.query["code"])
    return web.Response(
        headers={"content-type": "text/html"},
        text="<script>window.close()</script>",
    )

async def main():

    async with ClientSession() as session:
        auth_mgr = AuthenticationManager(session, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
        auth_url = auth_mgr.generate_authorization_url()
        webbrowser.open(auth_url)
        code = await queue.get()
        await auth_mgr.request_tokens(code)

        client = XboxLiveClient(auth_mgr)
        profile = await client.profile.get_profile_by_xuid(client.xuid)

        pprint(await profile.json())


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([web.get('/auth/callback', auth_callback)])
    runner = web.AppRunner(app)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, 'localhost', 8080)
    loop.run_until_complete(site.start())
    loop.run_until_complete(main())
