#!/usr/bin/env python
# -*- coding: utf-8 -*-

# test.test_noipy
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.rst and LICENSE for details.

import getpass
import os
import re
import shutil
import unittest

from noipy import authinfo
from noipy import dnsupdater
from noipy import main
from noipy import utils

VALID_IP_REGEX = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25" \
                 r"[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4]" \
                 r"[0-9]|25[0-5])$"


class SanityTest(unittest.TestCase):

    def setUp(self):
        self.parser = main.create_parser()
        self.test_dir = os.path.join(os.path.expanduser("~"), "noipy_test")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_get_ip(self):
        ip = utils.get_ip()

        self.assertTrue(re.match(VALID_IP_REGEX, ip), "get_ip() failed.")

        # monkey patch for testing (forcing ConnectionError)
        utils.HTTPBIN_URL = "http://example.nothing"

        ip = utils.get_ip()
        self.assertTrue(ip is None, "get_ip() should return None. IP=%s" % ip)

    def test_get_dns_ip(self):
        ip = utils.get_dns_ip("localhost")

        self.assertEqual(ip, "127.0.0.1", "get_dns_ip() failed.")

        ip = utils.get_dns_ip("http://example.nothing")
        self.assertTrue(ip is None, "get_dns_ip() should return None. IP=%s"
                        % ip)


class PluginsTest(unittest.TestCase):

    def setUp(self):
        self.parser = main.create_parser()
        self.test_ip = "10.1.2.3"

    def tearDown(self):
        pass

    def test_instance_str(self):
        plugin = dnsupdater.NoipDnsUpdater(auth=None,
                                           hostname="noipy.no-ip.org")
        self.assertEqual(str(plugin), "NoipDnsUpdater(host=noipy.no-ip.org)")

    def test_noip_plugin(self):
        cmd_args = ["-u", "username", "-p", "password",
                    "--provider", "noip",
                    "-n", "noipy.no-ip.org", self.test_ip]

        args = self.parser.parse_args(cmd_args)
        result = main.execute_update(args)

        self.assertEqual(result.get('exec_result'), main.EXECUTION_RESULT_OK,
                         "Update with 'No-IP' provider failed.")

        # noip.com returns either HTTP 200 or 401,
        # depending on which way the window is blowing
        self.assertTrue(result.get('response_code') in (200, 401),
                        "Invalid response code: %s. Should be 200."
                        % result.get('response_code'))

    def test_dyndns_plugin(self):
        cmd_args = ["-u", "test", "-p", "test",
                    "--provider", "dyn",
                    "-n", "test.dyndns.org", self.test_ip]

        args = self.parser.parse_args(cmd_args)
        result = main.execute_update(args)

        self.assertEqual(result.get('exec_result'), main.EXECUTION_RESULT_OK,
                         "Update with 'DynDNS' provider failed.")

        self.assertEqual(result.get('response_code'), 200,
                         "Invalid response code: %s. Should be 200."
                         % result.get('response_code'))

    def test_duckdns_plugin(self):
        cmd_args = ["-u", "1234567890ABC",
                    "--provider", "duck",
                    "-n", "noipy.duckdns.org", self.test_ip]

        args = self.parser.parse_args(cmd_args)
        result = main.execute_update(args)

        self.assertEqual(result.get('exec_result'), main.EXECUTION_RESULT_OK,
                         "Update with 'DuckDNS' provider failed.")

        self.assertEqual(result.get('response_code'), 200,
                         "Invalid response code: %s. Should be 200."
                         % result.get('response_code'))

    def test_generic_plugin(self):
        cmd_args = ["-u", "username", "-p", "password",
                    "--url", "https://dynupdate.no-ip.com/nic/update",
                    "--provider", "generic",
                    "-n", "noipy.no-ip.org", self.test_ip]

        args = self.parser.parse_args(cmd_args)
        result = main.execute_update(args)

        self.assertEqual(result.get('exec_result'), main.EXECUTION_RESULT_OK,
                         "Update with 'No-IP' using generic provider failed.")

        # noip.com returns either HTTP 200 or 401,
        # depending on which way the window is blowing
        self.assertTrue(result.get('response_code') in (200, 401),
                        "Invalid response code: %s. Should be 200."
                        % result.get('response_code'))

    def test_generic_plugin_malformed_url(self):
        cmd_args = ["-u", "username", "-p", "password",
                    "--url", "abced",
                    "--provider", "generic",
                    "-n", "noipy.no-ip.org", self.test_ip]

        args = self.parser.parse_args(cmd_args)
        result = main.execute_update(args)

        self.assertEqual(result.get('exec_result'), main.EXECUTION_RESULT_NOK,
                         "An error should be flagged when --provider is "
                         "'generic' and URL is malformed.")

        self.assertEqual(result.get('process_message'), "Malformed URL.",
                         "Status message should be an 'Malformed URL.'")

    def test_generic_plugin_without_url(self):
        cmd_args = ["-u", "username", "-p", "password",
                    "--provider", "generic",
                    "-n", "noipy.no-ip.org", self.test_ip]

        args = self.parser.parse_args(cmd_args)
        result = main.execute_update(args)

        self.assertEqual(result.get('exec_result'), main.EXECUTION_RESULT_NOK,
                         "An error should be flagged when --provider is "
                         "'generic' and no URL is provided.")

        self.assertTrue(result.get('process_message')
                        .startswith("Must use --url"),
                        "Status message should start with 'Must use --url'.")


