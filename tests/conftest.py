#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tests.conftest
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.rst and LICENSE for details.


from unittest.mock import Mock

import pytest
import requests

from noipy import main


@pytest.fixture
def parser():
    """Return a configured argument parser."""
    return main.create_parser()


@pytest.fixture
def test_ip():
    return '10.1.2.3'


@pytest.fixture
def mock_response():
    response = Mock()
    response.status_code = 200
    response.text = 'good 10.1.2.3'
    return response


@pytest.fixture
def mock_requests_success(monkeypatch):
    def mock_get(url, **kwargs):
        response = Mock()
        response.status_code = 200
        response.text = 'good 10.1.2.3'
        response.json.return_value = {'origin': '192.168.1.1'}
        return response

    monkeypatch.setattr(requests, 'get', mock_get)
    return mock_get
