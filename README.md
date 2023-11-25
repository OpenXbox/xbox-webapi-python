# Xbox-WebAPI

[![PyPi - latest](https://img.shields.io/pypi/v/xbox-webapi.svg)](https://pypi.python.org/pypi/xbox-webapi/)
[![Documentation status](https://readthedocs.org/projects/xbox-webapi-python/badge/?version=latest)](http://xbox-webapi-python.readthedocs.io/en/latest/?badge=latest)
[![Build status](https://img.shields.io/github/actions/workflow/status/OpenXbox/xbox-webapi-python/build.yml?branch=master)](https://github.com/OpenXbox/xbox-webapi-python/actions?query=workflow%3Abuild)
[![Discord chat channel](https://img.shields.io/badge/discord-OpenXbox-blue.svg)](https://openxbox.org/discord)

Xbox-WebAPI is a python library to authenticate with Xbox Live via your Microsoft Account and provides Xbox related Web-API.

Authentication is supported via OAuth2.

- Register a new application in [Azure AD](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade)
  - Name your app
  - Select "Personal Microsoft accounts only" under supported account types
  - Add <http://localhost/auth/callback> as a Redirect URI of type "Web"
- Copy your Application (client) ID for later use
- On the App Page, navigate to "Certificates & secrets"
  - Generate a new client secret and save for later use

## Dependencies

- Python >= 3.8

## How to use

Install

```text
pip install xbox-webapi
```

Authentication

**Note: You must use non child account (> 18 years old)**

Token save location: If tokenfile is not provided via cmdline, fallback of `<appdirs.user_data_dir>/tokens.json` is used as save-location

Specifically:

Windows: `C:\\Users\\<username>\\AppData\\Local\\OpenXbox\\xbox`

Mac OSX: `/Users/<username>/Library/Application Support/xbox/tokens.json`

Linux: `/home/<username>/.local/share/xbox`

For more information, see: <https://pypi.org/project/appdirs> and module: `xbox.webapi.scripts.constants`

```
xbox-authenticate --client-id <client-id> --client-secret <client-secret>
```

Example: Search Xbox Live via cmdline tool

```text
  # Search Xbox One Catalog
  xbox-searchlive "Some game title"
```

API usage

```py
import asyncio
import sys

from httpx import HTTPStatusError

from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.models import OAuth2TokenResponse
from xbox.webapi.common.signed_session import SignedSession
from xbox.webapi.scripts import CLIENT_ID, CLIENT_SECRET, TOKENS_FILE

"""
This uses the global default client identification by OpenXbox
You can supply your own parameters here if you are permitted to create
new Microsoft OAuth Apps and know what you are doing
"""
client_id = CLIENT_ID
client_secret = CLIENT_SECRET
tokens_file = TOKENS_FILE

"""
For doing authentication, see xbox/webapi/scripts/authenticate.py
"""


async def async_main():
    # Create a HTTP client session
    async with SignedSession() as session:
        """
        Initialize with global OAUTH parameters from above
        """
        auth_mgr = AuthenticationManager(session, client_id, client_secret, "")

        """
        Read in tokens that you received from the `xbox-authenticate`-script previously
        See `xbox/webapi/scripts/authenticate.py`
        """
        try:
            with open(tokens_file) as f:
                tokens = f.read()
            # Assign gathered tokens
            auth_mgr.oauth = OAuth2TokenResponse.model_validate_json(tokens)
        except FileNotFoundError as e:
            print(
                f"File {tokens_file} isn`t found or it doesn`t contain tokens! err={e}"
            )
            print("Authorizing via OAUTH")
            url = auth_mgr.generate_authorization_url()
            print(f"Auth via URL: {url}")
            authorization_code = input("Enter authorization code> ")
            tokens = await auth_mgr.request_oauth_token(authorization_code)
            auth_mgr.oauth = tokens

        """
        Refresh tokens, just in case
        You could also manually check the token lifetimes and just refresh them
        if they are close to expiry
        """
        try:
            await auth_mgr.refresh_tokens()
        except HTTPStatusError as e:
            print(
                f"""
                Could not refresh tokens from {tokens_file}, err={e}\n
                You might have to delete the tokens file and re-authenticate 
                if refresh token is expired
            """
            )
            sys.exit(-1)

        # Save the refreshed/updated tokens
        with open(tokens_file, mode="w") as f:
            f.write(auth_mgr.oauth.json())
        print(f"Refreshed tokens in {tokens_file}!")

        """
        Construct the Xbox API client from AuthenticationManager instance
        """
        xbl_client = XboxLiveClient(auth_mgr)

        """
        Some example API calls
        """
        # Get friendslist
        friendslist = await xbl_client.people.get_friends_own()
        print(f"Your friends: {friendslist}\n")

        # Get presence status (by list of XUID)
        presence = await xbl_client.presence.get_presence_batch(
            ["2533274794093122", "2533274807551369"]
        )
        print(f"Statuses of some random players by XUID: {presence}\n")

        # Get messages
        messages = await xbl_client.message.get_inbox()
        print(f"Your messages: {messages}\n")

        # Get profile by GT
        profile = await xbl_client.profile.get_profile_by_gamertag("SomeGamertag")
        print(f"Profile under SomeGamertag gamer tag: {profile}\n")


asyncio.run(async_main())
```

## Contribute

- Report bugs/suggest features
- Add/update docs
- Add additional xbox live endpoints

## Credits

This package uses parts of [Cookiecutter](https://github.com/audreyr/cookiecutter)
and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
The authentication code is based on [joealcorn/xbox](https://github.com/joealcorn/xbox)

Informations on endpoints gathered from:

- [XboxLive REST Reference](https://docs.microsoft.com/en-us/windows/uwp/xbox-live/xbox-live-rest/atoc-xboxlivews-reference)
- [XboxLiveTraceAnalyzer APIMap](https://github.com/Microsoft/xbox-live-trace-analyzer/blob/master/Source/XboxLiveTraceAnalyzer.APIMap.csv)
- [Xbox Live Service API](https://github.com/Microsoft/xbox-live-api)

## Disclaimer

Xbox, Xbox One, Smartglass and Xbox Live are trademarks of Microsoft Corporation. Team OpenXbox is in no way endorsed by or affiliated with Microsoft Corporation, or any associated subsidiaries, logos or trademarks.
