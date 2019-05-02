===========
Xbox-WebAPI
===========

.. image:: https://pypip.in/version/xbox-webapi/badge.svg
    :target: https://pypi.python.org/pypi/xbox-webapi/
    :alt: Latest Version

.. image:: https://readthedocs.org/projects/xbox-webapi-python/badge/?version=latest
    :target: http://xbox-webapi-python.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://travis-ci.org/OpenXbox/xbox-webapi-python.svg?branch=master
    :target: https://travis-ci.org/OpenXbox/xbox-webapi-python

.. image:: https://img.shields.io/badge/discord-OpenXbox-blue.svg
    :target: https://openxbox.org/discord
    :alt: Discord chat channel

Xbox-WebAPI is a python library to authenticate with Xbox Live via your Microsoft Account and provides Xbox related Web-API.

Authentication via credentials or tokens is supported, Two-Factor-Authentication ( 2FA ) is also possible.

Dependencies
------------
* Python >= 3.5
* Libraries: requests, demjson, appdirs, urwid

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

  xbox-authenticate --tokens tokens.json --email no@live.com --password abc123

  # NOTE: If no credentials are provided via cmdline, they are requested from stdin
  xbox-authenticate --tokens tokens.json

  # If you have a shell compatible with ncurses, you can use the Terminal UI app
  xbox-auth-ui --tokens tokens.json

Fallback Authentication::

  # In case this authentication flow breaks or you do not trust the code with your credentials..
  # Open the following URL in your web-browser and authenticate
  https://login.live.com/oauth20_authorize.srf?display=touch&scope=service%3A%3Auser.auth.xboxlive.com%3A%3AMBI_SSL&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf&locale=en&response_type=token&client_id=0000000048093EE3

  # Once you finished auth and reached a blank page, copy the redirect url from your browser address-field
  # Execute the script with supplied redirect url
  xbox-auth-via-browser 'https://login.live.com/oauth20_desktop.srf?...access_token=...&refresh_token=...'

Example: Search Xbox Live via cmdline tool::

  # Search Xbox One Catalog
  xbox-searchlive --tokens tokens.json "Some game title"

  # Search Xbox 360 Catalog
  xbox-searchlive --tokens tokens.json -l "Some game title"

API usage::

  import sys

  from xbox.webapi.api.client import XboxLiveClient
  from xbox.webapi.authentication.manager import AuthenticationManager
  from xbox.webapi.common.exceptions import AuthenticationException

  """
  For doing authentication in code, see xbox/webapi/scripts/authenticate.py
  or for OAUTH via web-brower, see xbox/webapi/scripts/browserauth.py
  """

  try:
    auth_mgr = AuthenticationManager.from_file('/path_to/tokens.json')
  except FileNotFoundError as e:
    print(
      'Failed to load tokens from \'{}\'.\n'
      'ERROR: {}'.format(e.filename, e.strerror)
    )
    sys.exit(-1)

  try:
    auth_mgr.authenticate(do_refresh=True)
  except AuthenticationException as e:
    print('Authentication failed! Err: %s' % e)
    sys.exit(-1)

  xbl_client = XboxLiveClient(auth_mgr.userinfo.userhash, auth_mgr.xsts_token.jwt, auth_mgr.userinfo.xuid)

  # Some example API calls

  # Get friendslist
  friendslist = xbl_client.people.get_friends_own()

  # Get presence status (by list of XUID)
  presence = xbl_client.presence.get_presence_batch([12344567687845, 453486346235151])

  # Get messages
  messages = xbl_client.message.get_message_inbox()

  # Get profile by GT
  profile = xbl_client.profile.get_profile_by_gamertag('SomeGamertag')

Screenshots
-----------
Here you can see the Auth TUI (Text user interface):

.. image:: https://raw.githubusercontent.com/OpenXbox/xbox-webapi-python/master/assets/xbox_auth_tui_main.png

.. image:: https://raw.githubusercontent.com/OpenXbox/xbox-webapi-python/master/assets/xbox_auth_tui_2fa.png

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
