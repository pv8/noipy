#!/usr/bin/env python
# -*- coding: utf-8 -*-

# noipy.settings
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.md and LICENSE.md for details.

import os

DEFAULT_FILE_PATH = os.path.join(os.path.expanduser('~'), '.noipy') 

def load(filename):
    """(str) -> dict of {str: str}
    
    Load update information from settings file and return them
    as a dictionary with keys "username", "password" and "hostname"
    """

    info = {}
    try:
        with open(filename) as f:
            info = dict([line.strip().split('=', 1) for line in f if not line.startswith('#')])
            #for line in f:
            #    tokens = line.strip().split('=', 1)
            #    d[tokens[0]] = '='.join(tokens[1:])
    except IOError as e:
        print '{0}: "{1}"'.format(e.strerror, filename)
        raise e

    return info

def store(info, settings_file = DEFAULT_FILE_PATH):
    """(dict of {str: str}, str) -> None
    
    Generate settings_file with basic info: "username", "password" 
    and "hostname" on given path.
    """

    try:
        print 'Creating settings file: %s' % settings_file

        with open(settings_file, 'w') as f:
            f.write('username=%s\n' % info['username'])
            f.write('password=%s\n' % info['password'])
            f.write('hostname=%s\n' % info['hostname'])

    except IOError as e:
        print '{0}: "{1}"'.format(e.strerror, settings_file)
        raise e

    print 'Settings file created.'
    
