"""Lab 6 log analyzer with JSON configuration support."""

from __future__ import annotations

import json
import logging
from collections import Counter
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"
DEFAULT_CONFIG = {
    "log_filename": "logfile.txt",
    "ip_address_filter": "",
    "request_method": "GET",
    "logging_level": "INFO",
    "display_lines": 10,
    "minimum_status_code": 0,
}


def parse_log_line(line: str) -> dict[str, object]:
    """Parse a single Apache common log format line."""
    before, request, after = line.split('"')
    assert len(request.split()) >= 2  # Helps debug malformed request fields before method extraction fails.

    before_parts = before.split()
    ip = before_parts[0]
    date = before_parts[3].strip("[]") if len(before_parts) > 3 else ""

    after_parts = after.strip().split()
    status = int(after_parts[0]) if after_parts else 0
    size = 0 if len(after_parts) < 2 or after_parts[1] == "-" else int(after_parts[1])

    return {
        "ip": ip,
        "date": date,
        "request": request,
        "method": request.split()[0] if request.split() else "",
        "status": status,
        "size": size,
    }


def load_log_data(filename: str | Path) -> list[dict[str, object]]:
    """Read Apache log data from a UTF-8 text file."""
    path = Path(filename)
    if not path.is_absolute():
        path = BASE_DIR / path

    entries: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()
            if not line:
                continue

            try:
                entries.append(parse_log_line(line))
            except (ValueError, IndexError):
                logging.warning("Skipping malformed log line: %s", line)

    return entries


def load_config(path: str | Path = CONFIG_PATH) -> dict[str, object]:
    """Load configuration from JSON, falling back to defaults when needed."""
    resolved_path = Path(path)
    if not resolved_path.is_absolute():
        resolved_path = BASE_DIR / resolved_path

    config = DEFAULT_CONFIG.copy()
    try:
        with resolved_path.open("r", encoding="utf-8") as file:
            loaded = json.load(file)
    except FileNotFoundError:
        logging.info("Configuration file %s does not exist. Using default values.", resolved_path)
        return config
    except json.JSONDecodeError as error:
        logging.error("Configuration file %s is not valid JSON: %s", resolved_path, error)
        raise

    if not isinstance(loaded, dict):
        logging.info(
            "Configuration file %s does not contain a JSON object. Using default values.",
            resolved_path,
        )
        return config

    missing_keys = [key for key in DEFAULT_CONFIG if key not in loaded]
    if missing_keys:
        logging.info(
            "Configuration file %s is missing %s. Using default values for them.",
            resolved_path,
            ", ".join(missing_keys),
        )

    config.update(loaded)
    config["log_filename"] = str(config.get("log_filename", DEFAULT_CONFIG["log_filename"]))
    config["ip_address_filter"] = str(config.get("ip_address_filter", DEFAULT_CONFIG["ip_address_filter"]))
    config["request_method"] = str(config.get("request_method", DEFAULT_CONFIG["request_method"])).upper()
    config["logging_level"] = str(config.get("logging_level", DEFAULT_CONFIG["logging_level"])).upper()

    try:
        raw_display_lines = int(config.get("display_lines", DEFAULT_CONFIG["display_lines"]))
        if raw_display_lines <= 0:
            logging.warning(
                "Configuration file %s sets display_lines=%s. Using 1 so paging still works.",
                resolved_path,
                raw_display_lines,
            )
            raw_display_lines = 1
        config["display_lines"] = raw_display_lines
    except (TypeError, ValueError):
        config["display_lines"] = DEFAULT_CONFIG["display_lines"]

    try:
        config["minimum_status_code"] = max(
            0, int(config.get("minimum_status_code", DEFAULT_CONFIG["minimum_status_code"]))
        )
    except (TypeError, ValueError):
        config["minimum_status_code"] = DEFAULT_CONFIG["minimum_status_code"]

    return config


def filter_entries(
    entries: list[dict[str, object]],
    ip_address_filter: str = "",
    minimum_status_code: int = 0,
) -> list[dict[str, object]]:
    """Return entries that match the configured filters."""
    filtered_entries = []
    for entry in entries:
        if ip_address_filter and entry["ip"] != ip_address_filter:
            continue
        if int(entry["status"]) < minimum_status_code:
            continue
        filtered_entries.append(entry)
    return filtered_entries


def ip_requests_number(entries: list[dict[str, object]], ip_address: str) -> int:
    return sum(1 for entry in entries if entry["ip"] == ip_address)


def ip_find(entries: list[dict[str, object]], most_active: bool = True) -> list[str]:
    if not entries:
        return []

    counts = Counter(entry["ip"] for entry in entries)
    target = max(counts.values()) if most_active else min(counts.values())
    return [ip for ip, count in counts.items() if count == target]


