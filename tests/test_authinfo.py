#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2013 Pablo V <noipy@pv8.dev>
#
# SPDX-License-Identifier: Apache-2.0

import pytest

from noipy import authinfo


def test_get_instance_password():
    # given
    auth1 = authinfo.ApiAuth('username', 'password')
    auth2 = authinfo.ApiAuth.get_instance(b'dXNlcm5hbWU6cGFzc3dvcmQ=')

    # when/then
    assert auth1 == auth2, 'ApiAuth.get_instance fail for password.'


def test_get_token_property_with_password():
    # given
    auth = authinfo.ApiAuth('username', 'password')

    # then
    with pytest.raises(NotImplementedError):
        # when
        _ = auth.token


def test_get_instance_token():
    # given
    token = '1234567890ABCDEFG'
    auth1 = authinfo.ApiAuth(usertoken=token)

    # when
    auth2 = authinfo.ApiAuth.get_instance(b'MTIzNDU2Nzg5MEFCQ0RFRkc6')

    # then
    assert auth1 == auth2, 'ApiAuth.get_instance fail for token.'
    assert auth1.token == auth2.token, 'ApiAuth.token fail.'


@pytest.mark.parametrize("other_user,other_pass,expected", [
    ('user1', 'pass1', True),
    ('user2', 'pass2', False),
    ('user1', 'pass2', False),
    ('user2', 'pass1', False),
])
def test_auth_info_equality(other_user, other_pass, expected):
    # given
    auth1 = authinfo.ApiAuth('user1', 'pass1')
    auth2 = authinfo.ApiAuth(other_user, other_pass)

    # when/then
    assert (auth1 == auth2) is expected


def test_store_creates_directories_and_file(tmp_path):
    # given
    config_dir = tmp_path / "custom_config"
    auth = authinfo.ApiAuth('testuser', 'testpass')

    noipy_dir = config_dir / '.noipy'
    auth_file = noipy_dir / 'testprovider'

    # when
    authinfo.store(auth, 'testprovider', str(config_dir))

    # then
    assert noipy_dir.exists()
    assert auth_file.exists()

    with open(auth_file) as f:
        stored_content = f.read()

    expected_content = auth.base64key.decode('utf-8')
    assert stored_content == expected_content


def test_store_with_existing_directories(tmp_path):
    # given
    config_dir = tmp_path / "existing_config"
    noipy_dir = config_dir / '.noipy'
    noipy_dir.mkdir(parents=True)
    auth = authinfo.ApiAuth('user', 'pass')

    # when
    authinfo.store(auth, 'provider', str(config_dir))

    # then
    auth_file = noipy_dir / 'provider'
    assert auth_file.exists()


def test_load_existing_auth_file(tmp_path):
    # given
    config_dir = tmp_path / "config"
    noipy_dir = config_dir / '.noipy'
    noipy_dir.mkdir(parents=True)
    auth_file = noipy_dir / 'loadprovider'

    expected_auth = authinfo.ApiAuth('loaduser', 'loadpass')

    with open(auth_file, 'w') as f:
        f.write(expected_auth.base64key.decode('utf-8'))

    # when
    loaded_auth = authinfo.load('loadprovider', str(config_dir))

    # then
    assert loaded_auth._usertoken == 'loaduser'
    assert loaded_auth == expected_auth
    assert loaded_auth._password == 'loadpass'


def test_load_nonexistent_file_raises_ioerror(tmp_path):
    # given
    config_dir = tmp_path / "empty_config"

    # then
    with pytest.raises(IOError):
        # when
        authinfo.load('nonexistent', str(config_dir))


def test_authinfo_exists_for_existing_file(tmp_path):
    # given
    config_dir = tmp_path / "config"
    noipy_dir = config_dir / '.noipy'
    noipy_dir.mkdir(parents=True)
    auth_file = noipy_dir / 'existingprovider'
    auth_file.write_text('dummy_content')

    # when/then
    assert authinfo.exists('existingprovider', str(config_dir))


def test_authinfo_exists_for_nonexistent_file(tmp_path):
    # given
    config_dir = tmp_path / "config"

    # when/then
    assert not authinfo.exists('nonexistent', str(config_dir))


def test_load_nonexistent_file(tmp_path):
    # given
    config_dir = tmp_path / "noipy_config"

    # then
    with pytest.raises(IOError):
        # when
        authinfo.load(provider='noip', config_location=str(config_dir))
