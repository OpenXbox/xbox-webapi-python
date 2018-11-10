from xbox.webapi.authentication.manager import AuthenticationManager


def test_extract_js_node(windows_live_authenticate_response):
    auth_manager = AuthenticationManager()
    js_node = auth_manager.extract_js_object(windows_live_authenticate_response, 'var ServerData')

    assert js_node is not None
    assert js_node['sFTTag'] == "<input name=\"PPFT\" value=\"normally_base64_encoded_string_here+\"/>"
    assert js_node['urlPost'] == "https://login.live.com/ppsecure/post.srf?response_type=token"

def test_extract_js_node_two(windows_live_authenticate_response_two_js_obj):
    auth_manager = AuthenticationManager()
    js_node = auth_manager.extract_js_object(windows_live_authenticate_response_two_js_obj, 'var ServerData')

    assert js_node is not None
    assert js_node['sFTTag'] == "<input type=\"hidden\" name=\"PPFT\" id=\"i0327\" value=\"normally_base64_encoded_string_here+\"/>"
    assert js_node['urlPost'] == "https://login.live.com/ppsecure/post.srf?response_type=token"