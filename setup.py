#!/usr/bin/env python
# -*- coding: utf-8 -*-

# setup
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.md and LICENSE.md for details.

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
        keywords=['no-ip', 'ddns', 'api'],
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Eclipse Public License (EPL)',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
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
