#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tests
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.rst and LICENSE for details.

import unittest
import os
import re
import shutil

from noipy import authinfo
from noipy import dnsupdater
from noipy import main

VALID_IP_REGEX = r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25' \
                 r'[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4]' \
                 r'[0-9]|25[0-5])$'


class SanityTest(unittest.TestCase):

    def setUp(self):
        self.parser = main.create_parser()
        self.test_dir = os.path.join(os.path.expanduser("~"), "noipy_test")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_sanity(self):
        """Tests the sanity of the unit testing framework and if we can
        import all we need to work

        * From https://github.com/rbanffy/testable_appengine (thanks, @rbanffy)
        """
        self.assertTrue(True, "Oops! Sanity test failed! Did we take the"
                              " blue pill?")


class PluginsTest(unittest.TestCase):

    def setUp(self):
        self.parser = main.create_parser()

    def tearDown(self):
        pass

    def test_noip_plugin(self):
        cmd_args = ['-u', 'username', '-p', 'password',
                    '-n', 'noipy.no-ip.org', '1.1.1.1']

        args = self.parser.parse_args(cmd_args)
        result, status_message = main.execute_update(args)

        self.assertTrue(result == main.EXECUTION_RESULT_OK,
                        "Result code should be %s " %
                        main.EXECUTION_RESULT_OK)

        self.assertTrue(status_message.startswith("ERROR:"),
                        "Status message should be an 'ERROR'")

    def test_dyndns_plugin(self):
        cmd_args = ['-u', 'username', '-p', 'password',
                    '-n', 'noipy.homelinux.com', '1.1.1.1']

        args = self.parser.parse_args(cmd_args)
        result, status_message = main.execute_update(args)

        self.assertTrue(result == main.EXECUTION_RESULT_OK,
                        "Result code should be %s " %
                        main.EXECUTION_RESULT_OK)

        self.assertTrue(status_message.startswith("ERROR:"),
                        "Status message should be an 'ERROR'")

    def test_duckdns_plugin(self):
        cmd_args = ['-u', '1234567890ABC',
                    '-n', 'noipy.duckdns.org', '1.1.1.1']

        args = self.parser.parse_args(cmd_args)
        result, status_message = main.execute_update(args)

        self.assertTrue(result == main.EXECUTION_RESULT_OK,
                        "Result code should be %s " %
                        main.EXECUTION_RESULT_OK)

        self.assertTrue(status_message.startswith("ERROR:"),
                        "Status message should be an 'ERROR'")


class AuthInfoTest(unittest.TestCase):

    def setUp(self):
        self.parser = main.create_parser()
        self.test_dir = os.path.join(os.path.expanduser("~"), "noipy_test")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_auth_get_instance_password(self):
        auth1 = authinfo.ApiAuth("username", "password")
        auth2 = authinfo.ApiAuth.get_instance(b"dXNlcm5hbWU6cGFzc3dvcmQ=")

        self.assertEqual(auth1, auth2, "ApiAuth.get_instance fail for "
                                       "password.")

    def test_auth_get_instance_token(self):
        token = "1234567890ABCDEFG"
        auth1 = authinfo.ApiAuth(usertoken=token)
        auth2 = authinfo.ApiAuth.get_instance(b"MTIzNDU2Nzg5MEFCQ0RFRkc6")

        self.assertEqual(auth1, auth2, 'ApiAuth.get_instance fail for token.')
        self.assertEqual(auth1.token, auth2.token, 'ApiAuth.token fail.')

    def test_store_and_load_auth_info(self):
        cmd_args = ['--store', '-u', 'username', '-p', 'password',
                    '--provider', 'noip', '-c', self.test_dir]

        # store
        args = self.parser.parse_args(cmd_args)
        result, status_message = main.execute_update(args)

        self.assertTrue(result == main.EXECUTION_RESULT_OK,
                        "Result code should be %s " %
                        main.EXECUTION_RESULT_OK)

        self.assertTrue(status_message == "Auth info stored.",
                        "Status message should be an 'Auth info stored.'")
        # load
        cmd_args = ['--provider', 'noip', '-n', 'noipy.no-ip.org',
                    '-c', self.test_dir]
        args = self.parser.parse_args(cmd_args)
        result, status_message = main.execute_update(args)

        self.assertTrue(result == main.EXECUTION_RESULT_OK,
                        "Result code should be %s " %
                        main.EXECUTION_RESULT_OK)


class GeneralTest(unittest.TestCase):

    def setUp(self):
        self.parser = main.create_parser()

    def tearDown(self):
        pass

    def test_cmd_line_no_args(self):
        cmd_args = []

        args = self.parser.parse_args(cmd_args)
        result, status_message = main.execute_update(args)

        self.assertTrue(result == main.EXECUTION_RESULT_NOK,
                        "Result code should be %s " %
                        main.EXECUTION_RESULT_NOK)

        self.assertTrue(
            status_message.startswith("Warning: The hostname to be updated "
                                      "must be provided."),
            "Status message should start with 'Warning: The hostname to be "
            "updated must be provided.'")

    def test_get_ip(self):
        ip = main.get_ip()

        self.assertTrue(re.match(VALID_IP_REGEX, ip), 'get_ip() failed.')

    def test_not_implemented_plugin(self):
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
        expected_message = "ERROR: Hostname specified does not exist in this" \
                           " user account."
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
        expected_message = "ERROR: Problem on server side. Retry update in a" \
                           " few minutes."
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
