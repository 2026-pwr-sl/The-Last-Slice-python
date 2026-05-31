import re
import sys
import os


def read_config(config_file="lab.config"):
    """Read configuration file and return settings."""

    # Check if config file exists
    if not os.path.exists(config_file):
        print(f"Error: Config file '{config_file}' not found!")
        sys.exit(1)

    config_data = {
        "Display": {},
        "LogFile": {},
        "Config": {}
    }

    current_section = None

    with open(config_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Check for section header [Section]
            section_match = re.match(r'^\[(\w+)\]$', line)
            if section_match:
                current_section = section_match.group(1)
                continue

            # Check for parameter=value
            if current_section and '=' in line:
                param_match = re.match(r'^(\w+)=(.+)$', line)
                if param_match:
                    key, value = param_match.groups()
                    config_data[current_section][key] = value

    # Set default values if missing
    config_data["Display"].setdefault("lines_per_page", "10")
    config_data["Display"].setdefault("separator", " | ")
    config_data["LogFile"].setdefault("filename", "access.log")
    config_data["Config"].setdefault("filter", "GET")

    return config_data


def read_log_file(filename):
    """Read log file into memory as list of lines."""

    if not os.path.exists(filename):
        print(f"Error: Log file '{filename}' not found!")
        sys.exit(1)

    with open(filename, "r", encoding="utf-8") as file:
        return file.readlines()


def parse_log_line(line):
    """Parse a single log line using regular expressions."""

    # Regex pattern for Apache common log format
    pattern = (
        r'^(\d+\.\d+\.\d+\.\d+) - - \[([^\]]+)\] '
        r'"([^"]+)" (\d+) (\d+|-)$'
    )

    line = line.strip()
    if not line:
        return None

    match = re.match(pattern, line)

    if not match:
        return None

    ip, timestamp, request, status, size = match.groups()

    # Convert to appropriate data types
    status_code = int(status)
    response_size = 0 if size == '-' else int(size)

    return {
        "ip": ip,
        "timestamp": timestamp,
        "request": request,
        "status": status_code,
        "size": response_size
    }


def parse_all_logs(log_lines):
    """Parse all log lines and return list of entry objects."""

    entries = []
    for line in log_lines:
        entry = parse_log_line(line)
        if entry:  # Only add if parsing succeeded
            entries.append(entry)

    return entries


def ip_to_int(ip):
    """Convert IP address string to integer."""
    parts = ip.split('.')
    return (int(parts[0]) << 24) + (int(parts[1]) << 16) + \
           (int(parts[2]) << 8) + int(parts[3])


def ip_in_subnet(ip_address, subnet_cidr=24):
    """Check if IP address belongs to given subnet."""
    ip_int = ip_to_int(ip_address)
    mask = (0xFFFFFFFF << (32 - subnet_cidr)) & 0xFFFFFFFF
    return (ip_int & mask) == (ip_int & mask)


def print_requests_by_subnet(entries, config):
    """Print requests from specific IP subnet with pagination."""

    # Using student ID
    student_index = 288397
    mask_length = (student_index % 16) + 8

    print(
        f"\n=== Student ID: {student_index}, Subnet mask: /{mask_length} ===")

    lines_per_page = int(config["Display"].get("lines_per_page", 10))

    filtered_entries = []
    for entry in entries:
        if ip_in_subnet(entry["ip"], mask_length):
            filtered_entries.append(entry)

    if not filtered_entries:
        print("No entries found for this subnet.")
        return

    print(f"Total entries in subnet: {len(filtered_entries)}\n")

    # Display with pagination
    for i, entry in enumerate(filtered_entries):
        print(f"{entry['ip']} - {entry['request']} - "
              f"{entry['status']} - {entry['size']} bytes")

        if (i + 1) % lines_per_page == 0 and i + 1 < len(filtered_entries):
            input("Press Enter to continue...")


def print_requests_by_browser(entries, browser_name="Chrome"):
    """Print requests from specific browser."""

    browser_patterns = {
        "Chrome": r"Chrome",
        "Firefox": r"Firefox",
        "Safari": r"Safari",
        "Edge": r"Edge"
    }

    pattern = browser_patterns.get(browser_name, browser_name)

    found = False
    print(f"\n=== Requests from {browser_name} browser ===")

    for entry in entries:
        if re.search(pattern, entry["request"], re.IGNORECASE):
            print(f"{entry['ip']} - {entry['request']} - {entry['status']}")
            found = True

    if not found:
        print(f"No {browser_name} requests found.")


def print_total_bytes_by_filter(entries, config):
    """Print total bytes for filtered request type."""

    request_filter = config["Config"].get("filter", "GET")
    separator = config["Display"].get("separator", " | ")

    total_bytes = 0
    count = 0

    for entry in entries:
        if re.search(request_filter, entry["request"]):
            total_bytes += entry["size"]
            count += 1

    print(f"\n=== Total Bytes by Request Type ===")
    print(f"Filter{separator}{request_filter}")
    print(f"Total Requests{separator}{count}")
    print(f"Total Bytes{separator}{total_bytes}")


def main():
    """Main application function."""

    print("=" * 50)
    print("Lab07 - Apache Log Analyzer")
    print("=" * 50)

    # Task 1: Read configuration
    print("\n[1] Loading configuration...")
    config = read_config("lab.config")
    print(f"    Config loaded: Display lines="
          f"{config['Display']['lines_per_page']}")

    # Task 2: Read log file
    print("\n[2] Reading log file...")
    log_filename = config["LogFile"].get("filename", "access.log")
    log_lines = read_log_file(log_filename)
    print(f"    Read {len(log_lines)} lines from {log_filename}")

    # Task 4: Parse all logs
    print("\n[3] Parsing log entries...")
    entries = parse_all_logs(log_lines)
    print(f"    Parsed {len(entries)} valid log entries")

    # Task 5: Print by subnet
    print_requests_by_subnet(entries, config)

    # Task 6: Print by browser
    print_requests_by_browser(entries, "Chrome")

    # Task 7: Total bytes by filter
    print_total_bytes_by_filter(entries, config)

    print("\n" + "=" * 50)
    print("Lab07 completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    main()
