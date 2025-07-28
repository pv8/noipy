#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tests.test_main
# Copyright (c) 2013 Pablo O Vieira (povieira)
# See README.rst and LICENSE for details.

import pytest
import requests
from unittest.mock import Mock

from noipy import main
from noipy import authinfo
from noipy import dnsupdater


def test_cmd_line_no_args(parser):
    # given
    cli_args = []
    args = parser.parse_args(cli_args)

    # when
    result = main.execute_update(args)

    # then
    assert result.get('exec_result') == main.EXECUTION_RESULT_NOK, 'Execution without args failed.'
    assert result.get('process_message').startswith('Warning: The hostname to be updated must be provided.'), \
        "Status message should start with 'Warning: The hostname to be updated must be provided.'"


def test_unchanged_ip(parser, monkeypatch):
    # given
    import socket
    monkeypatch.setattr(socket, 'gethostbyname', lambda _: '127.0.0.1')
    cli_args = [
        '-u', 'username',
        '-p', 'password',
        '--url', 'https://dynupdate.no-ip.com/nic/update',
        '--provider', 'generic',
        '-n', 'localhost',
        '127.0.0.1',
    ]
    args = parser.parse_args(cli_args)

    # when
    result = main.execute_update(args)

    # then
    assert result.get('exec_result') == main.EXECUTION_RESULT_OK, 'Update with unchanged IP failed.'
    assert result.get('process_message') == 'No update required.', "Status message should be 'No update required'."


def test_without_ip(parser, monkeypatch):
    # given
    monkeypatch.setattr('noipy.utils.get_ip', lambda: None)
    cli_args = [
        '-u', 'username',
        '-p', 'password',
        '--provider', 'noip',
        '-n', 'noipy.no-ip.org',
    ]
    args = parser.parse_args(cli_args)

    # when
    result = main.execute_update(args)

    # then
    assert result.get('exec_result') == main.EXECUTION_RESULT_NOK, 'Update without IP failed.'
    assert result.get('process_message').startswith('Unable to get IP address'), \
        "Status message should be 'Unable to get IP address'."

# authinfo tests


def test_store_auth_from_arguments(parser, tmp_path):
    # given
    config_dir = tmp_path / "noipy_config"
    cli_args = [
        '--store',
        '-u', 'username',
        '-p', 'password',
        '--provider', 'noip',
        '-c', str(config_dir),
    ]
    args = parser.parse_args(cli_args)

    # when
    result = main.execute_update(args)

    # then
    assert result.get('exec_result') == main.EXECUTION_RESULT_OK, 'Error storing auth info'
    assert result.get('process_message') == 'Auth info stored.', "Status message should be an 'Auth info stored.'"

    # Verify auth info was actually stored
    auth = authinfo.load(provider='noip', config_location=str(config_dir))
    expected_auth = authinfo.ApiAuth('username', 'password')
    assert auth == expected_auth


def test_load_stored_auth_for_update(parser, tmp_path, monkeypatch, mock_response):
    # given
    mock_response.text = 'good 10.1.2.3'
    monkeypatch.setattr(requests, 'get', lambda *args, **kwargs: mock_response)
    config_dir = tmp_path / "noipy_config"

    # Pre-store auth info
    auth = authinfo.ApiAuth('username', 'password')
    authinfo.store(auth, 'noip', str(config_dir))

    cli_args = [
        '--provider', 'noip',
        '-n', 'noipy.no-ip.org',
        '-c', str(config_dir),
        '10.1.2.3',
    ]
    args = parser.parse_args(cli_args)

    # when
    result = main.execute_update(args)

    # then
    assert result.get('exec_result') == main.EXECUTION_RESULT_OK, 'Error loading auth info'
    assert result.get('response_code') == 200


