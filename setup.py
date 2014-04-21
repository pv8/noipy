#!/usr/bin/env python
# -*- coding: utf-8 -*-

# setup
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.rst and epl-v10.html for details.

from setuptools import setup, find_packages
from noipy import __version__, __author__, __email__, __license__

with open('README.rst') as f:
    readme = f.read()
with open('CHANGELOG.rst') as f:
    changelog = f.read()

setup(
        name='noipy',
        version=__version__,
        description='Command line update for No-IP and Dyn DDNS Update API',
        long_description=readme + '\n\n' + changelog,
        license=__license__,
        author=__author__,
        author_email=__email__,
        url='https://github.com/povieira/noipy',
        packages=find_packages(),
        keywords=['no-ip', 'dyndns', 'duckdns', 'ddns', 'api'],
        platforms='Python 2.7 and later',
        classifiers = [
            'Development Status :: 5 - Production/Stable',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Topic :: Internet :: Name Service (DNS)',
        ],
        entry_points={
            'console_scripts': [
                    'noipy = noipy.noipy:main',
            ],
        },
        zip_safe=True,
        test_suite='test.test_noipy'
)