class AuthInfoTest(unittest.TestCase):

    def setUp(self):
        self.parser = main.create_parser()
        self.test_ip = "10.1.2.3"
        self.test_dir = os.path.join(os.path.expanduser("~"), "noipy_test")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            if os.path.isdir(self.test_dir):
                shutil.rmtree(self.test_dir)
            else:
                os.remove(self.test_dir)

    def test_get_instance_password(self):
        auth1 = authinfo.ApiAuth("username", "password")
        auth2 = authinfo.ApiAuth.get_instance(b"dXNlcm5hbWU6cGFzc3dvcmQ=")

        self.assertEqual(auth1, auth2, "ApiAuth.get_instance fail for "
                                       "password.")

    def test_get_token_property_with_password(self):
        auth = authinfo.ApiAuth("username", "password")

        try:
            token = auth.token
            self.fail("A 'NotImplementedError' should be raised. Token=%s" %
                      token)
        except Exception as e:
            if not isinstance(e, NotImplementedError):
                self.fail("A 'NotImplementedError' should be raised. Got: %s"
                          % e)

    def test_get_instance_token(self):
        token = "1234567890ABCDEFG"
        auth1 = authinfo.ApiAuth(usertoken=token)
        auth2 = authinfo.ApiAuth.get_instance(b"MTIzNDU2Nzg5MEFCQ0RFRkc6")

        self.assertEqual(auth1, auth2, "ApiAuth.get_instance fail for token.")
        self.assertEqual(auth1.token, auth2.token, "ApiAuth.token fail.")

    def test_store_from_arguments(self):
        cmd_args = ["--store", "-u", "username", "-p", "password",
                    "--provider", "noip", "-c", self.test_dir]

        # store
        args = self.parser.parse_args(cmd_args)
        result = main.execute_update(args)

        self.assertEqual(result.get('exec_result'), main.EXECUTION_RESULT_OK,
                         "Error storing auth info")

        self.assertEqual(result.get('process_message'), "Auth info stored.",
                         "Status message should be an 'Auth info stored.'")

        # load
        cmd_args = ["--provider", "noip", "-n", "noipy.no-ip.org",
                    "-c", self.test_dir, self.test_ip]
        args = self.parser.parse_args(cmd_args)
        result = main.execute_update(args)

        self.assertEqual(result.get('exec_result'), main.EXECUTION_RESULT_OK,
                         "Error loading auth info")

    def test_store_and_perform_update(self):
        cmd_args = ["--store", "-u", "username", "-p", "password",
                    "--provider", "noip", "-n", "noipy.no-ip.org",
                    "-c", self.test_dir, self.test_ip]

        # store
        args = self.parser.parse_args(cmd_args)
        result = main.execute_update(args)

        self.assertEqual(result.get('exec_result'), main.EXECUTION_RESULT_OK,
                         "Error storing auth info")

        # noip.com returns either HTTP 200 or 401,
        # depending on which way the window is blowing
        self.assertTrue(result.get('response_code') in (200, 401),
                        "Invalid response code: %s. Should be 200."
                        % result.get('response_code'))

    def test_store_from_stdin_input(self):
        cmd_args = ["--store", "--provider", "noip",
                    "-c", self.test_dir]

        # monkey patch for testing
        utils.read_input = lambda _: "username"
        getpass.getpass = lambda _: "password"

        # store
        args = self.parser.parse_args(cmd_args)
        result = main.execute_update(args)

        self.assertEqual(result.get('exec_result'), main.EXECUTION_RESULT_OK,
                         "Error storing auth info")

        self.assertEqual(result.get('process_message'), "Auth info stored.",
                         "Status message should be an 'Auth info stored.'")

        # load
        cmd_args = ["--provider", "noip", "-n", "noipy.no-ip.org",
                    "-c", self.test_dir, self.test_ip]
        args = self.parser.parse_args(cmd_args)
        result = main.execute_update(args)

        self.assertEqual(result.get('exec_result'), main.EXECUTION_RESULT_OK,
                         "Error loading auth info")

    def test_store_pass_from_stdin_input(self):
        cmd_args = ["-u", "username", "--store", "--provider", "noip",
                    "-c", self.test_dir]

        # monkey patch for testing
        getpass.getpass = lambda _: "password"

        # store
        args = self.parser.parse_args(cmd_args)
        result = main.execute_update(args)

        self.assertEqual(result.get('exec_result'), main.EXECUTION_RESULT_OK,
                         "Error storing auth info")

        self.assertEqual(result.get('process_message'), "Auth info stored.",
                         "Status message should be an 'Auth info stored.'")

        # load
        cmd_args = ["--provider", "noip", "-n", "noipy.no-ip.org",
                    "-c", self.test_dir, self.test_ip]
        args = self.parser.parse_args(cmd_args)
        result = main.execute_update(args)

        self.assertEqual(result.get('exec_result'), main.EXECUTION_RESULT_OK,
                         "Error loading auth info")

    def test_store_token_from_stdin_input(self):
        cmd_args = ["--store", "--provider", "duck",
                    "-c", self.test_dir]

        # monkey patch for testing
        utils.read_input = lambda _: "1234567890ABC"

        # store
        args = self.parser.parse_args(cmd_args)
        result = main.execute_update(args)

        self.assertEqual(result.get('exec_result'), main.EXECUTION_RESULT_OK,
                         "Error storing auth info")

        self.assertEqual(result.get('process_message'), "Auth info stored.",
                         "Status message should be an 'Auth info stored.'")

        # load
        cmd_args = ["--provider", "duck", "-n", "noipy.duckdns.org",
                    "-c", self.test_dir, self.test_ip]
        args = self.parser.parse_args(cmd_args)
        result = main.execute_update(args)

        self.assertEqual(result.get('exec_result'), main.EXECUTION_RESULT_OK,
                         "Error loading auth info")

    def test_ioerror(self):
        try:
            auth = authinfo.load(provider="noip",
                                 config_location=self.test_dir)
            self.fail("An 'IOError' should be raised. auth=%s" + auth)
        except Exception as e:
            if not isinstance(e, IOError):
                self.fail("An 'IOError' should be raised. Got: %s" % e)

    def test_update_without_authinfo(self):
        cmd_args = ["--provider", "noip", "-n", "noipy.no-ip.org",
                    "-c", self.test_dir, self.test_ip]

        args = self.parser.parse_args(cmd_args)
        result = main.execute_update(args)

        self.assertEqual(result.get('exec_result'), main.EXECUTION_RESULT_NOK,
                         "Update without auth info failed.")

        self.assertTrue(result.get('process_message').startswith(
            "No stored auth information found for provider:"),
            "Status message should be 'No stored auth information found "
            "for provider: ...'")


