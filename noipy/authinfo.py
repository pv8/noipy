#!/usr/bin/env python
# -*- coding: utf-8 -*-

# noipy.authinfo
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.rst and epl-v10.html for details.

import os
import base64

class ApiAuth(object):

    def __init__(self, username, password):
        self._username = username
        self._password = password

    @property
    def base64key(self):
        auth_str = '%s:%s' % (self._username, self._password)
        return base64.b64encode(auth_str.encode('utf-8'))

    @classmethod
    def get_instance(cls, encoded_key):
        """(str) -> ApiAuth
        
        Return an ApiAuth instance from an encoded key
        """
        login_str = base64.b64decode(encoded_key).decode('utf-8')
        username, password = login_str.strip().split(':', 1)

        instance = cls(username, password)

        return instance

    def __str__(self):
        return self.base64key.decode('utf-8')

    def __eq__(self, other):
        return str(self) == str(other)
    

AUTHFILE_DIR = os.path.join(os.path.expanduser('~'), '.noipy')

def store(auth, provider, auth_dir=AUTHFILE_DIR):
    """(ApiAuth, str, str) -> None
    
    Store auth info in file for specified provider
    """

    try:
        if not os.path.exists(auth_dir):
            print('Creating directory: %s' % auth_dir)
            os.mkdir(auth_dir)
        elif not os.path.isdir(auth_dir):
            os.remove(auth_dir)
            print('Creating directory: %s' % auth_dir)
            os.mkdir(auth_dir)

        auth_file = os.path.join(auth_dir, provider)
        print('Creating auth info file: %s' % auth_file)
        with open(auth_file, 'w') as f:
            buff = auth.base64key.decode('utf-8')
            f.write(buff)

    except IOError as e:
        print('{0}: "{1}"'.format(e.strerror, auth_file))
        raise e

    print('Auth info stored')

def load(provider, auth_dir=AUTHFILE_DIR):
    """(str, str) -> ApiAuth
    
    Load provider specific auth info from file
    """

    print('Loading stored auth info...')
    auth = None
    try:
        auth_file = os.path.join(auth_dir, provider)
        with open(auth_file) as f:
            auth_key = f.read()
            auth = ApiAuth.get_instance(auth_key.encode('utf-8'))
    except IOError as e:
        print('{0}: "{1}"'.format(e.strerror, auth_file))
        raise e

    return auth

def exists(provider, auth_dir=AUTHFILE_DIR):
    auth_file = os.path.join(auth_dir, provider)
    return os.path.exists(auth_file)
