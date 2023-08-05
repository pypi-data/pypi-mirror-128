#!/usr/bin/env python3

import pathlib
from setuptools import setup

CWD = pathlib.Path(__file__).parent
README = (CWD / "README.md").read_text()

setup(
    name="ungi_utils",
    version="0.0.4",
    description="Utils needed for ungi bots and the cli app",
    long_description=README,
    author="Unseen Giants",
    license="GPL 3.0",
    packages=["ungi_utils"],
    install_requires=["elasticsearch", "aiohttp", "requests"],
    author_email="incoming+unseen-giants-ungi-utils-26498131-issue-@incoming.gitlab.com",
    )