class GeneralTest(unittest.TestCase):

    def setUp(self):
        self.parser = main.create_parser()
        self.orig_get_ip = utils.get_ip

    def tearDown(self):
        utils.get_ip = self.orig_get_ip

    def test_cmd_line_no_args(self):
        cmd_args = []

        args = self.parser.parse_args(cmd_args)
        result = main.execute_update(args)

        self.assertEqual(result.get('exec_result'), main.EXECUTION_RESULT_NOK,
                         "Execution without args failed.")

        self.assertTrue(result.get('process_message').startswith(
            "Warning: The hostname to be updated must be provided."),
            "Status message should start with 'Warning: "
            "The hostname to be updated must be provided.'")

    def test_unchanged_ip(self):
        cmd_args = ["-u", "username", "-p", "password",
                    "--url", "https://dynupdate.no-ip.com/nic/update",
                    "--provider", "generic",
                    "-n", "localhost", "127.0.0.1"]

        args = self.parser.parse_args(cmd_args)
        result = main.execute_update(args)

        self.assertEqual(result.get('exec_result'), main.EXECUTION_RESULT_OK,
                         "Update with unchanged IP failed.")

        self.assertEqual(result.get('process_message'), "No update required.",
                         "Status message should be 'No update required'.")

    def test_without_ip(self):
        cmd_args = ["-u", "username", "-p", "password",
                    "--provider", "noip",
                    "-n", "noipy.no-ip.org"]

        # monkey patch for testing
        utils.get_ip = lambda: None

        args = self.parser.parse_args(cmd_args)
        result = main.execute_update(args)

        self.assertEqual(result.get('exec_result'), main.EXECUTION_RESULT_NOK,
                         "Update without IP failed.")

        self.assertTrue(result.get('process_message')
                        .startswith("Unable to get IP address"),
                        "Status message should be 'Unable to get IP address'.")

    def test_not_implemented_plugin(self):
        auth = authinfo.ApiAuth("username", "password")
        hostname = "hostname"
        plugin = dnsupdater.DnsUpdaterPlugin(auth, hostname)
        try:
            plugin.update_dns("10.1.1.1")
            self.fail("Not implemented plugin should fail: "
                      "'NoneType' object has no attribute 'format'")
        except AttributeError as e:
            self.assertEqual(str(e), "'NoneType' object has no attribute "
                                     "'format'",
                             "_get_base_url() should return 'NoneType'")
        except Exception as e:
            self.fail("_get_base_url() should return 'AttributeError'. "
                      "Got %s:%s" % (type(e).__name__, e))

    def test_dns_plugin_status_message(self):
        auth = authinfo.ApiAuth("username", "password")
        hostname = "hostname"
        plugin = dnsupdater.DnsUpdaterPlugin(auth, hostname)

        # badauth code
        plugin.last_ddns_response = "badauth"
        expected_message = "ERROR: Invalid username or password (%s)." \
                           % plugin.last_ddns_response
        self.assertEqual(plugin.status_message, expected_message,
                         "Expected 'badauth' status code.")

        # good <IP> code
        plugin.last_ddns_response = "good 1.1.1.1"
        expected_message = "SUCCESS: DNS hostname IP (1.1.1.1) successfully " \
                           "updated."
        self.assertEqual(plugin.status_message, expected_message,
                         "Expected 'good <1.1.1.1>' status code.")

        # nochg <IP> code
        plugin.last_ddns_response = "nochg 1.1.1.1"
        expected_message = "SUCCESS: IP address (1.1.1.1) is up to date, " \
                           "nothing was changed. Additional 'nochg' updates " \
                           "may be considered abusive."
        self.assertEqual(plugin.status_message, expected_message,
                         "Expected 'nochg <1.1.1.1>' status code.")

        # !donator code
        plugin.last_ddns_response = "!donator"
        expected_message = "ERROR: Update request include a feature that is " \
                           "not available to informed user."
        self.assertEqual(plugin.status_message, expected_message,
                         "Expected '!donator' status code.")

        # notfqdn code
        plugin.last_ddns_response = "notfqdn"
        expected_message = "ERROR: The hostname specified is not a " \
                           "fully-qualified domain name (not in the form " \
                           "hostname.dyndns.org or domain.com)."
        self.assertEqual(plugin.status_message, expected_message,
                         "Expected 'notfqdn' status code.")

        # nohost code
        plugin.last_ddns_response = "nohost"
        expected_message = "ERROR: Hostname specified does not exist in this" \
                           " user account."
        self.assertEqual(plugin.status_message, expected_message,
                         "Expected 'nohost' status code.")

        # numhost code
        plugin.last_ddns_response = "numhost"
        expected_message = "ERROR: Too many hosts (more than 20) specified " \
                           "in an update. Also returned if trying to update " \
                           "a round robin (which is not allowed)."
        self.assertEqual(plugin.status_message, expected_message,
                         "Expected 'numhost' status code.")

        # abuse code
        plugin.last_ddns_response = "abuse"
        expected_message = "ERROR: Username/hostname is blocked due to " \
                           "update abuse."
        self.assertEqual(plugin.status_message, expected_message,
                         "Expected 'abuse' status code.")

        # badagent code
        plugin.last_ddns_response = "badagent"
        expected_message = "ERROR: User agent not sent or HTTP method not " \
                           "permitted."
        self.assertEqual(plugin.status_message, expected_message,
                         "Expected 'badagent' status code.")

        # dnserr code
        plugin.last_ddns_response = "dnserr"
        expected_message = "ERROR: DNS error encountered."
        self.assertEqual(plugin.status_message, expected_message,
                         "Expected 'dnserr' status code.")

        # 911 code
        plugin.last_ddns_response = "911"
        expected_message = "ERROR: Problem on server side. Retry update in a" \
                           " few minutes."
        self.assertEqual(plugin.status_message, expected_message,
                         "Expected '911' status code.")

        # OK code
        plugin.last_ddns_response = "OK"
        expected_message = "SUCCESS: DNS hostname successfully updated."
        self.assertEqual(plugin.status_message, expected_message,
                         "Expected 'OK' status code.")

        # KO code
        plugin.last_ddns_response = "KO"
        expected_message = "ERROR: Hostname and/or token incorrect."
        self.assertEqual(plugin.status_message, expected_message,
                         "Expected 'KO' status code.")

        # Unknown code
        plugin.last_ddns_response = "UNKNOWN_CODE"
        expected_message = "ERROR: Ooops! Something went wrong !!!"
        self.assertEqual(plugin.status_message, expected_message,
                         "Expected 'Ooops' warning message.")

if __name__ == "__main__":
    unittest.main()
