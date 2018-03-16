import pytest
from xbox.webapi.common.userinfo import XboxLiveUserInfo
from xbox.webapi.authentication.token import AccessToken, RefreshToken, UserToken, XSTSToken


def test_extract_js_node(auth_manager, windows_live_authenticate_response):
    js_node = auth_manager._extract_js_object(windows_live_authenticate_response, 'ServerData')

    assert js_node is not None
    assert js_node['sFTTag'] == "<input name=\"PPFT\" value=\"normally_base64_encoded_string_here+\"/>"
    assert js_node['urlPost'] == "https://login.live.com/ppsecure/post.srf?response_type=token"


@pytest.mark.skip()
def test_auth_with_credentials(auth_manager):
    result_tuple = auth_manager.authenticate(email_address="", password="")
    access, refresh, user, xsts, userinfo = result_tuple

    assert access.token is not None
    assert access.is_valid is True
    assert isinstance(access, AccessToken) is True

    assert refresh.token is not None
    assert refresh.is_valid is True
    assert isinstance(refresh, RefreshToken) is True

    assert user.token is not None
    assert user.is_valid is True
    assert isinstance(user, UserToken) is True

    assert xsts.token is not None
    assert xsts.is_valid is True
    assert isinstance(xsts, XSTSToken) is True

    assert userinfo is not None
    assert isinstance(userinfo, XboxLiveUserInfo) is True
