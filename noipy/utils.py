#!/usr/bin/env python
# -*- coding: utf-8 -*-

# noipy.utils
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.rst and LICENSE for details.

import socket
import sys

import requests


def get_input(message):
    if sys.version_info[:2] < (3, 0):
        return input(message)
    else:
        return raw_input(message)


def get_ip():
    """Return machine's origin IP address.
    """
    try:
        r = requests.get("http://httpbin.org/ip")
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
