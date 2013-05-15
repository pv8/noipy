#!/usr/bin/env python
# -*- coding: utf-8 -*-

# noipy.dnsupdater
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.md and LICENSE.md for details.

import urllib2
import re
import abc

AVAILABLE_PLUGINS = {'noip': 'NoipDnsUpdater',
                     'dyn': 'DynDnsUpdater'}
DEFAULT_PLUGIN = 'noip'

class DnsUpdaterPlugin():
    """ Base class for any DDNS updater
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, auth, hostname):
        """Init plugin with auth information, hostname and IP address.
        """

        self.auth = auth
        self.hostname = hostname
        self.last_status_code = ''

    @abc.abstractmethod
    def _get_base_url(self):
        """ (None) -> str
        
        Get the base URL for DDNS Update API. URL must contain these 3 variables: 
        'auth_str' (auth string <usename:password>), 'hostname' and 'ip' 
        Example: https://{auth_str}@ddnsprovider.com/update?hostname={hostname}&ip={ip}  
        """

        return NotImplemented 

    def update_dns(self, new_ip):
        """(str) -> None
        
        Call No-IP API based on dict login_info and return the status code. 
        """

        api_call_url = self._get_base_url().format(auth_str=str(self.auth),
                                                   hostname=self.hostname, 
                                                   ip=new_ip) 
        
        # call update url
        #response = urllib.urlopen(api_call_url)
        request = urllib2.Request(api_call_url)
        request.get_method = lambda: 'GET'
        request.add_header('Authorization', 'Basic %s' % self.auth.get_base64_key())

        response = urllib2.urlopen(request)

        self.last_status_code = response.read()

    def print_status_message(self):
        """(str) -> NoneType
        
        Print friendly response from API based on response code.   
        """

        msg = '' 
        if 'good' in self.last_status_code or 'nochg' in self.last_status_code:
            ip = re.search(r'(\d{1,3}\.?){4}', self.last_status_code).group()
            if 'good' in self.last_status_code:
                msg = 'SUCCESS: DNS hostname IP (%s) successfully updated.' % ip
            else:
                msg = 'SUCCESS: IP address (%s) is up to date, nothing was changed. Additional "nochg" updates may be considered abusive.' % ip
        elif self.last_status_code == 'badauth':
            msg = 'ERROR: Invalid username or password.'
        elif self.last_status_code == '!donator':
            msg = 'ERROR: Update request include a feature that is not available to informed user.'
        elif self.last_status_code == 'notfqdn':
            msg = 'ERROR: The hostname specified is not a fully-qualified domain name (not in the form hostname.dyndns.org or domain.com).'
        elif self.last_status_code == 'nohost':
            msg = 'ERROR: Hostname specified does not exist in this user account.'
        elif self.last_status_code == 'numhost':
            msg = 'ERROR: Too many hosts (more than 20) specified in an update. Also returned if trying to update a round robin (which is not allowed).'
        elif self.last_status_code == 'abuse':
            msg = 'ERROR: Username/hostname is blocked due to update abuse. '
        elif self.last_status_code == 'badagent':
            msg = 'ERROR: User agent not sent or HTTP method not permitted.'
        elif self.last_status_code == 'dnserr':
            msg = 'ERROR: DNS error encountered'
        elif self.last_status_code == '911':
            msg = 'ERROR: Problem on server side. Retry update in a few minutes.'
        else:
            msg = 'WARNING: Ooops! Something went wrong !!!'

        print msg

    def __str__(self):
        return '%s(host=%s)' % (type(self).__name__, self.hostname)

class NoipDnsUpdater(DnsUpdaterPlugin):
    """No-IP DDNS provider plugin
    """

    def _get_base_url(self):
        return 'https://dynupdate.no-ip.com/nic/update?hostname={hostname}&myip={ip}'

class DynDnsUpdater(DnsUpdaterPlugin):
    """DynDNS DDNS provider plugin
    """

    def _get_base_url(self):
        return 'http://members.dyndns.org/nic/update?hostname={hostname}&myip={ip}&wildcard=NOCHG&mx=NOCHG&backmx=NOCHG'

