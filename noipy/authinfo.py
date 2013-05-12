#!/usr/bin/env python

# noipy.authinfo
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.md for details.

import os
import pickle

class ApiAuth:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def username(self):
        return self.username

    @property
    def password(self):
        return self.password

    def __str__(self):
        return '%s:%s' % (self.username, self.password)


AUTHFILE_DIR = os.path.join(os.path.expanduser('~'), '.noipy')
DEFAULT_FILE_PATH = os.path.join(os.path.expanduser('~'), '.noipy')

def store(auth, path=DEFAULT_FILE_PATH):
    try:
        print 'Creating settings file: %s' % path
        with open(path, 'w') as f:
            pickle.dump(auth, f)

    except IOError as e:
        print '{0}: "{1}"'.format(e.strerror, path)
        raise e

    print 'Auth info stored'

def load(path=DEFAULT_FILE_PATH):
    print 'Loading stored auth info...'
    auth = None
    try:
        auth = pickle.load(path, pickle.HIGHEST_PROTOCOL)
    except IOError as e:
        print '{0}: "{1}"'.format(e.strerror, path)
        raise e

    return auth

def exists():
    return os.path.exists(DEFAULT_FILE_PATH)
