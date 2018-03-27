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

Authentication via credentials or tokens is supported, Two-Factor-Authentication is also possible.

Dependencies
------------
* Python >= 3.5
* Libraries: requests, python-dateutil, demjson

How to use
----------
Install::

  pip install xbox-webapi

Authentication::

  xbox-authenticate --tokenfile tokens.json --email no@live.com --password abc123

  # If no credentials are provided via mail, they are requested from stdin
  xbox-authenticate --tokenfile tokens.json
  >> Input authentication credentials
  >> Email: <input>
  >> Password: <input>

API usage::

  # Search Xbox One Catalog
  xbox-searchlive --tokenfile tokens.json "Some game title"

  # Search Xbox 360 Catalog
  xbox-searchlive --tokenfile tokens.json -l "Some game title"

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

.. _`joealcorn/xbox`: https://github.com/joealcorn/xbox
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
