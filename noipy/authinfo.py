#!/usr/bin/env python
# -*- coding: utf-8 -*-

# noipy.authinfo
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.md and LICENSE.md for details.

import os
import base64

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

    @classmethod
    def get_instance(cls, encoded_key):
        """(str) -> ApiAuth
        
        Return an ApiAuth instance from an encoded key
        """
        login_str = base64.b64decode(encoded_key)
        username, password = login_str.strip().split(':', 1)

        return cls(username, password)

    def get_base64_key(self):
        return base64.b64encode('%s:%s' % (self.username, self.password))

    def __str__(self):
        return '%s:%s' % (self.username, self.password)

    def __eq__(self, other):
        return str(self) == str(other)


AUTHFILE_DIR = os.path.join(os.path.expanduser('~'), '.noipy')

def store(auth, provider, auth_dir=AUTHFILE_DIR):
    """(ApiAuth, str, str) -> None
    
    Store auth info in file for specified provider
    """

    try:
        if not os.path.exists(auth_dir):
            print 'Creating directory: %s' % auth_dir
            os.mkdir(auth_dir)
        elif not os.path.isdir(auth_dir):
            os.remove(auth_dir)
            print 'Creating directory: %s' % auth_dir
            os.mkdir(auth_dir)

        auth_file = os.path.join(auth_dir, provider)
        print 'Creating auth info file: %s' % auth_file
        with open(auth_file, 'w') as f:
            f.write(auth.get_base64_key())

    except IOError as e:
        print '{0}: "{1}"'.format(e.strerror, auth_file)
        raise e

    print 'Auth info stored'

def load(provider, auth_dir=AUTHFILE_DIR):
    """(str, str) -> ApiAuth
    
    Load provider specific auth info from file
    """

    print 'Loading stored auth info...'
    auth = None
    try:
        auth_file = os.path.join(auth_dir, provider)
        with open(auth_file) as f:
            auth_key = f.read()
            auth = ApiAuth.get_instance(auth_key)
    except IOError as e:
        print '{0}: "{1}"'.format(e.strerror, auth_file)
        raise e

    return auth

def exists(provider):
    auth_file = os.path.join(AUTHFILE_DIR, provider)
    return os.path.exists(auth_file)
