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
