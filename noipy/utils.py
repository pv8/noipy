#!/usr/bin/env python
# -*- coding: utf-8 -*-

# noipy.utils
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.rst and LICENSE for details.

import socket

import requests

HTTPBIN_URL = "http://httpbin.org/ip"

try:
    input = raw_input
except NameError:
    pass


def read_input(message):
    return input(message)


def get_ip():
    """Return machine's origin IP address.
    """
    try:
        r = requests.get(HTTPBIN_URL)
        return r.json()['origin'] if r.status_code == 200 else None
    except requests.exceptions.ConnectionError:
        return None


def get_dns_ip(dnsname):
    """Return machine's current IP address in DNS.
    """
    try:
        return socket.gethostbyname(dnsname)
    except socket.error:
        return None
