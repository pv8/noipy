#!/usr/bin/env python
# -*- coding: utf-8 -*-

# noipy.dnsupdater
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.md and LICENSE.md for details.

import urllib
import argparse
import re
import sys
import settings 
import getpass

def get_ip():
    """
    (NoneType) -> str
    
    Return the machine external IP.
    """

    page = urllib.urlopen('http://checkip.dyndns.org')
    content = page.read()

    return re.search(r'(\d{1,3}\.?){4}', content).group()

def call_api(update_info, ip):
    """(dict of {str: str}, str) -> str
    
    Call No-IP API based on dict login_info and return the status code. 
    """

    base_url = 'https://{0}:{1}@dynupdate.no-ip.com/nic/update?hostname={2}&myip={3}' 

    api_call_url = base_url.format(update_info['username'], update_info['password'],
                                          update_info['hostname'], ip) 

    # call update url
    result = urllib.urlopen(api_call_url)

    return result.read()

def print_status(status_code):
    """(str) -> NoneType
    
    Print friendly response from API based on status_code.   
    See details: http://www.noip.com/integrate/response/
    """

    if 'good' in status_code:
        print 'SUCCESS: DNS hostname update successful. Followed by a space and the IP address it was updated to.'
    elif 'nochg' in status_code:
        print 'SUCCESS: IP address is current, no update performed. Followed by a space and the IP address that it is currently set to.'
    elif status_code == 'nohost':
        print 'ERROR: Hostname supplied does not exist under specified account, client exit and require user to enter new login credentials before performing and additional request.'
    elif status_code == 'badauth':
        print 'ERROR: Invalid username password combination.'
    elif status_code == 'badagent':
        print 'ERROR: Client disabled. Client should exit and not perform any more updates without user intervention.'
    elif status_code == '!donator':
        print 'ERROR: An update request was sent including a feature that is not available to that particular user such as offline options.'
    elif status_code == 'abuse':
        print 'ERROR: Username is blocked due to abuse. Either for not following our update specifications or disabled due to violation of the No-IP terms of service. Our terms of service can be viewed at http://www.noip.com/legal/tos. Client should stop sending updates.'
    elif status_code == '911':
        print 'ERROR: A fatal error on our side such as a database outage. Retry the update no sooner 30 minutes.'
    else:
        print 'WARNING: Something went wrong !!!'

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

    # obtain wan ip from checkip.dyndns.org
    ip = get_ip()

    # call No-IP API
    print 'Updating hostname "%s" with IP %s ...' % (api_params['hostname'], ip) 
    response = call_api(api_params, ip)

    print_status(response)

if __name__ == '__main__':
    main()
