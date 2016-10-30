#!/usr/bin/env python
# -*- coding: utf-8 -*-

# noipy.noipy
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.rst and LICENSE for details.

from __future__ import print_function

import argparse
import getpass
import re
import sys

from noipy import utils


from noipy import dnsupdater
from noipy import authinfo
from noipy import __version__


EXECUTION_RESULT_OK = 0
EXECUTION_RESULT_NOK = 1

URL_RE = re.compile(
    r'^https?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
    r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def execute_update(args):
    """Execute the update based on command line args and returns a dictionary
    with 'execution result, ''response code', 'response info' and
    'process friendly message'.
    """

    provider_class = getattr(dnsupdater,
                             dnsupdater.AVAILABLE_PLUGINS.get(args.provider))
    updater_options = {}
    process_message = None
    auth = None

    if args.store:  # --store argument
        if provider_class.auth_type == 'T':
            user_arg = args.usertoken or utils.read_input(
                "Paste your auth token: ")
            auth = authinfo.ApiAuth(usertoken=user_arg)
        else:
            user_arg = args.usertoken or utils.read_input(
                "Type your username: ")
            pass_arg = args.password or getpass.getpass("Type your password: ")
            auth = authinfo.ApiAuth(user_arg, pass_arg)

        authinfo.store(auth, args.provider, args.config)
        exec_result = EXECUTION_RESULT_OK
        if not args.hostname:
            update_ddns = False
            process_message = "Auth info stored."
        else:
            update_ddns = True

    # informations arguments
    elif args.usertoken and args.hostname:
        if provider_class.auth_type == 'T':
            auth = authinfo.ApiAuth(args.usertoken)
        else:
            auth = authinfo.ApiAuth(args.usertoken, args.password)
        update_ddns = True
        exec_result = EXECUTION_RESULT_OK
    elif args.hostname:
        if authinfo.exists(args.provider, args.config):
            auth = authinfo.load(args.provider, args.config)
            update_ddns = True
            exec_result = EXECUTION_RESULT_OK
        else:
            update_ddns = False
            exec_result = EXECUTION_RESULT_NOK
            process_message = "No stored auth information found for " \
                              "provider: '%s'" % args.provider
    else:  # no arguments
        update_ddns = False
        exec_result = EXECUTION_RESULT_NOK
        process_message = "Warning: The hostname to be updated must be " \
                          "provided.\nUsertoken and password can be either " \
                          "provided via command line or stored with --store " \
                          "option.\nExecute noipy --help for more details."

    if update_ddns and args.provider == 'generic':
        if args.url:
            if not URL_RE.match(args.url):
                process_message = "Malformed URL."
                exec_result = EXECUTION_RESULT_NOK
                update_ddns = False
            else:
                updater_options['url'] = args.url
        else:
            process_message = "Must use --url if --provider is 'generic' " \
                              "(default)"
            exec_result = EXECUTION_RESULT_NOK
            update_ddns = False

    response_code = None
    response_text = None
    if update_ddns:
        ip_address = args.ip if args.ip else utils.get_ip()
        if not ip_address:
            process_message = "Unable to get IP address. Check connection."
            exec_result = EXECUTION_RESULT_NOK
        elif ip_address == utils.get_dns_ip(args.hostname):
            process_message = "No update required."
        else:
            updater = provider_class(auth, args.hostname, updater_options)
            print("Updating hostname '%s' with IP address %s "
                  "[provider: '%s']..."
                  % (args.hostname, ip_address, args.provider))
            response_code, response_text = updater.update_dns(ip_address)
            process_message = updater.status_message

    proc_result = {
        'exec_result': exec_result,
        'response_code': response_code,
        'response_text': response_text,
        'process_message': process_message,
    }

    return proc_result


def create_parser():
    parser = argparse.ArgumentParser(
        description="Update DDNS IP address on selected provider.")
    parser.add_argument('-u', '--usertoken', help="provider username or token")
    parser.add_argument('-p', '--password',
                        help="provider password when apply")
    parser.add_argument('-n', '--hostname',
                        help="provider hostname to be updated")
    parser.add_argument('--provider', help="DDNS provider plugin (default: %s)"
                                           % dnsupdater.DEFAULT_PLUGIN,
                        choices=dnsupdater.AVAILABLE_PLUGINS.keys(),
                        default=dnsupdater.DEFAULT_PLUGIN)
    parser.add_argument('--url', help="custom DDNS server address")
    parser.add_argument('--store',
                        help="store DDNS authentication information and "
                             "update the hostname if it is provided",
                        action='store_true')
    parser.add_argument('-c', '--config',
                        help="noipy config directory (default: %s)" %
                             authinfo.DEFAULT_CONFIG_DIR,
                        default=authinfo.DEFAULT_CONFIG_DIR)
    parser.add_argument('ip', metavar='IP_ADDRESS', nargs='?',
                        help="New host IP address. If not provided, current "
                             "external IP address will be used.")

    return parser


def main():
    print("== noipy DDNS updater tool v%s ==" % __version__)
    parser = create_parser()
    args = parser.parse_args()

    result = execute_update(args)
    print(result.get('process_message'))
    if result.get('exec_result') != EXECUTION_RESULT_OK:
        parser.format_usage()

    sys.exit(result.get('exec_result'))

if __name__ == '__main__':
    main()
