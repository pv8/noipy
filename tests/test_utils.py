#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tests.test_utils
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.rst and LICENSE for details.

from unittest.mock import Mock

import requests

from noipy import utils


def test_get_ip_success(monkeypatch):
    # given
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'origin': '203.0.113.42'}

    called_with_url = None

    def mock_get(url, **kwargs):
        nonlocal called_with_url
        called_with_url = url
        return mock_response

    monkeypatch.setattr(requests, 'get', mock_get)

    # when
    ip = utils.get_ip()

    # then
    assert called_with_url == utils.HTTPBIN_URL
    assert ip == '203.0.113.42'


def test_get_ip_connection_error(monkeypatch):
    # given
    called_with_url = None

    def mock_get(url, **kwargs):
        nonlocal called_with_url
        called_with_url = url
        raise requests.exceptions.ConnectionError()

    monkeypatch.setattr(requests, 'get', mock_get)

    # when
    ip = utils.get_ip()

    # then
    assert called_with_url == utils.HTTPBIN_URL
    assert ip is None


def test_get_ip_non_200_status(monkeypatch):
    # given
    called_with_url = None
    mock_response = Mock()
    mock_response.status_code = 404

    def mock_get(url, **kwargs):
        nonlocal called_with_url
        called_with_url = url
        return mock_response

    monkeypatch.setattr(requests, 'get', mock_get)

    # when
    ip = utils.get_ip()

    # then
    assert called_with_url == utils.HTTPBIN_URL
    assert ip is None


def test_get_dns_ip_success(monkeypatch):
    # given
    import socket
    monkeypatch.setattr(socket, 'gethostbyname', lambda hostname: '127.0.0.1')

    # when
    ip = utils.get_dns_ip('localhost')

    # then
    assert ip == '127.0.0.1', 'get_dns_ip() failed.'


def test_get_dns_ip_error(monkeypatch):
    # given
    import socket

    def mock_gethostbyname(hostname):
        raise socket.error()

    monkeypatch.setattr(socket, 'gethostbyname', mock_gethostbyname)

    # when
    ip = utils.get_dns_ip('http://example.nothing')

    # then
    assert ip is None, f'get_dns_ip() should return None. IP={ip}'


def test_read_input(monkeypatch):
    # given
    monkeypatch.setattr('builtins.input', lambda _: 'test_input')

    # when
    result = utils.read_input('Enter something: ')

    # then
    assert result == 'test_input'
