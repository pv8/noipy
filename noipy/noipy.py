#!/usr/bin/env python
# -*- coding: utf-8 -*-

# noipy.noipy
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.rst and epl-v10.html for details.

from __future__ import print_function

try:
    import urllib.request as urllib
except ImportError:
    import urllib

import argparse
import sys
import re
import getpass

from . import dnsupdater
from . import authinfo

try: 
    input = raw_input
except NameError: 
    pass

def get_ip():
    """(NoneType) -> str
    
    Return the machine external IP.
    """

    page = urllib.urlopen('http://checkip.dyndns.org')
    content = page.read().decode('utf-8')

    return re.search(r'(\d{1,3}\.?){4}', content).group()

def main():
    parser = argparse.ArgumentParser(description='Update DDNS IP address on selected provider.')
    parser.add_argument('-u', '--username', help='provider auth username')
    parser.add_argument('-p', '--password', help='provider auth password')
    parser.add_argument('-n', '--hostname', help='provider hostname to be updated')
    parser.add_argument('--provider', help='DDNS provider plugin', 
                        choices=dnsupdater.AVAILABLE_PLUGINS.keys(), default=dnsupdater.DEFAULT_PLUGIN)
    parser.add_argument('--store', 
                        help='store DDNS authentication information and update the hostname if it is provided',
                        action='store_true')
    parser.add_argument('ip', metavar='IP_ADDRESS', nargs='?', 
                        help='New host IP address. If not provided, current external IP address will be used.')

    args = parser.parse_args()

    auth = None
    if args.store:  # --store argument
        if args.username and args.password:
            auth = authinfo.ApiAuth(args.username, args.password)
        else:
            username = input('Type your username: ')
            password = getpass.getpass('Type your password: ')
            auth = authinfo.ApiAuth(username, password)

        authinfo.store(auth, args.provider)
        if not args.hostname:
            sys.exit(1)
    elif args.username and args.password and args.hostname:  # informations arguments
        auth = authinfo.ApiAuth(args.username, args.password)
    elif args.hostname:
        if authinfo.exists(args.provider):
            auth = authinfo.load(args.provider)
        else:
            print('No stored auth information found for provider: "%s"' % args.provider)
            print(parser.format_usage())
            sys.exit(1)
    else:  # no arguments 
        print('Atention: The hostname to be updated must be provided.\nUsername and ' \
            'password can be either provided via command line or stored with --store ' \
            'option.\nExecute noipy --help for more details.')
        print(parser.format_usage())
        sys.exit(1)

    updater_class = getattr(dnsupdater, dnsupdater.AVAILABLE_PLUGINS.get(args.provider))
    updater = updater_class(auth, args.hostname)

    ip_address = args.ip if args.ip else get_ip()

    print('Updating hostname "%s" with IP address %s ...' % (args.hostname, ip_address))

    updater.update_dns(ip_address)
    print(updater.status_message)

if __name__ == '__main__':
    main()
