#!/usr/bin/env python

from setuptools import find_packages, setup

PACKAGES = [f"xbox.{p}" for p in find_packages(where="xbox")]

setup(
    name="xbox-webapi",
    version="2.0.11",
    author="OpenXbox",
    description="A library to authenticate with Windows Live/Xbox Live and use their API",
    long_description=open("README.md").read() + "\n\n" + open("CHANGELOG.md").read(),
    long_description_content_type="text/markdown",
    license="GPL",
    keywords="xbox one live api",
    url="https://github.com/OpenXbox/xbox-webapi-python",
    packages=PACKAGES,
    namespace_packages=["xbox"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    test_suite="tests",
    install_requires=[
        "httpx",
        "appdirs",
        "ms_cv",
        "pydantic",
        "ecdsa",
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov", "respx"],
    extras_require={
        "dev": [
            "pip",
            "bump2version",
            "wheel",
            "watchdog",
            "flake8",
            "tox",
            "coverage",
            "Sphinx",
            "sphinx_rtd_theme",
            "recommonmark",
            "twine",
            "pytest",
            "pytest-cov",
            "pytest-runner",
        ],
    },
    entry_points={
        "console_scripts": [
            "xbox-authenticate=xbox.webapi.scripts.authenticate:main",
            "xbox-searchlive=xbox.webapi.scripts.search:main",
            "xbox-change-gt=xbox.webapi.scripts.change_gamertag:main",
            "xbox-friends=xbox.webapi.scripts.friends:main",
        ]
    },
)
