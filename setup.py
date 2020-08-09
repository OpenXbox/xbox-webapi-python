#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="xbox-webapi",
    version="1.1.8",
    author="OpenXbox",
    description="A library to authenticate with Windows Live/Xbox Live and use their API",
    long_description=open('README.rst').read() + '\n\n' + open('HISTORY.rst').read(),
    license="GPL",
    keywords="xbox one live api",
    url="https://github.com/OpenXbox/xbox-webapi-python",
    packages=[
        'xbox.webapi',
        'xbox.webapi.common',
        'xbox.webapi.scripts',
        'xbox.webapi.api',
        'xbox.webapi.api.provider',
        'xbox.webapi.authentication'
    ],
    namespace_packages=['xbox'],
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    test_suite="tests",
    install_requires=[
        'requests',
        'demjson',
        'appdirs',
        'urwid'
    ],
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest',
        'betamax'
    ],
    extras_require={
        'dev': [
            'pip',
            'bump2version',
            'wheel',
            'watchdog',
            'flake8',
            'tox',
            'coverage',
            'Sphinx',
            'twine',
            'betamax',
            'pytest',
            'pytest-runner'
        ],
    },
    entry_points={
        'console_scripts': [
            'xbox-auth-via-browser=xbox.webapi.scripts.browserauth:main',
            'xbox-authenticate=xbox.webapi.scripts.authenticate:main',
            'xbox-auth-tui=xbox.webapi.scripts.tui:main',
            'xbox-searchlive=xbox.webapi.scripts.search:main',
            'xbox-change-gt=xbox.webapi.scripts.change_gamertag:main'
        ]
    }
)
