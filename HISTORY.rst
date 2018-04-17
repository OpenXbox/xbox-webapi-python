=======
History
=======

1.1.0 (2018-04-17)
------------------

* Auth: Updated 2FA authentication to meet current windows live auth flow
* Auth: Redesigned 2FA authentication procedure
* Auth: Implemented xbox-auth-ui script (xbox.webapi.scripts.tui: urwid terminal ui)
* Auth: For password masking, getpass instead or raw input() is used
* Scripts: Default to appdirs.user_data_dir if no tokenfile provided via cmdline argument (see README)

1.0.9 (2018-03-30)
------------------

* Extend **Gameclips** provider with title id filtering and saved clips
* Add **Screenshots** provider
* Add **Titlehub** provider

1.0.8 (2018-03-29)
------------------

* Added **Userstats** endpoint
* Updated README

1.0.7 (2018-03-28)
------------------

* Support supplying auth credentials via stdin
* Added tests for all endpoints
* Added tests for authentication
* Added **QCS** endpoint
* Added **Profile** endpoint
* Added **Achievements** endpoint
* Added **Usersearch** endpoint
* Added **Gameclips** endpoint
* Added **People** endpoint
* Added **Presence** endpoint
* Added **Message** endpoint
* Removed **Gamerpics** endpoint

1.0.3 - 1.0.6 (2018-03-17)
--------------------------

* Metadata changes

1.0.2 (2018-03-17)
------------------

* More metadata changes, rendering on PyPi is fine now

1.0.1 (2018-03-17)
------------------

* Metadata changes

1.0.0 (2018-03-17)
------------------

* First release on PyPI.
