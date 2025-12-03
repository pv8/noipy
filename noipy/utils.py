#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2013 Pablo V <noipy@pv8.dev>
#
# SPDX-License-Identifier: Apache-2.0

import socket
from typing import Optional

import requests

HTTPBIN_URL = 'https://httpbin.org/ip'


def read_input(message: str) -> str:
    """Read input from user."""
    return input(message)


def get_ip() -> Optional[str]:
    """Return machine's origin IP address."""
    try:
        r = requests.get(HTTPBIN_URL)
        return r.json()['origin'] if r.status_code == 200 else None
    except requests.exceptions.ConnectionError:
        return None


def get_dns_ip(dnsname: str) -> Optional[str]:
    """Return machine's current IP address in DNS."""
    try:
        return socket.gethostbyname(dnsname)
    except socket.error:
        return None
