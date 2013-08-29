#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tests
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.rst and epl-v10.html for details.

import unittest
import os
import re

from noipy import authinfo
from noipy import dnsupdater
from noipy import noipy

class NoipyTest(unittest.TestCase):

    def setUp(self):
        self.test_dir = os.path.join(os.path.expanduser('~'), 'noipy_test')

    def tearDown(self):
        if os.path.exists(self.test_dir):
            os.remove(os.path.join(self.test_dir, dnsupdater.DEFAULT_PLUGIN))
            if not os.path.isdir(self.test_dir):
                os.remove(self.test_dir)
            else:
                os.rmdir(self.test_dir)


    def testGetIP(self):
        ip = noipy.get_ip()
        VALID_IP_REGEX = r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'

        self.assertTrue(re.match(VALID_IP_REGEX, ip), 'get_ip() failed.')

    def testAuthObject(self):
        auth1 = authinfo.ApiAuth('username', 'password')
        auth2 = authinfo.ApiAuth.get_instance(b'dXNlcm5hbWU6cGFzc3dvcmQ=')

        self.assertEqual(auth1, auth2, 'ApiAuth.get_instance fail.')

    def testGetAuthInstance(self):
        auth1 = authinfo.ApiAuth('username', 'password')
        auth2 = authinfo.ApiAuth.get_instance(b'dXNlcm5hbWU6cGFzc3dvcmQ=')

        self.assertEqual(auth1, auth2, 'ApiAuth.get_instance fail.')

    def testStoreAuthInfo(self):
        auth1 = authinfo.ApiAuth('username', 'password')
        authinfo.store(auth1, dnsupdater.DEFAULT_PLUGIN, self.test_dir)
        auth2 = None
        try:
            auth_file = os.path.join(self.test_dir, dnsupdater.DEFAULT_PLUGIN)
            with open(auth_file) as f:
                auth_key = f.read()
                auth2 = authinfo.ApiAuth.get_instance(auth_key.encode('utf-8'))
        except IOError as e:
            self.fail('Store settings function failed. {0}: "{1}"'.format(e.strerror, self.test_dir))

        self.assertTrue(auth1 == auth2, 'Auth information storing failed.')

    def testLoadAuthInfo(self):
        auth1 = authinfo.ApiAuth('username', 'password')
        try:
            os.mkdir(self.test_dir)
            auth_file = os.path.join(self.test_dir, dnsupdater.DEFAULT_PLUGIN)
            with open(auth_file, 'w') as f:
                f.write(auth1.base64key.decode('utf-8'))
        except IOError as e:
            self.fail('Load settings function failed. {0}: "{1}"'.format(e.strerror, self.test_dir))

        auth2 = authinfo.load(dnsupdater.DEFAULT_PLUGIN, self.test_dir)

        self.assertTrue(auth1 == auth2, 'Auth information loading failed.')

    def testStoreAuthInfoAfterUpgradeVersion(self):
        auth1 = authinfo.ApiAuth('username', 'password')
        
        # ealier version settings file
        try:
            with open(self.test_dir, 'w') as f:
                f.write('test')
        except IOError as e:
            self.fail('Store settings function failed. {0}: "{1}"'.format(e.strerror, self.test_dir))

        authinfo.store(auth1, dnsupdater.DEFAULT_PLUGIN, self.test_dir)

        auth2 = None
        try:
            auth_file = os.path.join(self.test_dir, dnsupdater.DEFAULT_PLUGIN)
            with open(auth_file) as f:
                auth_key = f.read()
                auth2 = authinfo.ApiAuth.get_instance(auth_key.encode('utf-8'))
        except IOError as e:
            self.fail('Store settings function failed. {0}: "{1}"'.format(e.strerror, self.test_dir))

        self.assertTrue(auth1 == auth2, 'Auth information storing failed.')

    def testProviderExists(self):
        auth1 = authinfo.ApiAuth('username', 'password')
        authinfo.store(auth1, dnsupdater.DEFAULT_PLUGIN, self.test_dir)
        
        if not authinfo.exists(dnsupdater.DEFAULT_PLUGIN, self.test_dir):
            self.fail('Settings file should be avaliable.')

        if authinfo.exists('fake_provider'):
            self.fail('Temp settings file should NOT be avaliable.')

    def testNoipPlugin(self):
        auth = authinfo.ApiAuth('username', 'password')
        hotsname = 'noipy.no-ip.org'

        plugin = dnsupdater.NoipDnsUpdater(auth, hotsname)
        plugin.update_dns('1.1.1.1')

        self.assertTrue(plugin.status_message.startswith('ERROR: Invalid username or password'), 'Status message should be "Invalid username or password"')

    def testDynDnsPlugin(self):
        auth = authinfo.ApiAuth('username', 'password')
        hotsname = 'noipy.homelinux.com'

        plugin = dnsupdater.DynDnsUpdater(auth, hotsname)
        plugin.update_dns('1.1.1.1')

        self.assertTrue(plugin.status_message.startswith('ERROR: Invalid username or password'), 'Status message should be "Invalid username or password"')

if __name__ == "__main__":
    unittest.main()
