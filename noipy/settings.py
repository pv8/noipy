#!/usr/bin/env python
# -*- coding: utf-8 -*-

# noipy.settings
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.md and LICENSE.md for details.

import os

# contants
SETTINGS_DIR = os.path.join(os.path.expanduser("~"), '.noipy')
SETTINGS_FILE_NAME = 'settings' 

def load(filename):
    """(str) -> dict of {str: str}
    
    Load update information from settings file and return them
    as a dictionary with keys "username", "password" and "hostname"
    """

    d = {}
    try:
        with open(filename) as f:
            d = dict([line.strip().split('=', 1) for line in f if not line.startswith('#')])
            #for line in f:
            #    tokens = line.strip().split('=', 1)
            #    d[tokens[0]] = '='.join(tokens[1:])
    except IOError as e:
        print '{0}: "{1}"'.format(e.strerror, filename)
        raise e

    return d

def store(info):
    """(dict of {str: str}) -> None
    
    Generate settings file with basic information: "username", 
    "password" and "hostname"
    """

    try:
        # create dir if it does not exist
        if not os.path.exists(SETTINGS_DIR):
            os.makedirs(SETTINGS_DIR)

        settingsfile = os.path.join(SETTINGS_DIR, SETTINGS_FILE_NAME)
        print 'Creating settings file: %s' % settingsfile

        with open(settingsfile, 'w') as f:
            f.write('username=%s\n' % info['username'])
            f.write('password=%s\n' % info['password'])
            f.write('hostname=%s\n' % info['hostname'])

    except IOError as e:
        print '{0}: "{1}"'.format(e.strerror, settingsfile)
        raise e

    print 'Settings file created.'
    