def test_store_and_perform_update(parser, tmp_path, test_ip, monkeypatch, mock_response):
    # given
    mock_response.text = 'good 10.1.2.3'
    monkeypatch.setattr(requests, 'get', lambda *args, **kwargs: mock_response)
    config_dir = tmp_path / "noipy_config"
    cli_args = [
        '--store',
        '-u', 'username',
        '-p', 'password',
        '--provider', 'noip',
        '-n', 'noipy.no-ip.org',
        '-c', str(config_dir),
        test_ip,
    ]
    args = parser.parse_args(cli_args)

    # when
    result = main.execute_update(args)

    # then
    assert result.get('exec_result') == main.EXECUTION_RESULT_OK, 'Error storing auth info'
    assert result.get('response_code') == 200


def test_store_from_stdin_input(parser, tmp_path, monkeypatch):
    # given
    monkeypatch.setattr('noipy.utils.read_input', lambda _: 'username')
    monkeypatch.setattr('getpass.getpass', lambda _: 'password')
    config_dir = tmp_path / "noipy_config"
    cli_args = ['--store', '--provider', 'noip', '-c', str(config_dir)]
    args = parser.parse_args(cli_args)

    expected_auth = authinfo.ApiAuth('username', 'password')

    # when
    result = main.execute_update(args)

    # then
    assert result.get('exec_result') == main.EXECUTION_RESULT_OK, 'Error storing auth info'
    assert result.get('process_message') == 'Auth info stored.', \
        "Status message should be an 'Auth info stored.'"

    auth = authinfo.load(provider='noip', config_location=str(config_dir))
    assert auth == expected_auth


def test_store_pass_from_stdin_input(parser, tmp_path, monkeypatch):
    # given
    monkeypatch.setattr('getpass.getpass', lambda _: 'password')
    config_dir = tmp_path / "noipy_config"
    cli_args = [
        '-u', 'username',
        '--store',
        '--provider', 'noip',
        '-c', str(config_dir),
    ]
    args = parser.parse_args(cli_args)

    # when
    result = main.execute_update(args)

    # then
    assert result.get('exec_result') == main.EXECUTION_RESULT_OK, 'Error storing auth info'
    assert result.get('process_message') == 'Auth info stored.', \
        "Status message should be an 'Auth info stored.'"


def test_store_token_from_stdin_input(parser, tmp_path, monkeypatch):
    # given
    expected_token_input = '1234567890ABC'
    monkeypatch.setattr('noipy.utils.read_input', lambda _: expected_token_input)
    config_dir = tmp_path / "noipy_config"
    cli_args = ['--store', '--provider', 'duck', '-c', str(config_dir)]
    args = parser.parse_args(cli_args)

    # when
    result = main.execute_update(args)
    auth = authinfo.load(provider='duck', config_location=str(config_dir))

    # then
    assert result.get('exec_result') == main.EXECUTION_RESULT_OK, 'Error storing auth info'
    assert result.get('process_message') == 'Auth info stored.', \
        "Status message should be an 'Auth info stored.'"

    assert auth.token == expected_token_input


def test_update_custom_config_file(parser, tmp_path, test_ip):
    # given
    config_dir = tmp_path / "custom_config"
    cli_args = [
        '--provider', 'noip',
        '-n', 'noipy.no-ip.org',
        '-c', str(config_dir),
        test_ip,
    ]
    args = parser.parse_args(cli_args)

    # when
    result = main.execute_update(args)

    # then
    assert result.get('exec_result') == main.EXECUTION_RESULT_NOK, 'Update without auth info failed.'
    assert result.get('process_message').startswith('No stored auth information found for provider:'), \
        "Status message should be 'No stored auth information found for provider: ...'"


# dnsupdater tests

def test_noip_plugin(parser, test_ip, monkeypatch, mock_response):
    # given
    mock_response.text = 'good 10.1.2.3'
    monkeypatch.setattr(requests, 'get', lambda *args, **kwargs: mock_response)
    cli_args = [
        '-u', 'username',
        '-p', 'password',
        '--provider', 'noip',
        '-n', 'noipy.no-ip.org',
        test_ip,
    ]
    args = parser.parse_args(cli_args)

    # when
    result = main.execute_update(args)

    # then
    assert result.get('exec_result') == main.EXECUTION_RESULT_OK, "Update with 'No-IP' provider failed."
    assert result.get('response_code') == 200


