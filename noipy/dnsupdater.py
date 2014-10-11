#!/usr/bin/env python
# -*- coding: utf-8 -*-

# noipy.dnsupdater
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.rst and LICENSE for details.

from __future__ import print_function

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

import re

AVAILABLE_PLUGINS = {
    'noip': 'NoipDnsUpdater',
    'dyn': 'DynDnsUpdater',
    'duck': 'DuckDnsUpdater',
}

DEFAULT_PLUGIN = 'noip'


class DnsUpdaterPlugin(object):
    """ Base class for any DDNS updater
    """

    auth_type = ""
    default_page_url = ""

    def __init__(self, auth, hostname, page_url):
        """Init plugin with auth information, hostname and IP address.
        """

        self._auth = auth
        self._hostname = hostname
        self.last_status_code = ''
        self._page_url = page_url

    @property
    def auth(self):
        return self._auth

    @property
    def hostname(self):
        return self._hostname

    @property
    def page_url(self):
        return self._page_url if self._page_url else self.default_page_url

    def _get_base_url(self):
        """Get the base URL for DDNS Update API. URL must contain 'hostname'
        and 'ip'. If authentication is via token string 'token' argument must
        be provided as well. Example:
          http://{auth_str}@ddnsprovider.com/update?hostname={hostname}&ip={ip}

        This method must be implemented by plugin subclasses
        """

        return NotImplemented

    def update_dns(self, new_ip):
        """Call No-IP API based on dict login_info and return the status code.
        """

        if self.auth_type == 'T':
            api_call_url = self._get_base_url().format(hostname=self.hostname,
                                                       token=self.auth.token,
                                                       ip=new_ip,
                                                       page_url=self.page_url)
            request = urllib2.Request(api_call_url)
        else:
            api_call_url = self._get_base_url().format(hostname=self.hostname,
                                                       ip=new_ip,
                                                       page_url=self.page_url)
            request = urllib2.Request(api_call_url)
            request.add_header('Authorization', 'Basic %s' %
                               self.auth.base64key.decode('utf-8'))

        try:
            response = urllib2.urlopen(request)
            self.last_status_code = response.read().decode('utf-8')
        except urllib2.HTTPError as e:
            self.last_status_code = str(e.code)

    @property
    def status_message(self):
        """Return friendly response from API based on response code. """

        msg = None
        if self.last_status_code in ['badauth', 'nochg', '401', '403']:
            msg = "ERROR: Invalid username or password (%s)." % \
                  self.last_status_code
        elif 'good' in self.last_status_code \
                or 'nochg' in self.last_status_code:
            ip = re.search(r'(\d{1,3}\.?){4}', self.last_status_code)
            ip = ip.group() if ip else ''
            if 'good' in self.last_status_code:
                msg = "SUCCESS: DNS hostname IP (%s) successfully updated." % ip
            else:
                msg = "SUCCESS: IP address (%s) is up to date, nothing was " \
                      "changed. Additional 'nochg' updates may be considered" \
                      " abusive." % ip
        elif self.last_status_code == '!donator':
            msg = "ERROR: Update request include a feature that is not " \
                  "available to informed user."
        elif self.last_status_code == 'notfqdn':
            msg = "ERROR: The hostname specified is not a fully-qualified " \
                  "domain name (not in the form hostname.dyndns.org or " \
                  "domain.com)."
        elif self.last_status_code == 'nohost':
            msg = "ERROR: Hostname specified does not exist in this user " \
                  "account."
        elif self.last_status_code == 'numhost':
            msg = "ERROR: Too many hosts (more than 20) specified in an " \
                  "update. Also returned if trying to update a round robin " \
                  "(which is not allowed)."
        elif self.last_status_code == 'abuse':
            msg = "ERROR: Username/hostname is blocked due to update abuse."
        elif self.last_status_code == 'badagent':
            msg = "ERROR: User agent not sent or HTTP method not permitted."
        elif self.last_status_code == 'dnserr':
            msg = "ERROR: DNS error encountered."
        elif self.last_status_code == '911':
            msg = "ERROR: Problem on server side. Retry update in a few " \
                  "minutes."
        elif self.last_status_code == 'OK':
            msg = "SUCCESS: DNS hostname successfully updated."
        elif self.last_status_code == 'KO':
            msg = "ERROR: Hostname and/or token incorrect."
        else:
            msg = "WARNING: Ooops! Something went wrong !!!"

        return msg

    def __str__(self):
        return '%s(host=%s)' % (type(self).__name__, self.hostname)


class NoipDnsUpdater(DnsUpdaterPlugin):
    """No-IP DDNS provider plugin """

    auth_type = "P"
    default_page_url = "https://dynupdate.no-ip.com/nic/update"

    def _get_base_url(self):
        return "{page_url}?hostname={hostname}&myip={ip}"


class DynDnsUpdater(DnsUpdaterPlugin):
    """DynDNS DDNS provider plugin """

    auth_type = "P"
    default_page_url = "http://members.dyndns.org/nic/update"

    def _get_base_url(self):
        return "{page_url}?hostname={hostname}" \
               "&myip={ip}&wildcard=NOCHG&mx=NOCHG&backmx=NOCHG"


class DuckDnsUpdater(DnsUpdaterPlugin):
    """DuckDNS DDNS provider plugin """

    auth_type = "T"
    default_page_url = "https://www.duckdns.org/update"

    @property
    def hostname(self):
        hostname = self._hostname
        found = re.search(r'(.*?)\.duckdns\.org', self._hostname)
        if found:
            hostname = found.group(1)
        return hostname

    def _get_base_url(self):
        return "{page_url}?domains={hostname}&token={token}&ip={ip}"
