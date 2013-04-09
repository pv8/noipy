#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from noipy import __version__, __author__, __email__, __license__

setup(
        name='noipy',
        version=__version__,
        description='Command line update for No-IP DDNS Update API',
        long_description=open('README.md').read(),
        license=__license__,
        author=__author__,
        author_email=__email__,
        url='https://github.com/povieira/noipy',
        packages=find_packages(),
        keywords='no-ip ddns update api',
        entry_points={
            'console_scripts': [
                    'noipy = noipy.dnsupdater:main',
            ],
        },
        zip_safe=True
)
