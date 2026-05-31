"""Interactive configuration writer for lab 6."""

from __future__ import annotations

import json
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
VALID_LOGGING_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


def prompt_text(prompt: str, default: str) -> str:
    value = input(f"{prompt} [{default}]: ").strip()
    return value or default


def prompt_int(prompt: str, default: int) -> int:
    while True:
        value = input(f"{prompt} [{default}]: ").strip()
        if not value:
            return default

        try:
            return int(value)
        except ValueError:
            print("Please enter a valid integer.")


def prompt_logging_level(default: str) -> str:
    while True:
        value = input(f"Logging level {sorted(VALID_LOGGING_LEVELS)} [{default}]: ").strip()
        if not value:
            return default

        value = value.upper()
        if value in VALID_LOGGING_LEVELS:
            return value

        print("Please choose one of the supported logging levels.")


def build_config() -> dict[str, object]:
    """Collect configuration values from the user."""
    config = DEFAULT_CONFIG.copy()
    config["log_filename"] = prompt_text("Web server log file name", DEFAULT_CONFIG["log_filename"])
    config["ip_address_filter"] = prompt_text("IP address filter", DEFAULT_CONFIG["ip_address_filter"])
    config["request_method"] = prompt_text("Request method to display", DEFAULT_CONFIG["request_method"])
    config["logging_level"] = prompt_logging_level(DEFAULT_CONFIG["logging_level"])
    config["display_lines"] = prompt_int("Number of lines to display at once", DEFAULT_CONFIG["display_lines"])
    config["minimum_status_code"] = prompt_int(
        "Minimum HTTP status code to display", DEFAULT_CONFIG["minimum_status_code"]
    )
    return config


def save_config(config: dict[str, object], path: Path = CONFIG_PATH) -> Path:
    """Persist configuration values as UTF-8 JSON."""
    with path.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=2, ensure_ascii=False)
        file.write("\n")
    return path


def main() -> None:
    config = build_config()
    path = save_config(config)
    print(f"Configuration saved to {path}")


if __name__ == "__main__":
    main()