def test_dyndns_plugin(parser, test_ip, monkeypatch, mock_response):
    # given
    mock_response.text = 'good 10.1.2.3'
    monkeypatch.setattr(requests, 'get', lambda *args, **kwargs: mock_response)
    cli_args = [
        '-u', 'test',
        '-p', 'test',
        '--provider', 'dyn',
        '-n', 'test.dyndns.org',
        test_ip,
    ]
    args = parser.parse_args(cli_args)

    # when
    result = main.execute_update(args)

    # then
    assert result.get('exec_result') == main.EXECUTION_RESULT_OK, "Update with 'DynDNS' provider failed."
    assert result.get('response_code') == 200


def test_duckdns_plugin(parser, test_ip, monkeypatch, mock_response):
    # given
    mock_response.text = 'OK'
    monkeypatch.setattr(requests, 'get', lambda *args, **kwargs: mock_response)
    cli_args = [
        '-u', '1234567890ABC',
        '--provider', 'duck',
        '-n', 'noipy.duckdns.org',
        test_ip,
    ]
    args = parser.parse_args(cli_args)

    # when
    result = main.execute_update(args)

    # then
    assert result.get('exec_result') == main.EXECUTION_RESULT_OK, "Update with 'DuckDNS' provider failed."
    assert result.get('response_code') == 200


def test_generic_plugin(parser, test_ip, monkeypatch, mock_response):
    # given
    mock_response.text = 'good 10.1.2.3'
    monkeypatch.setattr(requests, 'get', lambda *args, **kwargs: mock_response)
    cli_args = [
        '-u', 'username',
        '-p', 'password',
        '--url', 'https://dynupdate.no-ip.com/nic/update',
        '--provider', 'generic',
        '-n', 'noipy.no-ip.org',
        test_ip,
    ]
    args = parser.parse_args(cli_args)

    # when
    result = main.execute_update(args)

    # then
    assert result.get('exec_result') == main.EXECUTION_RESULT_OK, "Update with 'No-IP' using generic provider failed."
    assert result.get('response_code') == 200


def test_generic_plugin_malformed_url(parser, test_ip):
    # given
    cli_args = [
        '-u', 'username',
        '-p', 'password',
        '--url', 'abced',
        '--provider', 'generic',
        '-n', 'noipy.no-ip.org',
        test_ip,
    ]
    args = parser.parse_args(cli_args)

    # when
    result = main.execute_update(args)

    # then
    assert result.get('exec_result') == main.EXECUTION_RESULT_NOK, \
        'An error should be flagged when --provider is "generic" and URL is malformed.'
    assert result.get('process_message') == 'Malformed URL.', 'Status message should contain "Malformed URL."'


def test_generic_plugin_without_url(parser, test_ip):
    # given
    cli_args = [
        '-u', 'username',
        '-p', 'password',
        '--provider', 'generic',
        '-n', 'noipy.no-ip.org',
        test_ip,
    ]
    args = parser.parse_args(cli_args)

    # when
    result = main.execute_update(args)

    # then
    assert result.get('exec_result') == main.EXECUTION_RESULT_NOK, \
        'An error should be flagged when --provider is  "generic" and no URL is provided.'
    assert result.get('process_message').startswith('Must use --url'), \
        'Status message should start with "Must use --url".'


# Provider-specific response code tests

