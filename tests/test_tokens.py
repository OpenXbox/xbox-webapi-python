import pytest

from datetime import datetime, timedelta

from xbox.webapi.authentication.token import Token, AccessToken, RefreshToken, XSTSToken, UserToken


def test_token_validity(jwt):
    time_now = datetime.utcnow()
    time_minus_1day = time_now - timedelta(days=1)
    time_minus_14days = time_now - timedelta(days=14)
    time_plus_14days = time_now + timedelta(days=14)

    token_invalid = Token(jwt, time_minus_14days, time_minus_1day)
    token_valid = Token(jwt, time_now, time_plus_14days)

    assert token_invalid.is_valid is False
    assert token_valid.is_valid is True

    assert token_valid.date_issued == time_now
    assert token_valid.date_valid == time_plus_14days


def test_access_refresh_token_validity(jwt):
    access_token_invalid = AccessToken(jwt, 0)
    access_token_120seconds = AccessToken(jwt, 120)
    refresh_token_14days = RefreshToken(jwt)

    assert access_token_invalid.is_valid is False
    assert access_token_120seconds.is_valid is True
    assert refresh_token_14days.is_valid is True
    assert access_token_invalid.jwt == jwt


def test_token_string_conversion(jwt, token_timestring, token_datetime):
    token_datestring = Token(jwt, token_timestring, token_timestring)

    assert token_datestring.date_issued == token_datetime


def test_token_from_dict(jwt, token_timestring, token_datetime):
    token_dict = UserToken(jwt, token_timestring, token_timestring).to_dict()

    token = Token.from_dict(token_dict)

    # Invalid Name
    token_dict['name'] = 'InvalidTokenName'
    with pytest.raises(ValueError):
        Token.from_dict(token_dict)

    assert token.jwt == jwt
    assert token.date_valid == token_datetime


def test_token_to_dict(jwt, token_timestring, token_datetime):
    token_dict = XSTSToken(jwt, token_timestring, token_timestring).to_dict()

    assert token_dict['name'] == 'XSTSToken'
    assert token_dict['jwt'] == jwt
    assert token_dict['date_valid'] == token_timestring
    assert token_dict['date_issued'] == token_timestring
