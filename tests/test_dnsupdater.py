#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2013 Pablo V <noipy@pv8.dev>
#
# SPDX-License-Identifier: Apache-2.0


import pytest
import requests

from noipy import authinfo
from noipy import dnsupdater


def test_plugin_instance_str():
    # given
    plugin = dnsupdater.NoipDnsUpdater(auth=None, hostname='noipy.no-ip.org')

    # when/then
    assert str(plugin) == 'NoipDnsUpdater(host=noipy.no-ip.org)'


@pytest.mark.parametrize("provider_name,expected_class,expected_auth_type,base_url_contains", [
    ('noip', dnsupdater.NoipDnsUpdater, 'P', 'dynupdate.no-ip.com'),
    ('dyn', dnsupdater.DynDnsUpdater, 'P', 'members.dyndns.org'),
    ('duck', dnsupdater.DuckDnsUpdater, 'T', 'duckdns.org'),
    ('generic', dnsupdater.GenericDnsUpdater, 'P', 'https://example.com/update'),
])
def test_plugin_class_instantiation(provider_name, expected_class, expected_auth_type, base_url_contains):
    # given
    auth = authinfo.ApiAuth('testuser', 'testpass')
    hostname = 'test.example.com'
    class_name = dnsupdater.AVAILABLE_PLUGINS.get(provider_name)
    options = {'url': 'https://example.com/update'} if provider_name == 'generic' else None

    # when
    plugin_class = getattr(dnsupdater, class_name)
    if options:
        plugin_instance = plugin_class(auth, hostname, options)
    else:
        plugin_instance = plugin_class(auth, hostname)

    # then
    assert isinstance(plugin_instance, expected_class)
    assert plugin_instance._auth == auth
    assert plugin_instance._hostname == hostname
    assert plugin_instance.auth_type == expected_auth_type
    assert base_url_contains in plugin_instance._base_url


def test_not_implemented_plugin():
    # given
    auth = authinfo.ApiAuth('username', 'password')
    hostname = 'hostname'
    plugin = dnsupdater.DnsUpdaterPlugin(auth, hostname)

    # then
    with pytest.raises(NotImplementedError) as exc_info:
        # when
        plugin.update_dns('10.1.1.1')

    # then
    assert str(exc_info.value) == "Subclasses must implement _base_url property", \
        "_base_url property should raise NotImplementedError"


@pytest.mark.parametrize("response,expected_message", [
    ('badauth', 'ERROR: Invalid username or password (badauth).'),
    ('good 1.1.1.1', 'SUCCESS: DNS hostname IP (1.1.1.1) successfully updated.'),
    ('nochg 1.1.1.1', "SUCCESS: IP address (1.1.1.1) is up to date, nothing was changed. "
                      "Additional 'nochg' updates may be considered abusive."),
    ('!donator', 'ERROR: Update request include a feature that is not available to informed user.'),
    ('notfqdn', 'ERROR: The hostname specified is not a fully-qualified domain name '
                '(not in the form hostname.dyndns.org or domain.com).'),
    ('nohost', 'ERROR: Hostname specified does not exist in this user account.'),
    ('numhost', 'ERROR: Too many hosts (more than 20) specified in an update. '
                'Also returned if trying to update a round robin (which is not allowed).'),
    ('abuse', 'ERROR: Username/hostname is blocked due to update abuse.'),
    ('badagent', 'ERROR: User agent not sent or HTTP method not permitted.'),
    ('dnserr', 'ERROR: DNS error encountered.'),
    ('911', 'ERROR: Problem on server side. Retry update in a few minutes.'),
    ('OK', 'SUCCESS: DNS hostname successfully updated.'),
    ('KO', 'ERROR: Hostname and/or token incorrect.'),
    ('UNKNOWN_CODE', 'ERROR: Ooops! Something went wrong !!!'),
])
def test_dns_plugin_status_message(response, expected_message):
    # given
    auth = authinfo.ApiAuth('username', 'password')
    hostname = 'hostname'
    plugin = dnsupdater.DnsUpdaterPlugin(auth, hostname)

    # when
    plugin.last_ddns_response = response

    # then
    assert plugin.status_message == expected_message


def test_plugin_update_connection_error(monkeypatch):
    # given
    def mock_get(*args, **kwargs):
        raise requests.exceptions.ConnectionError()

    monkeypatch.setattr(requests, 'get', mock_get)
    auth = authinfo.ApiAuth('username', 'password')
    plugin = dnsupdater.NoipDnsUpdater(auth, 'test.no-ip.org')

    # then
    with pytest.raises(requests.exceptions.ConnectionError):
        # when
        plugin.update_dns('10.1.2.3')


def test_plugin_update_timeout(monkeypatch):
    # given
    def mock_get(*args, **kwargs):
        raise requests.exceptions.Timeout()

    monkeypatch.setattr(requests, 'get', mock_get)
    auth = authinfo.ApiAuth('username', 'password')
    plugin = dnsupdater.NoipDnsUpdater(auth, 'test.no-ip.org')

    # then
    with pytest.raises(requests.exceptions.Timeout):
        # when
        plugin.update_dns('10.1.2.3')
