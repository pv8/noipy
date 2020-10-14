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


def get_ip():
    """Return machine's origin IP address(es).
    """
    lst = []
    try:
        r = requests.get(IP4ONLY_URL)
        if r.status_code == 200:
            lst.append(r.text.split(',')[1])
    except requests.exceptions.ConnectionError:
        pass
    try:
        r = requests.get(IP6ONLY_URL)
        if r.status_code == 200:
            lst.append(r.text.split(',')[1])
    except requests.exceptions.ConnectionError:
        pass
    if not lst:
        try:
            r = requests.get(HTTPBIN_URL)
            if r.status_code == 200:
                lst.append(r.json()['origin'])
        except requests.exceptions.ConnectionError:
            pass
    if not lst:
        return None
    return ','.join(lst)


def get_dns_ip(dnsname):
    """Return machine's current IP address(es) in DNS.
    """
    resolver = dns.resolver.Resolver(StringIO("nameserver %s" % COMMON_DNS))

    try:
        resolve = resolver.resolve
    except AttributeError:
        resolve = resolver.query

    lst = []
    try:
        lst += [a.address for a in resolve(dnsname, 'A')]
    except dns.exception.DNSException:
        pass
    try:
        lst += [a.address for a in resolve(dnsname, 'AAAA')]
    except dns.exception.DNSException:
        pass
    if not lst:
        try:
            lst.append(socket.gethostbyname(dnsname))
        except socket.error:
            pass
    if not lst:
        return None
    return ','.join(lst)
