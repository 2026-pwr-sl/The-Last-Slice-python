from dataclasses import dataclass
import re

class BadRequestTypeError(Exception):
    pass

class BadHTTPVersion(Exception):
    pass

VALID_METHODS = {"GET", "POST", "PUT", "DELETE", "PATCH"}
VALID_PROTOCOLS = {"HTTP1.0", "HTTP1.1", "HTTP2.0", "HTTP/1.0", "HTTP/1.1", "HTTP/2.0"}

@dataclass(frozen=True)
class HttpRequest:
    """Simple representation of an HTTP request line."""
    request_type: str
    resource_path: str
    protocol_type: str

def reqstr2obj(request_string):
    """Function gets text HTTP request and returns HTTP request object."""
    if not isinstance(request_string, str):
        raise TypeError("request_string must be a string")

    text = request_string.strip()
    if not text:
        raise ValueError("request_string cannot be empty")

    parts = text.split()
    
    # FIX: Must raise ValueError for the test to pass (not return None)
    if len(parts) != 3:
        raise ValueError("Request must have exactly 3 parts")

    request_type, resource_path, protocol_type = parts

    if request_type not in VALID_METHODS:
        raise BadRequestTypeError("Invalid request type")

    if not resource_path.startswith("/"):
        raise ValueError("Path must start with /")

    # FIX: Explicitly catch HTTPS to raise ValueError as per test requirement
    if not protocol_type.startswith("HTTP") or protocol_type.startswith("HTTPS"):
        raise ValueError("Invalid protocol prefix")

    if protocol_type not in VALID_PROTOCOLS:
        raise BadHTTPVersion("Invalid HTTP version")

    return HttpRequest(
        request_type=request_type,
        resource_path=resource_path,
        protocol_type=protocol_type,
    )