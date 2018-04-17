import pytest
from betamax import Betamax

from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.common.exceptions import AuthenticationException, TwoFactorAuthRequired
from xbox.webapi.authentication.two_factor import TwoFactorAuthentication


def _do_2fa(cassette_name, strategy_index, proof=None, otc=None):
    auth_manager = AuthenticationManager()
    auth_manager.email_address = 'pyxb-testing@outlook.com'
    auth_manager.password = 'password'

    with Betamax(auth_manager.session).use_cassette(cassette_name):
        with pytest.raises(TwoFactorAuthRequired) as excinfo:
            auth_manager.authenticate()

        two_fa_auth = TwoFactorAuthentication(
            auth_manager.session, auth_manager.email_address, excinfo.value.server_data
        )
        two_fa_auth.check_otc(strategy_index, proof)
        access_token, refresh_token = two_fa_auth.authenticate(strategy_index, proof, otc)
        auth_manager.access_token = access_token
        auth_manager.refresh_token = refresh_token
        auth_manager.authenticate(do_refresh=False)
    return auth_manager


def test_email_all_correct():
    ret = _do_2fa('2fa_email_all_correct',
                  strategy_index=0, proof='pyxb-testing@outlook.com', otc='1379343')

    assert ret.access_token.jwt == 'AccessToken'
    assert ret.refresh_token.jwt == 'RefreshToken'
    assert ret.user_token.jwt == 'UserToken'
    assert ret.xsts_token.jwt == 'XSTSToken'


def test_email_wrong_mail():
    with pytest.raises(AuthenticationException):
        _do_2fa('2fa_email_wrong_mail',
                strategy_index=0, proof='pyxxx-testing@outlook.com', otc='1234')


def test_totp_correct():
    ret = _do_2fa('2fa_totp_correct',
                  strategy_index=2, otc='285371')

    assert ret.access_token.jwt == 'AccessToken'
    assert ret.refresh_token.jwt == 'RefreshToken'
    assert ret.user_token.jwt == 'UserToken'
    assert ret.xsts_token.jwt == 'XSTSToken'


def test_totp_wrong_code():
    with pytest.raises(AuthenticationException):
        _do_2fa('2fa_totp_wrong_code',
                strategy_index=2, otc='123456')


def test_totp_v2_auth_accept():
    ret = _do_2fa('2fa_totpv2_accept', strategy_index=3)

    assert ret.access_token.jwt == 'AccessToken'
    assert ret.refresh_token.jwt == 'RefreshToken'
    assert ret.user_token.jwt == 'UserToken'
    assert ret.xsts_token.jwt == 'XSTSToken'


def test_totp_v2_auth_reject():
    with pytest.raises(AuthenticationException):
        _do_2fa('2fa_totpv2_reject', strategy_index=3)


def test_sms_all_correct():
    ret = _do_2fa('2fa_sms_all_correct',
                  strategy_index=1, proof='6842', otc='0135392')

    assert ret.access_token.jwt == 'AccessToken'
    assert ret.refresh_token.jwt == 'RefreshToken'
    assert ret.user_token.jwt == 'UserToken'
    assert ret.xsts_token.jwt == 'XSTSToken'


def test_sms_wrong_number():
    with pytest.raises(AuthenticationException):
        _do_2fa('2fa_sms_wrong_number',
                strategy_index=1, proof='9942', otc='123456')


def test_no_auth_methods():
    auth_manager = AuthenticationManager()
    with pytest.raises(AuthenticationException):
        TwoFactorAuthentication(auth_manager.session, 'fake@mail.com', server_data=dict())


def test_invalid_authmethod_choice():
    server_data = {
        'D':
        [
            {
                'data': '<some data>', 'type': 1, 'display': 'pyxb-testing@outlook.com', 'otcEnabled': True,
                'otcSent': False, 'isLost': False, 'isSleeping': False, 'isSADef': True, 'isVoiceDef': False,
                'isVoiceOnly': False, 'pushEnabled': False
            }
        ]
    }

    auth_manager = AuthenticationManager()
    two_factor_auth = TwoFactorAuthentication(auth_manager.session, 'fake@mail.com', server_data)

    with pytest.raises(IndexError):
        two_factor_auth.authenticate(strategy_index=99, proof=None, otc='')
