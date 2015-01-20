#!/usr/bin/env python
# -*- coding: utf-8 -*-

# setup
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.rst and LICENSE for details.

from setuptools import setup, find_packages
from noipy import __version__, __author__, __email__, __license__

lib_dependencies = [
    'requests>=2.0.0',
]

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
    install_requires=lib_dependencies,
    keywords=['no-ip', 'dyndns', 'duckdns', 'ddns', 'api'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: Name Service (DNS)',
    ],
    entry_points={
        'console_scripts': [
            'noipy = noipy.main:main',
        ],
    },
    zip_safe=True,
    test_suite='test.test_noipy'
)
