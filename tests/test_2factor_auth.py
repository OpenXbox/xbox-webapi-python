import pytest
from betamax import Betamax

from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.common.exceptions import AuthenticationException
from xbox.webapi.authentication.two_factor import TwoFactorAuthentication
from xbox.webapi.authentication.two_factor import TwoFactorAuthMethods


def _2fa_with_stdin_patch(monkeypatch, cassette_name, inputs):
    auth_manager = AuthenticationManager()
    auth_manager.email_address = 'pyxb-testing@outlook.com'
    auth_manager.password = 'password'

    input_generator = (i for i in inputs)
    monkeypatch.setattr('builtins.input', lambda prompt: next(input_generator))

    with Betamax(auth_manager.session).use_cassette(cassette_name):
        auth_manager.authenticate()
    return auth_manager


def test_email_all_correct(monkeypatch):
    input_data = ['0', 'pyxb-testing@outlook.com', '1379343']
    ret = _2fa_with_stdin_patch(monkeypatch, '2fa_email_all_correct', input_data)

    assert ret.access_token.jwt == 'AccessToken'
    assert ret.refresh_token.jwt == 'RefreshToken'
    assert ret.user_token.jwt == 'UserToken'
    assert ret.xsts_token.jwt == 'XSTSToken'


def test_email_wrong_mail(monkeypatch):
    input_data = ['0', 'pyxxx-testing@outlook.com', '1234']
    with pytest.raises(AuthenticationException):
        _2fa_with_stdin_patch(monkeypatch, '2fa_email_wrong_mail', input_data)


def test_totp_correct(monkeypatch):
    input_data = ['2', '285371']
    ret = _2fa_with_stdin_patch(monkeypatch, '2fa_totp_correct', input_data)

    assert ret.access_token.jwt == 'AccessToken'
    assert ret.refresh_token.jwt == 'RefreshToken'
    assert ret.user_token.jwt == 'UserToken'
    assert ret.xsts_token.jwt == 'XSTSToken'


def test_totp_wrong_code(monkeypatch):
    input_data = ['2', '123456']
    with pytest.raises(AuthenticationException):
        _2fa_with_stdin_patch(monkeypatch, '2fa_totp_wrong_code', input_data)


def test_totp_v2_auth(monkeypatch):
    input_data = ['2']
    with pytest.raises(AuthenticationException):
        _2fa_with_stdin_patch(monkeypatch, '2fa_totpv2_accept', input_data)

def test_sms_all_correct(monkeypatch):
    input_data = ['1', '6842', '0135392']
    ret = _2fa_with_stdin_patch(monkeypatch, '2fa_sms_all_correct', input_data)

    assert ret.access_token.jwt == 'AccessToken'
    assert ret.refresh_token.jwt == 'RefreshToken'
    assert ret.user_token.jwt == 'UserToken'
    assert ret.xsts_token.jwt == 'XSTSToken'


def test_sms_wrong_number(monkeypatch):
    input_data = ['1', '9942', '123456']
    with pytest.raises(AuthenticationException):
        _2fa_with_stdin_patch(monkeypatch, '2fa_sms_wrong_number', input_data)

def test_no_auth_methods():
    auth_manager = AuthenticationManager()
    two_factor_auth = TwoFactorAuthentication(auth_manager.session)

    with pytest.raises(AuthenticationException):
        two_factor_auth.authenticate(server_data=dict())


def test_invalid_authmethod_choice(monkeypatch):
    auth_manager = AuthenticationManager()
    two_factor_auth = TwoFactorAuthentication(auth_manager.session)

    server_data = {
        'D': [
            {'type': TwoFactorAuthMethods.Voice, 'display': 'phone number **'},
            {'type': TwoFactorAuthMethods.Email, 'display': 'mail bla@bla.com'}
        ]
    }

    inputs = ['99']
    input_generator = (i for i in inputs)
    monkeypatch.setattr('builtins.input', lambda prompt: next(input_generator))

    with pytest.raises(AuthenticationException):
        two_factor_auth.authenticate(server_data)
