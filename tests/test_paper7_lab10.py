import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from paper7_lab10 import HttpRequest, reqstr2obj


def test_1_reqstr2obj_raises_type_error_when_input_is_not_string():
    with pytest.raises(TypeError):
        reqstr2obj(123)


def test_2_reqstr2obj_returns_http_request_object_for_get_root_http11():
    result = reqstr2obj("GET / HTTP1.1")
    assert isinstance(result, HttpRequest)


def test_3_reqstr2obj_sets_attributes_for_get_root_http11():
    result = reqstr2obj("GET / HTTP1.1")

    assert isinstance(result, HttpRequest)
    assert result.request_type == "GET"
    assert result.resource_path == "/"
    assert result.protocol_type == "HTTP1.1"


def test_reqstr2obj_returns_http_request_object():
    result = reqstr2obj("GET /index.html HTTP/1.1")

    assert isinstance(result, HttpRequest)
    assert result.request_type == "GET"
    assert result.resource_path == "/index.html"
    assert result.protocol_type == "HTTP/1.1"


def test_reqstr2obj_raises_value_error_for_invalid_number_of_parts():
    with pytest.raises(ValueError):
        reqstr2obj("GET /index.html")


def test_reqstr2obj_raises_value_error_for_invalid_resource_path():
    with pytest.raises(ValueError):
        reqstr2obj("GET index.html HTTP/1.1")


def test_reqstr2obj_raises_value_error_for_invalid_protocol_prefix():
    with pytest.raises(ValueError):
        reqstr2obj("GET /index.html HTTPS/1.1")

def test_4_multiple_valid_requests():
    cases = [
        ("GET / HTTP1.1", ("GET", "/", "HTTP1.1")),
        ("POST /form HTTP1.0", ("POST", "/form", "HTTP1.0")),
        ("DELETE /item HTTP2.0", ("DELETE", "/item", "HTTP2.0")),
    ]

    for req, expected in cases:
        result = reqstr2obj(req)
        assert (result.request_type, result.resource_path, result.protocol_type) == expected


##def test_5_returns_none_for_invalid_parts():
    ##assert reqstr2obj("GET /index.html") is None


def test_6_bad_request_type():
    from paper7_lab10 import BadRequestTypeError

    with pytest.raises(BadRequestTypeError):
        reqstr2obj("DOWNLOAD /movie.mp4 HTTP1.1")


def test_7_bad_http_version():
    from paper7_lab10 import BadHTTPVersion

    with pytest.raises(BadHTTPVersion):
        reqstr2obj("GET /index.html HTTP3.0")


def test_8_path_error_message():
    with pytest.raises(ValueError, match="Path must start with /"):
        reqstr2obj("GET index.html HTTP1.1")


if __name__ == "__main__":
    exit_code = pytest.main([__file__, "-v"])
    if exit_code == 0:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some tests failed!")
    sys.exit(exit_code)
