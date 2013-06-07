#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tests
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.md and LICENSE.md for details.

import unittest
import os
import re

from noipy import authinfo
from noipy import dnsupdater
from noipy import noipy

class NoipyTest(unittest.TestCase):

    def setUp(self):
        self.auth = authinfo.ApiAuth('username', 'password')
        self.test_dir = os.path.join(os.path.expanduser('~'), 'noipy_test')

    def tearDown(self):
        if os.path.exists(self.test_dir):
            os.remove(os.path.join(self.test_dir, dnsupdater.DEFAULT_PLUGIN))
            os.rmdir(self.test_dir)

    def testGetIP(self):
        ip = noipy.get_ip()
        VALID_IP_REGEX = '^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'

        self.assertTrue(re.match(VALID_IP_REGEX, ip), 'get_ip() failed.')

    def testGetAuthInstance(self):
        auth1 = authinfo.ApiAuth('username', 'password')
        auth2 = authinfo.ApiAuth.get_instance('dXNlcm5hbWU6cGFzc3dvcmQ=')

        self.assertEqual(auth1, auth2, 'ApiAuth.get_instance fail.')

    def testStoreAuthInfo(self):
        authinfo.store(self.auth, dnsupdater.DEFAULT_PLUGIN, self.test_dir)
        auth = None
        try:
            auth_file = os.path.join(self.test_dir, dnsupdater.DEFAULT_PLUGIN)
            with open(auth_file) as f:
                auth_key = f.read()
                auth = authinfo.ApiAuth.get_instance(auth_key)
        except IOError as e:
            self.fail('Store settings function failed. {0}: "{1}"'.format(e.strerror, self.test_dir))

        self.assertTrue(auth == self.auth, 'Auth information storing failed.')

    def testLoadAuthInfo(self):
        try:
            os.mkdir(self.test_dir)
            auth_file = os.path.join(self.test_dir, dnsupdater.DEFAULT_PLUGIN)
            with open(auth_file, 'w') as f:
                f.write(self.auth.get_base64_key())
        except IOError as e:
            self.fail('Load settings function failed. {0}: "{1}"'.format(e.strerror, self.test_dir))

        auth = authinfo.load(dnsupdater.DEFAULT_PLUGIN, self.test_dir)

        self.assertTrue(auth == self.auth, 'Auth information loading failed.')

if __name__ == "__main__":
    unittest.main()

