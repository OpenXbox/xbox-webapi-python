# Changelog

## 2.0.10 (2020-11-13)

* Add models for XAD and XAT Token responses
* Fix message.get_inbox() (Setting text field as Optional) (Fixes issue #37)
* Fix OAuth2TokenResponse incase no refresh_token is returned by authentication (Fixes issue #36)
* Fix pytest warnings (unclosed ClientSession, usage of deprecated ClientResponse field)
* Fix CatalogResponse.Products[].DisplaySkuAvailabilities[].Availabilities - Set order_management_data as Optional
* Enable passing extra values to headers, params and data for all providers via kwargs (extra_headers, extra_params, extra_data)
* Fix GameclipsResponse

## 2.0.9 (2020-11-02)

* Fix titlehub endpoint
* AuthenticationManager: Allow fetching title endpoints
* RequestSigner: Extend to respect SigningPolicy

## 2.0.8 (2020-10-14)

* GH action: Use official docker setup-buildx-step
* Make more CatalogResponse fields optional
* Allow fetching all installed apps across devices (remove device_id requirement)

## 2.0.7 (2020-10-12)

* Fix broken 2.0.6 yarl dep
* Change GitHub action to not deploy on failed build

## 2.0.6 (2020-10-12)

* Add constants for some system titles that do not have PFN in catalog

## 2.0.5 (2020-10-12)

* Fix catalog models for legacy products

## 2.0.4 (2020-10-11)

* Fix catalog fields template

## 2.0.3 (2020-10-11)

* Fix catalog alt id lookup

## 2.0.2 (2020-10-11)

* Fixed package includes for providers
* No longer attempts to refresh tokens when no auth required
* Fixed `xbox-searchlive`

## 2.0.1 (2020-10-10)

* Ensures token validity on every request

## 2.0.0 (2020-10-10)

* Major rewrite (thx @hunterjm)
* Removed auth-TUI (text user interface)
* async via aiohttp
* Support full OAUTH2 flow
* Add new smartglass endpoint (xccs.xboxlive.com)
* Add new catalog endpoint (displaycatalog)
* Easier tests (ditch betamax)
* Add RequestSigner / SignedSession (thx @socram8888)

## 1.1.8 (2020-02-29)

* Update people.py - Added get friends by XUID
* CI / metadata changes

## 1.1.7 (2018-11-10)

* Fix parsing of WindowsLive auth response

## 1.1.6 (2018-09-30)

* Consider (User-)privileges of (XSTS) userinfo optional
* Fix: Always return bool for @Property AuthenticationManager.authenticated

## 1.1.5 (2018-08-11)

* Make property *authenticated* in AuthenticationManager check token validity
* Break out of windows live auth early if cookies were cached previously

## 1.1.4 (2018-07-01)

* Implement convenience functions for Partner Service Authentication

## 1.1.3 (2018-06-16)

* Gracefully fail on wrong account password
* Fix "ValueError: tui: Unexpected button pressed: Cancel"
* provider.lists: Correct headers, GET list works
* Titlehub: Support getting title history by xuid

## 1.1.2 (2018-05-06)

* Fixing appdir (aka. token save location) creation on windows

## 1.1.1 (2018-05-03)

* Removed python-dateutil dependency
* Add auth-via-browser fallback script
* Small changes

## 1.1.0 (2018-04-17)

* Auth: Updated 2FA authentication to meet current windows live auth flow
* Auth: Redesigned 2FA authentication procedure
* Auth: Implemented xbox-auth-ui script (xbox.webapi.scripts.tui: urwid terminal ui)
* Auth: For password masking, getpass instead or raw input() is used
* Scripts: Default to appdirs.user_data_dir if no tokenfile provided via cmdline argument (see README)

## 1.0.9 (2018-03-30)

* Extend **Gameclips** provider with title id filtering and saved clips
* Add **Screenshots** provider
* Add **Titlehub** provider

## 1.0.8 (2018-03-29)

* Added **Userstats** endpoint
* Updated README

## 1.0.7 (2018-03-28)

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

## 1.0.3 - 1.0.6 (2018-03-17)

* Metadata changes

## 1.0.2 (2018-03-17)

* More metadata changes, rendering on PyPi is fine now

## 1.0.1 (2018-03-17)

* Metadata changes

## 1.0.0 (2018-03-17)

* First release on PyPI.