@pytest.mark.parametrize("response_text,expected_status,expected_exec_result", [
    ('good 192.168.1.1', 200, main.EXECUTION_RESULT_OK),
    ('nochg 192.168.1.1', 200, main.EXECUTION_RESULT_OK),
    ('badauth', 401, main.EXECUTION_RESULT_OK),  # API returns 401 but we handle it
    ('nohost', 200, main.EXECUTION_RESULT_OK),
    ('notfqdn', 200, main.EXECUTION_RESULT_OK),
    ('badagent', 200, main.EXECUTION_RESULT_OK),
    ('abuse', 200, main.EXECUTION_RESULT_OK),
    ('!donator', 200, main.EXECUTION_RESULT_OK),
])
def test_noip_response_codes(parser, test_ip, monkeypatch, response_text, expected_status, expected_exec_result):
    # given
    mock_response = Mock()
    mock_response.text = response_text
    mock_response.status_code = expected_status
    monkeypatch.setattr(requests, 'get', lambda *args, **kwargs: mock_response)
    cli_args = [
        '-u', 'username',
        '-p', 'password',
        '--provider', 'noip',
        '-n', 'noipy.no-ip.org',
        test_ip,
    ]
    args = parser.parse_args(cli_args)

    # when
    result = main.execute_update(args)

    # then
    assert result.get('exec_result') == expected_exec_result
    assert result.get('response_code') == expected_status

    # Verify appropriate status message is returned
    if 'good' in response_text:
        assert 'successfully updated' in result.get('process_message')
    elif 'nochg' in response_text:
        assert 'up to date' in result.get('process_message')
    elif response_text == 'badauth':
        assert 'Invalid username or password' in result.get('process_message')
    elif response_text == 'nohost':
        assert 'Hostname specified does not exist' in result.get('process_message')
    elif response_text == 'notfqdn':
        assert 'not a fully-qualified domain name' in result.get('process_message')
    elif response_text == 'badagent':
        assert 'User agent not sent' in result.get('process_message')
    elif response_text == 'abuse':
        assert 'blocked due to update abuse' in result.get('process_message')
    elif response_text == '!donator':
        assert 'feature that is not available' in result.get('process_message')


@pytest.mark.parametrize("response_text,expected_message", [
    ('OK', 'SUCCESS: DNS hostname successfully updated.'),
    ('KO', 'ERROR: Hostname and/or token incorrect.'),
    ('NOCHANGE', 'ERROR: Ooops! Something went wrong !!!'),  # Unknown response
])
def test_duckdns_response_codes(parser, test_ip, monkeypatch, response_text, expected_message):
    # given
    mock_response = Mock()
    mock_response.text = response_text
    mock_response.status_code = 200
    monkeypatch.setattr(requests, 'get', lambda *args, **kwargs: mock_response)
    cli_args = [
        '-u', '1234567890ABC',
        '--provider', 'duck',
        '-n', 'noipy.duckdns.org',
        test_ip,
    ]
    args = parser.parse_args(cli_args)

    # when
    result = main.execute_update(args)

    # then
    assert result.get('exec_result') == main.EXECUTION_RESULT_OK
    assert result.get('response_code') == 200
    assert result.get('process_message') == expected_message


@pytest.mark.parametrize("response_text", [
    'good',
    'nochg',
    'badauth',
    'notfqdn',
    'nohost',
    'numhost',
    'abuse',
    'badagent',
    'dnserr',
    '911',
])
def test_dyndns_response_codes(parser, test_ip, monkeypatch, response_text):
    # given
    if response_text in ['good', 'nochg']:
        response_text = f'{response_text} {test_ip}'

    mock_response = Mock()
    mock_response.text = response_text
    mock_response.status_code = 200
    monkeypatch.setattr(requests, 'get', lambda *args, **kwargs: mock_response)
    cli_args = [
        '-u', 'test',
        '-p', 'test',
        '--provider', 'dyn',
        '-n', 'test.dyndns.org',
        test_ip,
    ]
    args = parser.parse_args(cli_args)

    # when
    result = main.execute_update(args)

    # then
    assert result.get('exec_result') == main.EXECUTION_RESULT_OK
    assert result.get('response_code') == 200

    plugin = dnsupdater.DynDnsUpdater(authinfo.ApiAuth('test', 'test'), 'test.dyndns.org')
    plugin.last_ddns_response = response_text.strip()
    assert plugin.status_message == result.get('process_message')
