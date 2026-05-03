from dataclasses import dataclass
import re


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
	if len(parts) != 3:
		raise ValueError(
			"request_string must have exactly 3 parts: METHOD PATH PROTOCOL"
		)

	request_type, resource_path, protocol_type = parts

	if not resource_path.startswith("/"):
		raise ValueError("resource path must start with '/'")

	protocol_pattern = r"^HTTP/?\d+\.\d+$"
	if not re.match(protocol_pattern, protocol_type):
		raise ValueError("protocol type must look like HTTP/1.1 or HTTP1.1")

	return HttpRequest(
		request_type=request_type,
		resource_path=resource_path,
		protocol_type=protocol_type,
	)