def longest_request(entries: list[dict[str, object]]) -> tuple[str, str]:
    longest_ip = ""
    longest_request_text = ""

    for entry in entries:
        request_text = str(entry["request"])
        if len(request_text) > len(longest_request_text):
            longest_request_text = request_text
            longest_ip = str(entry["ip"])

    return longest_ip, longest_request_text


def request_method_requests(entries: list[dict[str, object]], request_method: str) -> list[dict[str, object]]:
    return [entry for entry in entries if str(entry.get("method", "")).upper() == request_method.upper()]


def non_existent(entries: list[dict[str, object]]) -> list[str]:
    requests = {str(entry["request"]) for entry in entries if int(entry["status"]) == 404}
    return sorted(requests)


def format_entry(entry: dict[str, object]) -> str:
    return (
        f'{entry["ip"]} | {entry["date"]} | {entry["request"]} | '
        f'{entry["status"]} | {entry["size"]}'
    )


def display_entries(entries: list[dict[str, object]], display_lines: int) -> None:
    if not entries:
        print("No log entries matched the configured filters.")
        return

    if display_lines <= 0:
        logging.warning("display_lines must be greater than zero. Using 1 to continue paging.")
        display_lines = 1

    for start in range(0, len(entries), display_lines):
        chunk = entries[start : start + display_lines]
        for entry in chunk:
            print(format_entry(entry))

        if start + display_lines < len(entries):
            input(f"--- showing {start + len(chunk)} of {len(entries)} entries. Press Enter to continue ---")


def display_requests_for_method(entries: list[dict[str, object]], request_method: str, display_lines: int) -> None:
    method_entries = request_method_requests(entries, request_method)

    print()
    print(f"Requests using method {request_method.upper()}: {len(method_entries)}")
    display_entries(method_entries, display_lines)


def process_custom_parameter(entries: list[dict[str, object]], minimum_status_code: int) -> None:
    """Custom log processing controlled by the user-defined configuration value."""
    assert minimum_status_code >= 0  # Helps catch invalid debug/test inputs before the filter is applied.

    interesting_entries = [entry for entry in entries if int(entry["status"]) >= minimum_status_code]
    print()
    print(f"Custom parameter - requests with status >= {minimum_status_code}: {len(interesting_entries)}")
    if interesting_entries:
        print(f"First matching request: {interesting_entries[0]['request']}")


def run(config_path: str | Path = CONFIG_PATH) -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    try:
        config = load_config(config_path)
    except json.JSONDecodeError:
        raise SystemExit(1)

    logging.getLogger().setLevel(getattr(logging, str(config["logging_level"]), logging.INFO))

    log_filename = config["log_filename"]
    try:
        entries = load_log_data(log_filename)
    except FileNotFoundError:
        resolved_path = Path(log_filename)
        if not resolved_path.is_absolute():
            resolved_path = BASE_DIR / resolved_path
        logging.error("Log file %s does not exist. Update the configuration and try again.", resolved_path)
        raise SystemExit(1)

    filtered_entries = filter_entries(
        entries,
        ip_address_filter=str(config["ip_address_filter"]),
        minimum_status_code=int(config["minimum_status_code"]),
    )

    print(f"Configuration file: {Path(config_path)}")
    print(f"Log file: {log_filename}")
    print(f"Logging level: {config['logging_level']}")
    print(f"IP filter: {config['ip_address_filter'] or 'ALL'}")
    print(f"Request method: {config['request_method']}")
    print(f"Display lines at once: {config['display_lines']}")
    print(f"Minimum status code: {config['minimum_status_code']}")
    print()

    display_entries(filtered_entries, int(config["display_lines"]))
    display_requests_for_method(filtered_entries, str(config["request_method"]), int(config["display_lines"]))
    process_custom_parameter(filtered_entries, int(config["minimum_status_code"]))

    print()
    print(f"Total unique IPs: {len({entry['ip'] for entry in filtered_entries})}")
    print(f"Total requests: {len(filtered_entries)}")

    if filtered_entries:
        sample_ip = str(filtered_entries[0]["ip"])
        print(f"Requests from {sample_ip}: {ip_requests_number(filtered_entries, sample_ip)}")

    print(f"Most active: {ip_find(filtered_entries, most_active=True)}")
    print(f"Least active: {ip_find(filtered_entries, most_active=False)}")

    longest_ip, longest_request_text = longest_request(filtered_entries)
    print(f"Longest request IP: {longest_ip}")
    print(f"Longest request: {longest_request_text}")

    print(f"Unique 404 requests: {non_existent(filtered_entries)}")


if __name__ == "__main__":
    run()