#!/usr/bin/env python
# -*- coding: utf-8 -*-

# noipy.authinfo
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.rst and LICENSE for details.

from __future__ import print_function

import os
import base64

NOIPY_CONFIG = ".noipy"
DEFAULT_CONFIG_DIR = os.path.expanduser("~")


class ApiAuth(object):
    """ Providers auth information """

    def __init__(self, usertoken, password=""):
        self._usertoken = usertoken
        self._password = password

    @property
    def token(self):
        if self._password != "":
            raise NotImplementedError
        return self._usertoken

    @property
    def base64key(self):
        auth_str = '%s:%s' % (self._usertoken, self._password)
        return base64.b64encode(auth_str.encode('utf-8'))

    @classmethod
    def get_instance(cls, encoded_key):
        """Return an ApiAuth instance from an encoded key """

        login_str = base64.b64decode(encoded_key).decode('utf-8')
        usertoken, password = login_str.strip().split(':', 1)

        instance = cls(usertoken, password)

        return instance

    def __str__(self):
        return self.base64key.decode('utf-8')

    def __eq__(self, other):
        return str(self) == str(other)


def store(auth, provider, config_location=DEFAULT_CONFIG_DIR):
    """Store auth info in file for specified provider """

    auth_file = None
    try:
        # only for custom locations
        if not os.path.exists(config_location):
            print("Creating custom config directory [%s]... "
                  % config_location, end="")
            os.mkdir(config_location)
            print("OK.")

        config_dir = os.path.join(config_location, NOIPY_CONFIG)
        if not os.path.exists(config_dir):
            print("Creating directory [%s]... " % config_dir, end="")
            os.mkdir(config_dir)
            print("OK.")
        elif not os.path.isdir(config_dir):
            os.remove(config_dir)
            print("Creating directory [%s]... " % config_dir, end="")
            os.mkdir(config_dir)
            print("OK.")

        auth_file = os.path.join(config_dir, provider)
        print("Creating auth info file [%s]... " % auth_file, end="")
        with open(auth_file, 'w') as f:
            buff = auth.base64key.decode('utf-8')
            f.write(buff)
        print("OK.")

    except IOError as e:
        print('{0}: "{1}"'.format(e.strerror, auth_file))
        raise e


def load(provider, config_location=DEFAULT_CONFIG_DIR):
    """Load provider specific auth info from file """

    auth = None
    auth_file = None
    try:
        config_dir = os.path.join(config_location, NOIPY_CONFIG)
        print("Loading stored auth info [%s]... " % config_dir, end="")
        auth_file = os.path.join(config_dir, provider)
        with open(auth_file) as f:
            auth_key = f.read()
            auth = ApiAuth.get_instance(auth_key.encode('utf-8'))
        print("OK.")
    except IOError as e:
        print('{0}: "{1}"'.format(e.strerror, auth_file))
        raise e

    return auth


def exists(provider, config_location=DEFAULT_CONFIG_DIR):
    """Check whether provider info is already stored """

    config_dir = os.path.join(config_location, NOIPY_CONFIG)
    auth_file = os.path.join(config_dir, provider)
    return os.path.exists(auth_file)
