#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name="xbox-webapi",
    version="1.1.0",
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
        'xbox.webapi.authentication',
        'xbox.webapi.api.provider'
    ],
    namespace_packages=['xbox'],
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ],
    test_suite="tests",
    install_requires=[
        'requests',
        'python-dateutil',
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
            'pip==9.0.1',
            'bumpversion==0.5.3',
            'wheel==0.30.0',
            'watchdog==0.8.3',
            'flake8==3.5.0',
            'tox==2.9.1',
            'coverage==4.5.1',
            'Sphinx==1.7.1',
            'twine==1.10.0',
            'betamax==0.8.1',
            'pytest==3.4.2',
            'pytest-runner==2.11.1'
        ],
    },
    entry_points={
        'console_scripts': [
            'xbox-authenticate=xbox.webapi.scripts.authenticate:main',
            'xbox-auth-tui=xbox.webapi.scripts.tui:main',
            'xbox-searchlive=xbox.webapi.scripts.search:main'
        ]
    }
)
