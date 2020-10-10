===========
Xbox-WebAPI
===========

.. image:: https://pypip.in/version/xbox-webapi/badge.svg
    :target: https://pypi.python.org/pypi/xbox-webapi/
    :alt: Latest Version

.. image:: https://readthedocs.org/projects/xbox-webapi-python/badge/?version=latest
    :target: http://xbox-webapi-python.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/github/workflow/status/OpenXbox/xbox-webapi-python/build?label=build
    :target: https://github.com/OpenXbox/xbox-webapi-python/actions?query=workflow%3Abuild
    :alt: Build status

.. image:: https://img.shields.io/badge/discord-OpenXbox-blue.svg
    :target: https://openxbox.org/discord
    :alt: Discord chat channel

Xbox-WebAPI is a python library to authenticate with Xbox Live via your Microsoft Account and provides Xbox related Web-API.

Authentication is supported via OAuth2.

#. Register a new application in `Azure AD <https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade>`_
    #. Name your app
    #. Select "Personal Microsoft accounts only" under supported account types
    #. Add http://localhost/auth/callback as a Redirect URI of type "Web"
#. Copy your Application (client) ID for later use
#. On the App Page, navigate to "Certificates & secrets"
    #. Generate a new client secret and save for later use

Dependencies
------------
* Python >= 3.6
* Libraries: aiohttp, appdirs, ms_cv, pydantic, urwid, yarl, ecdsa

How to use
----------
Install::

  pip install xbox-webapi

Authentication::

  # Token save location: If tokenfile is not provided via cmdline, fallback
  # of <appdirs.user_data_dir>/tokens.json is used as save-location
  #
  # Specifically:
  # Windows: C:\\Users\\<username>\\AppData\\Local\\OpenXbox\\xbox
  # Mac OSX: /Users/<username>/Library/Application Support/xbox/tokens.json
  # Linux: /home/<username>/.local/share/xbox
  #
  # For more information, see: https://pypi.org/project/appdirs and module: xbox.webapi.scripts.constants

  xbox-authenticate --client-id <client-id> --client-secret <client-secret>

Example: Search Xbox Live via cmdline tool::

  # Search Xbox One Catalog
  xbox-searchlive "Some game title"

API usage::

  import sys

  from xbox.webapi.api.client import XboxLiveClient
  from xbox.webapi.authentication.manager import AuthenticationManager
  from xbox.webapi.common.exceptions import AuthenticationException

  """
  For doing authentication, see xbox/webapi/scripts/authenticate.py
  """

  tokens = "/path_to/tokens.json"
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

      # Some example API calls

      # Get friendslist
      friendslist = await xbl_client.people.get_friends_own()

      # Get presence status (by list of XUID)
      presence = await xbl_client.presence.get_presence_batch(["12344567687845", "453486346235151"])

      # Get messages
      messages = await xbl_client.message.get_inbox()

      # Get profile by GT
      profile = await xbl_client.profile.get_profile_by_gamertag("SomeGamertag")

Known issues
------------
* There are a lot of missing XBL endpoints

Contribute
----------
* Report bugs/suggest features
* Add/update docs
* Add additional xbox live endpoints

Credits
-------
This package uses parts of Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.
The authentication code is based on `joealcorn/xbox`_

Informations on endpoints gathered from:

* `XboxLive REST Reference`_
* `XboxLiveTraceAnalyzer APIMap`_
* `Xbox Live Service API`_

.. _`joealcorn/xbox`: https://github.com/joealcorn/xbox
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`XboxLive REST Reference`: https://docs.microsoft.com/en-us/windows/uwp/xbox-live/xbox-live-rest/atoc-xboxlivews-reference
.. _`XboxLiveTraceAnalyzer APIMap`: https://github.com/Microsoft/xbox-live-trace-analyzer/blob/master/Source/XboxLiveTraceAnalyzer.APIMap.csv
.. _`Xbox Live Service API`: https://github.com/Microsoft/xbox-live-api

Disclaimer
----------
Xbox, Xbox One, Smartglass and Xbox Live are trademarks of Microsoft Corporation. Team OpenXbox is in no way endorsed by or affiliated with Microsoft Corporation, or any associated subsidiaries, logos or trademarks.
