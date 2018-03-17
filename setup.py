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

test_requirements = [
    'pytest',
    'tox',
    'flake8'
]

setup(
    name="xbox-webapi",
    version="1.0.6",
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
    install_requires=requirements,
    tests_requires=test_requirements,
    test_suite="tests",
    entry_points={
        'console_scripts': [
            'xbox_authenticate=xbox.webapi.scripts.authenticate:main',
            'xbox_searchlive=xbox.webapi.scripts.search:main'
        ]
    }
)
