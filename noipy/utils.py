#!/usr/bin/env python
# -*- coding: utf-8 -*-

# noipy.utils
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.rst and LICENSE for details.

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import socket

import dns.resolver
import requests

HTTPBIN_URL = "https://httpbin.org/ip"

IP4ONLY_URL = "http://ip4only.me/api"
IP6ONLY_URL = "http://ip6only.me/api"

COMMON_DNS = "8.8.8.8"

try:
    input = raw_input
except NameError:
    pass


def read_input(message):
    return input(message)


def _try_request_get_and_store(url, callback):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            callback(r)
    except requests.exceptions.ConnectionError:
        pass


def get_ip():
    """Return machine's origin IP address(es).
    """

    lst = []
    for url in (IP4ONLY_URL, IP6ONLY_URL):
        _try_request_get_and_store(
            url,
            lambda r: lst.append(r.text.split(',')[1])
        )
    if not lst:
        _try_request_get_and_store(
            HTTPBIN_URL,
            lambda r: lst.append(r.json()['origin'])
        )
    if not lst:
        return None
    return ','.join(lst)


def _safe_resolve(dnsname, dnstype):
    resolver = dns.resolver.Resolver(StringIO("nameserver %s" % COMMON_DNS))

    try:
        resolve = resolver.resolve
    except AttributeError:
        resolve = resolver.query

    try:
        return list(resolve(dnsname, dnstype))
    except dns.exception.DNSException:
        return []


def get_dns_ip(dnsname):
    """Return machine's current IP address(es) in DNS.
    """

    lst = [a.address for a in _safe_resolve(dnsname, 'A') + _safe_resolve(dnsname, 'AAAA')]
    if not lst:
        try:
            lst.append(socket.gethostbyname(dnsname))
        except socket.error:
            pass
    if not lst:
        return None
    return ','.join(lst)
