#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests',
    'python-dateutil',
    'demjson'
]

setup_requirements = ['pytest-runner']

test_requirements = [
    'pytest',
    'betamax'
]

dev_requirements = [
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
]

setup(
    name="xbox-webapi",
    version="1.0.9",
    author="OpenXbox",
    description="A library to authenticate with Windows Live/Xbox Live and use their API",
    long_description=readme + '\n\n' + history,
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
    install_requires=requirements,
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    extras_require={
        'dev': dev_requirements,
    },
    entry_points={
        'console_scripts': [
            'xbox-authenticate=xbox.webapi.scripts.authenticate:main',
            'xbox-searchlive=xbox.webapi.scripts.search:main'
        ]
    }
)
