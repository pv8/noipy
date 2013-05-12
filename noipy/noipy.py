#!/usr/bin/env python

# noipy.noipy
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.md for details.

import argparse
import sys
import re
import urllib
import getpass

import dnsupdater
import authinfo

def get_ip():
    """(NoneType) -> str
    
    Return the machine external IP.
    """

    page = urllib.urlopen('http://checkip.dyndns.org')
    content = page.read()

    return re.search(r'(\d{1,3}\.?){4}', content).group()

def parse_args():
    """(NoneType) -> dict of {str: str}
    
    Parse commandline args and return a dictionary with keys "username", "password" and "hostname".
    """

    parser = argparse.ArgumentParser(description='Update DNS using NO-IP DNS Update API')
    parser.add_argument('-u', '--username', help='NO-IP username')
    parser.add_argument('-p', '--password', help='NO-IP password')
    parser.add_argument('-n', '--hostname', help='NO-IP hostname to be updated')
    parser.add_argument('--store', 
                        help='store DDNS authentication information and update the hostname if it is provided',
                        action='store_true')
    parser.add_argument('ip', metavar='IP_ADDRESS', nargs='?', 
                        help='New host IP address. If not provided, current external IP address will be used.')

    args = parser.parse_args()

    # load auth information
    api_params = {}
    if args.store:  # --store argument
        auth = None
        if args.username and args.password:
            auth = authinfo.ApiAuth(args.username, args.password)
            api_params['auth'] = auth
        else:
            username = raw_input('Type your username: ')
            password = getpass.getpass('Type your password: ')
            auth = authinfo.ApiAuth(username, password)
            api_params['auth'] = auth

        authinfo.store(auth)
        if args.hostname:
            api_params['hostname'] = args.hostname
        else:
            sys.exit(1)
    elif args.username and args.password and args.hostname:  # informations arguments
        api_params['auth'] = authinfo.ApiAuth(args.username, args.password)
        api_params['hostname'] = args.hostname
    elif args.hostname and authinfo.exists():
        api_params['auth'] = authinfo.load()
        api_params['hostname'] = args.hostname
    else:  # no arguments 
        print 'Atention: The hostname to be updated must be provided.\nUsername and ' \
            'password can be either provided via command line or stored with --store ' \
            'option.\nExecute noipy --help for more details.'
        print parser.format_usage()
        sys.exit(1)

    api_params['ip'] = args.ip if args.ip else get_ip()

    return api_params

def main():
    # parse command line args
    api_params = parse_args()
    
    updater = dnsupdater.NoIpDnsUpdater(api_params['auth'], api_params['hostname'])

    print 'Updating hostname "{hostname}" with IP address {ip} ...'.format(**api_params)
    updater.update_dns(api_params['ip'])
    updater.print_status_message()

if __name__ == '__main__':
    main()
