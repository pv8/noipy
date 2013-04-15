#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tests
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.md and LICENSE.md for details.

import unittest
import os
import re

from noipy import settings
from noipy import dnsupdater

class NoipyTest(unittest.TestCase):

    def setUp(self):
        self.info = {}
        self.info['username'] = 'username'
        self.info['password'] = 'password'
        self.info['hostname'] = 'hostname.no-ip.info'

        self.test_file = 'noipy.test'
        
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def testGetIP(self):
        ip = dnsupdater.get_ip()
        VALID_IP_REGEX = '^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
        self.assertTrue(re.match(VALID_IP_REGEX, ip), 'get_ip() failed.')

    def testStoreSettings(self):

        settings.store(self.info, self.test_file)
        info = {}
        try:
            with open(self.test_file) as f:
                info = dict([line.strip().split('=', 1) for line in f])
        except IOError as e:
            self.fail('Store settings function failed. {0}: "{1}"'.format(e.strerror, self.test_file))

        self.assertTrue(info == self.info, 'Store settings function failed.')

    def testLoadSettings(self):

        try:
            with open(self.test_file, 'w') as f:
                f.write('username=%s\n' % self.info['username'])
                f.write('password=%s\n' % self.info['password'])
                f.write('hostname=%s\n' % self.info['hostname'])
    
        except IOError as e:
            self.fail('Load settings function failed. {0}: "{1}"'.format(e.strerror, self.test_file))

        info = settings.load(self.test_file)

        self.assertTrue(info == self.info, 'Load settings function failed.')

if __name__ == "__main__":
    unittest.main()
