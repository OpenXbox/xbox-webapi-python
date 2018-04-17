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


Xbox-WebAPI is a python library to authenticate with Xbox Live via your Microsoft Account and provides Xbox related Web-API.

Authentication via credentials or tokens is supported, Two-Factor-Authentication ( 2FA ) is also possible.

Dependencies
------------
* Python >= 3.5
* Libraries: requests, python-dateutil, demjson, appdirs, urwid

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

API usage::

  # Search Xbox One Catalog
  xbox-searchlive --tokens tokens.json "Some game title"

  # Search Xbox 360 Catalog
  xbox-searchlive --tokens tokens.json -l "Some game title"

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
