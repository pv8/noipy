#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2013 Pablo V <noipy@pv8.dev>
#
# SPDX-License-Identifier: Apache-2.0


from unittest.mock import Mock

import pytest

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
