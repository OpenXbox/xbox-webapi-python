# this is just script from README.md
import sys
import asyncio
from aiohttp import ClientSession
from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.models import OAuth2TokenResponse
from xbox.webapi.common.exceptions import AuthenticationException
from xbox import *
client_id = 'YOUR CLIENT ID HERE'
client_secret = 'YOUR CLIENT SECRET HERE'
"""
For doing authentication, see xbox/webapi/scripts/authenticate.py
"""
async def async_main():
    tokens_file = "./tokens.json" # replace with path in auth scrip or just paste file with tokens here
    async with ClientSession() as session:
        auth_mgr = AuthenticationManager(
              session, client_id, client_secret, ""
        )

        try:
            with open(tokens_file, mode="r") as f:
                  tokens = f.read()
            auth_mgr.oauth = OAuth2TokenResponse.parse_raw(tokens)
        except FileNotFoundError:
            print(f'File {tokens_file} isn`t found or it doesn`t contain tokens!')
            exit(-1)
        
        try:
              await auth_mgr.refresh_tokens()
        except ClientResponseError:
              print("Could not refresh tokens")
              sys.exit(-1)

        with open(tokens_file, mode="w") as f:
              f.write(auth_mgr.oauth.json())
        print(f'Refreshed tokens in {tokens_file}!')

        xbl_client = XboxLiveClient(auth_mgr)

        # Some example API calls
        # Get friendslist
        friendslist = await xbl_client.people.get_friends_own()
        print('Your friends:')
        print(friendslist)
        print()

        # Get presence status (by list of XUID)
        presence = await xbl_client.presence.get_presence_batch(["2533274794093122", "2533274807551369"])
        print('Statuses of some random players by XUID:')
        print(presence)
        print()

        # Get messages
        messages = await xbl_client.message.get_inbox()
        print('Your messages:')
        print(messages)
        print()

        # Get profile by GT
        profile = await xbl_client.profile.get_profile_by_gamertag("SomeGamertag")
        print('Profile under SomeGamertag gamer tag:')
        print(profile)
        print()

asyncio.run(async_main())