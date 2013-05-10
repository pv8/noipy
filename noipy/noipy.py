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
import settings 

class ApiAuth:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def username(self):
        return self.username

    @property
    def password(self):
        return self.password

    def __str__(self):
        return '%s:%s' % (self.username, self.password)

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

    # with store, this option is no longer necessary
    # parser.add_argument('-f', '--file', help='settings file with login & hostname information')

    parser.add_argument('-s', '--store', help='store login information and update the hostname if it is provided',
                        action='store_true')

    args = parser.parse_args()

    # load login information
    api_params = {}
    if args.store:  # --store argument
        if args.username and args.password:
            api_params['username'] = args.username
            api_params['password'] = args.password
        else:
            api_params['username'] = raw_input('Type your username: ')
            api_params['password'] = getpass.getpass('Type your password: ')
        settings.store(api_params)
        if args.hostname:
            api_params['hostname'] = args.hostname
    # elif args.file: # --file argument
    #    api_params = settings.load(args.file)
    elif args.username and args.password and args.hostname:  # informations arguments
        api_params['username'] = args.username
        api_params['password'] = args.password
        api_params['hostname'] = args.hostname
    elif args.hostname and settings.file_exists():
        api_params = settings.load()
        api_params['hostname'] = args.hostname
    else:  # no arguments 
        print 'Atention: The hostname to be updated must be provided.\nUsername and ' \
            'password can be either provided via command line or stored with --store ' \
            'option.\nExecute noipy --help for detailed information.'
        print parser.format_usage()
        sys.exit(1)

    return api_params

def main():
    # parse command line args
    api_params = parse_args()

    auth = ApiAuth(api_params['username'], api_params['password'])
    ip = get_ip()

    updater = dnsupdater.NoIpDnsUpdater(auth, api_params['hostname'], ip)

    print 'Updating hostname "%s" with IP address %s ...' % (api_params['hostname'], ip)
    updater.update_dns()
    updater.print_status_message()

if __name__ == '__main__':
    main()
