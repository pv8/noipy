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

    def test_get_ip(self):
        ip = noipy.get_ip()
        VALID_IP_REGEX = r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'

        self.assertTrue(re.match(VALID_IP_REGEX, ip), 'get_ip() failed.')

    def test_auth_user_password(self):
        auth1 = authinfo.ApiAuth('username', 'password')
        auth2 = authinfo.ApiAuth.get_instance(b'dXNlcm5hbWU6cGFzc3dvcmQ=')

        self.assertEqual(auth1, auth2, 'ApiAuth.get_instance fail.')

    def test_auth_token(self):
        token = "1234567890ABCDEFG"
        auth1 = authinfo.ApiAuth(usertoken=token)
        auth2 = authinfo.ApiAuth.get_instance(b'MTIzNDU2Nzg5MEFCQ0RFRkc6')

        self.assertEqual(auth1, auth2, 'ApiAuth.get_instance fail for token.')
        self.assertEqual(auth1.token, auth2.token, 'ApiAuth.token fail.')

    def test_store_auth_info(self):
        auth1 = authinfo.ApiAuth('username', 'password')
        authinfo.store(auth1, dnsupdater.DEFAULT_PLUGIN, self.test_dir)
        auth2 = None
        try:
            auth_file = os.path.join(self.test_dir, dnsupdater.DEFAULT_PLUGIN)
            with open(auth_file) as f:
                auth_key = f.read()
                auth2 = authinfo.ApiAuth.get_instance(auth_key.encode('utf-8'))
        except IOError as e:
            self.fail('Store settings function failed. {0}: "{1}"'.format(
                e.strerror, self.test_dir))

        self.assertTrue(auth1 == auth2, 'Auth information storing failed.')

    def test_load_auth_info(self):
        auth1 = authinfo.ApiAuth('username', 'password')
        try:
            os.mkdir(self.test_dir)
            auth_file = os.path.join(self.test_dir, dnsupdater.DEFAULT_PLUGIN)
            with open(auth_file, 'w') as f:
                f.write(auth1.base64key.decode('utf-8'))
        except IOError as e:
            self.fail('Load settings function failed. {0}: "{1}"'.format(
                e.strerror, self.test_dir))

        auth2 = authinfo.load(dnsupdater.DEFAULT_PLUGIN, self.test_dir)

        self.assertTrue(auth1 == auth2, 'Auth information loading failed.')

    def test_store_auth_info_after_upgrade_version(self):
        auth1 = authinfo.ApiAuth('username', 'password')
        
        # ealier version settings file
        try:
            with open(self.test_dir, 'w') as f:
                f.write('test')
        except IOError as e:
            self.fail('Store settings function failed. {0}: "{1}"'.format(
                e.strerror, self.test_dir))

        authinfo.store(auth1, dnsupdater.DEFAULT_PLUGIN, self.test_dir)

        auth2 = None
        try:
            auth_file = os.path.join(self.test_dir, dnsupdater.DEFAULT_PLUGIN)
            with open(auth_file) as f:
                auth_key = f.read()
                auth2 = authinfo.ApiAuth.get_instance(auth_key.encode('utf-8'))
        except IOError as e:
            self.fail('Store settings function failed. {0}: "{1}"'.format(
                e.strerror, self.test_dir))

        self.assertTrue(auth1 == auth2, 'Auth information storing failed.')

    def test_provider_exists(self):
        auth1 = authinfo.ApiAuth('username', 'password')
        authinfo.store(auth1, dnsupdater.DEFAULT_PLUGIN, self.test_dir)
        
        if not authinfo.exists(dnsupdater.DEFAULT_PLUGIN, self.test_dir):
            self.fail('Settings file should be avaliable.')

        if authinfo.exists('fake_provider'):
            self.fail('Temp settings file should NOT be avaliable.')

    def test_noip_plugin(self):
        auth = authinfo.ApiAuth('username', 'password')
        hotsname = 'noipy.no-ip.org'

        plugin = dnsupdater.NoipDnsUpdater(auth, hotsname)
        plugin.update_dns('1.1.1.1')

        self.assertTrue(
            plugin.status_message.startswith('ERROR: Invalid username or password'),
            'Status message should be "Invalid username or password"')

    def test_dyndns_plugin(self):
        auth = authinfo.ApiAuth('username', 'password')
        hotsname = 'noipy.homelinux.com'

        plugin = dnsupdater.DynDnsUpdater(auth, hotsname)
        plugin.update_dns('1.1.1.1')

        self.assertTrue(
            plugin.status_message.startswith("ERROR: Invalid username or password"),
            "Status message should be 'Invalid username or password'")

    def test_duckdns_plugin(self):
        auth = authinfo.ApiAuth(usertoken="1234567890ABCDEFG")
        hotsname = 'duck.dickdns.org'

        plugin = dnsupdater.DuckDnsUpdater(auth, hotsname)
        plugin.update_dns('1.1.1.1')

        self.assertEqual(plugin.status_message,
                         "ERROR: Hostname and/or token incorrect.",
                         "Status message should be 'ERROR: Hostname and/or token incorrect.'")

    def test_not_implemented(self):
        auth = authinfo.ApiAuth('username', 'password')
        hostname = "hostname"
        plugin = dnsupdater.DnsUpdaterPlugin(auth, hostname)
        try:
            plugin.update_dns("1.1.1.1")
            self.fail("_get_base_url() should return NotImplemented")
        except AttributeError as e:
            self.assertTrue(str(e).startswith("'NotImplementedType' object"),
                            "_get_base_url() should return NotImplemented")
        except Exception as e:
            self.fail("_get_base_url() should return NotImplemented. Got %s:%s"
                      % (type(e).__name__, e))

    def test_dns_plugin_status_message(self):
        auth = authinfo.ApiAuth('username', 'password')
        hostname = "hostname"
        plugin = dnsupdater.DnsUpdaterPlugin(auth, hostname)

        # badauth code
        plugin.last_status_code = 'badauth'
        expected_message = "ERROR: Invalid username or password (%s)." \
                           % plugin.last_status_code
        self.assertTrue(plugin.status_message == expected_message,
                        "Expected 'badauth' status code.")

        # good <IP> code
        plugin.last_status_code = 'good 1.1.1.1'
        expected_message = "SUCCESS: DNS hostname IP (1.1.1.1) successfully " \
                           "updated."
        self.assertTrue(plugin.status_message == expected_message,
                        "Expected 'good <1.1.1.1>' status code.")

        # nochg <IP> code
        plugin.last_status_code = 'nochg 1.1.1.1'
        expected_message = "SUCCESS: IP address (1.1.1.1) is up to date, " \
                           "nothing was changed. Additional 'nochg' updates " \
                           "may be considered abusive."
        self.assertTrue(plugin.status_message == expected_message,
                        "Expected 'nochg <1.1.1.1>' status code.")

        # !donator code
        plugin.last_status_code = '!donator'
        expected_message = "ERROR: Update request include a feature that is " \
                           "not available to informed user."
        self.assertTrue(plugin.status_message == expected_message,
                        "Expected '!donator' status code.")

        # notfqdn code
        plugin.last_status_code = 'notfqdn'
        expected_message = "ERROR: The hostname specified is not a " \
                           "fully-qualified domain name (not in the form " \
                           "hostname.dyndns.org or domain.com)."
        self.assertTrue(plugin.status_message == expected_message,
                        "Expected 'notfqdn' status code.")

        # nohost code
        plugin.last_status_code = 'nohost'
        expected_message = "ERROR: Hostname specified does not exist in this " \
                           "user account."
        self.assertTrue(plugin.status_message == expected_message,
                        "Expected 'nohost' status code.")

        # numhost code
        plugin.last_status_code = 'numhost'
        expected_message = "ERROR: Too many hosts (more than 20) specified " \
                           "in an update. Also returned if trying to update " \
                           "a round robin (which is not allowed)."
        self.assertTrue(plugin.status_message == expected_message,
                        "Expected 'numhost' status code.")

        # abuse code
        plugin.last_status_code = 'abuse'
        expected_message = "ERROR: Username/hostname is blocked due to " \
                           "update abuse."
        self.assertTrue(plugin.status_message == expected_message,
                        "Expected 'abuse' status code.")

        # badagent code
        plugin.last_status_code = 'badagent'
        expected_message = "ERROR: User agent not sent or HTTP method not " \
                           "permitted."
        self.assertTrue(plugin.status_message == expected_message,
                        "Expected 'badagent' status code.")

        # dnserr code
        plugin.last_status_code = 'dnserr'
        expected_message = "ERROR: DNS error encountered."
        self.assertTrue(plugin.status_message == expected_message,
                        "Expected 'dnserr' status code.")

        # 911 code
        plugin.last_status_code = '911'
        expected_message = "ERROR: Problem on server side. Retry update in a " \
                           "few minutes."
        self.assertTrue(plugin.status_message == expected_message,
                        "Expected '911' status code.")

        # OK code
        plugin.last_status_code = 'OK'
        expected_message = "SUCCESS: DNS hostname successfully updated."
        self.assertTrue(plugin.status_message == expected_message,
                        "Expected 'OK' status code.")

        # KO code
        plugin.last_status_code = 'KO'
        expected_message = "ERROR: Hostname and/or token incorrect."
        self.assertTrue(plugin.status_message == expected_message,
                        "Expected 'KO' status code.")

        # Unknown code
        plugin.last_status_code = 'UNKNOWN_CODE'
        expected_message = "WARNING: Ooops! Something went wrong !!!"
        self.assertTrue(plugin.status_message == expected_message,
                        "Expected 'Ooops' warning message.")

if __name__ == "__main__":
    unittest.main()
