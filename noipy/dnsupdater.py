#!/usr/bin/env python
# -*- coding: utf-8 -*-

# dnsupdater
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.md and LICENSE.md for details.

import urllib
import argparse
import re
import sys

def get_ip():
    """
    (NoneType) -> NoneType
    
    Return the machine external IP.
    """

    page = urllib.urlopen('http://checkip.dyndns.org')
    content = page.read()

    r = re.compile(r'.*\<body>Current IP Address:\s(.*)\</body>.*')

    return r.match(content).group(1)

def load_properties(filename):
    """(str) -> dict of {str: str}
    
    Load update information from properties file and return them
    as a dictionary with keys "username", "password" and "hostname"
    """

    d = {}
    try:
        with open(filename) as f:
            d = dict([line.strip().split('=', 1) for line in f if not line.startswith('#')])
            #for line in f:
            #    tokens = line.strip().split('=', 1)
            #    d[tokens[0]] = '='.join(tokens[1:])
    except IOError as e:
        print '{0}: "{1}"'.format(e.strerror, filename)
        raise e

    return d

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
    elif 'nochg'  in status_code:
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
    parser.add_argument('-f', '--file', help='properties file with login & domain information')

    args = parser.parse_args()

    # load login information
    login_info = {}
    if args.file:
        login_info = load_properties(args.file)
    elif args.hostname:
        login_info['username'] = args.username
        login_info['password'] = args.password
        login_info['hostname'] = args.hostname
    else:
        print 'Either properties file with login information or domain argument must be provided.'
        print parser.format_usage()
        sys.exit(1)

    return login_info

def main():
    # parse command line args
    login_info = parse_args()

    # obtain wan ip from checkip.dyndns.org
    ip = get_ip()

    # call No-IP API
    print 'Updating hostname "%s" with IP %s ...' % (login_info['hostname'], ip) 
    response = call_api(login_info, ip)

    print_status(response)

if __name__ == '__main__':
    main()
