#!/usr/bin/env python
# -*- coding: utf-8 -*-

# noipy.dnsupdater
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.rst and LICENSE for details.

from __future__ import print_function

import re

import requests

from . import __title__, __version__, __email__

AVAILABLE_PLUGINS = {
    'noip': 'NoipDnsUpdater',
    'dyn': 'DynDnsUpdater',
    'duck': 'DuckDnsUpdater',
    'generic': 'GenericDnsUpdater',
}

DEFAULT_PLUGIN = 'generic'


response_messages = {
    'OK': "SUCCESS: DNS hostname successfully updated.",
    'badauth': "ERROR: Invalid username or password (badauth).",
    'nochg': "ERROR: Invalid username or password (nochg).",
    '401': "ERROR: Invalid username or password (401).",
    '403': "ERROR: Invalid username or password (403).",
    '!donator': "ERROR: Update request include a feature that is not "
                "available to informed user.",
    'notfqdn': "ERROR: The hostname specified is not a fully-qualified domain"
               " name (not in the form hostname.dyndns.org or domain.com).",
    'nohost': "ERROR: Hostname specified does not exist in this user account.",
    'numhost': "ERROR: Too many hosts (more than 20) specified in an update. "
               "Also returned if trying to update a round robin (which is "
               "not allowed).",
    'abuse': "ERROR: Username/hostname is blocked due to update abuse.",
    'badagent': "ERROR: User agent not sent or HTTP method not permitted.",
    'dnserr': "ERROR: DNS error encountered.",
    '911': "ERROR: Problem on server side. Retry update in a few minutes.",
    'KO': "ERROR: Hostname and/or token incorrect.",
}


class DnsUpdaterPlugin(object):
    """ Base class for any DDNS updater
    """

    auth_type = ""

    def __init__(self, auth, hostname, options=None):
        """Init plugin with auth information, hostname and IP address.
        """

        self._auth = auth
        self._hostname = hostname
        self._options = {} if options is None else options
        self.last_ddns_response = ""

    @property
    def auth(self):
        return self._auth

    @property
    def hostname(self):
        return self._hostname

    def _get_base_url(self):
        """Get the base URL for DDNS Update API. URL must contain 'hostname'
        and 'ip'. If authentication is via token string 'token' argument must
        be provided as well. Example:
          http://{auth_str}@ddnsprovider.com/update?hostname={hostname}&ip={ip}

        This method must be implemented by plugin subclasses
        """
        pass

    def update_dns(self, new_ip):
        """Call No-IP API based on dict login_info and return the status code.
        """

        headers = None
        if self.auth_type == 'T':
            api_call_url = self._get_base_url().format(hostname=self.hostname,
                                                       token=self.auth.token,
                                                       ip=new_ip)
        else:
            api_call_url = self._get_base_url().format(hostname=self.hostname,
                                                       ip=new_ip)
            headers = {
                'Authorization': "Basic %s" %
                                 self.auth.base64key.decode('utf-8'),
                'User-Agent': "%s/%s %s" % (__title__, __version__, __email__)
            }

        r = requests.get(api_call_url, headers=headers)
        self.last_ddns_response = str(r.text).strip()

        return r.status_code, r.text

    @property
    def status_message(self):
        """Return friendly response from API based on response code. """

        msg = None
        if self.last_ddns_response in response_messages.keys():
            msg = response_messages.get(self.last_ddns_response)
        elif 'good' in self.last_ddns_response \
                or 'nochg' in self.last_ddns_response:
            ip = re.search(r'(\d{1,3}\.?){4}', self.last_ddns_response).group()
            if 'good' in self.last_ddns_response:
                msg = "SUCCESS: DNS hostname IP (%s) successfully updated." % \
                      ip
            else:
                msg = "SUCCESS: IP address (%s) is up to date, nothing was " \
                      "changed. Additional 'nochg' updates may be considered" \
                      " abusive." % ip
        else:
            msg = "ERROR: Ooops! Something went wrong !!!"

        return msg

    def __str__(self):
        return '%s(host=%s)' % (type(self).__name__, self.hostname)


class NoipDnsUpdater(DnsUpdaterPlugin):
    """No-IP DDNS provider plugin """

    auth_type = "P"

    def _get_base_url(self):
        return "https://dynupdate.no-ip.com/nic/update?hostname={hostname}" \
               "&myip={ip}"


class DynDnsUpdater(DnsUpdaterPlugin):
    """DynDNS DDNS provider plugin """

    auth_type = "P"

    def _get_base_url(self):
        return "http://members.dyndns.org/nic/update?hostname={hostname}" \
               "&myip={ip}&wildcard=NOCHG&mx=NOCHG&backmx=NOCHG"


class DuckDnsUpdater(DnsUpdaterPlugin):
    """DuckDNS DDNS provider plugin """

    auth_type = "T"

    @property
    def hostname(self):
        hostname = self._hostname
        found = re.search(r'(.*?)\.duckdns\.org', self._hostname)
        if found:
            hostname = found.group(1)
        return hostname

    def _get_base_url(self):
        return "https://www.duckdns.org/update?domains={hostname}" \
               "&token={token}&ip={ip}"


class GenericDnsUpdater(DnsUpdaterPlugin):
    """ Generic DDNS provider plugin - accepts a custom specification for the
    DDNS base url
    """

    auth_type = "P"

    def _get_base_url(self):
        return "{url}?hostname={{hostname}}&myip={{ip}}&wildcard=NOCHG" \
               "&mx=NOCHG&backmx=NOCHG".format(url=self._options['url'])
