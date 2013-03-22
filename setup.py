#!/usr/bin/env python

from setuptools import setup, find_packages
from noipy import __version__, __author__, __email__, __license__

setup(
        name="noipy",
        version=__version__,
        description="Command line update for No-IP DDNS Update API",
        long_description=open('README.md').read(),
        license=__license__,
        author=__author__,
        author_email=__email__,
        url="https://github.com/povieira/noipy",
        packages=find_packages(),
        keywords="no-ip ddns update api",
        zip_safe=True
)
