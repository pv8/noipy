#!/usr/bin/env python
# -*- coding: utf-8 -*-

# noipy.settings
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.md and LICENSE.md for details.

import os

DEFAULT_FILE_PATH = os.path.join(os.path.expanduser('~'), '.noipy')

def load(settings_file=DEFAULT_FILE_PATH):
    """(str) -> dict of {str: str}
    
    Load update information from settings file and return them
    as a dictionary with keys "username" and "password"
    """

    info = {}
    try:
        with open(settings_file) as f:
            info = dict([line.strip().split('=', 1) for line in f if not line.startswith('#')])
    except IOError as e:
        print '{0}: "{1}"'.format(e.strerror, settings_file)
        raise e

    return info

def store(auth_info, settings_file=DEFAULT_FILE_PATH):
    """(dict of {str: str}, str) -> None
    
    Create settings_file with basic info: "username" and "password" 
    on given path.
    """

    try:
        print 'Creating settings file: %s' % settings_file

        with open(settings_file, 'w') as f:
            f.write('username=%s\n' % auth_info['username'])
            f.write('password=%s\n' % auth_info['password'])

    except IOError as e:
        print '{0}: "{1}"'.format(e.strerror, settings_file)
        raise e

    print 'Settings file created.'

def file_exists():
    return os.path.exists(DEFAULT_FILE_PATH)
