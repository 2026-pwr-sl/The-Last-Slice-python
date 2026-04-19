import sys
import logging
from datetime import datetime
from ipaddress import IPv4Address, IPv4Network

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def parse_timestamp(timestamp_text):
    """Parse timestamp in format DD/Mon/YYYY:HH:MM:SS into datetime."""
    # Break the timestamp in small pieces using split(), then build datetime.
    day_part, rest = timestamp_text.split("/", 1)
    month_part, rest = rest.split("/", 1)
    year_part, time_part = rest.split(":", 1)
    hour_part, minute_part, second_part = time_part.split(":")

    month_number = datetime.strptime(month_part, "%b").month

    return datetime(
        int(year_part),
        month_number,
        int(day_part),
        int(hour_part),
        int(minute_part),
        int(second_part)
    )


def ipv4_belongs_to_network(ip_text, network_text):
    """Return True when IPv4 address is inside the IPv4 network."""
    # Convert text values into ipaddress objects and use the `in` operator.
    ip_obj = IPv4Address(ip_text)
    network_obj = IPv4Network(network_text, strict=False)
    return ip_obj in network_obj


class LogEntry:
    """Keep one parsed log line as an object.

    Each instance represents one request line from the log file.
    """

    def __init__(self, path, status_code, bytes_sent, processing_time):
        self.path = path
        self.status_code = status_code
        self.bytes_sent = bytes_sent
        self.processing_time = processing_time

    def __str__(self):
        # Human-friendly format (used when printing the object).
        return (
            f"{self.path} {self.status_code} "
            f"{self.bytes_sent} {self.processing_time}"
        )

    def __repr__(self):
        # Developer/debug format showing constructor-style data.
        return (
            "LogEntry("
            f"path={self.path!r}, "
            f"status_code={self.status_code}, "
            f"bytes_sent={self.bytes_sent}, "
            f"processing_time={self.processing_time}"
            ")"
        )

    @classmethod
    def from_line(cls, line_text):
        """Create LogEntry from one log line using split(), no regex."""
        # Skip blank lines in the input file.
        stripped = line_text.strip()
        if not stripped:
            return None

        # Expected line shape: <path> <status> <bytes> <processing_time>
        parts = stripped.split()
        if len(parts) != 4:
            raise ValueError(f"Invalid log line format: {line_text!r}")

        return cls(
            path=parts[0],
            status_code=int(parts[1]),
            bytes_sent=int(parts[2]),
            processing_time=int(parts[3])
        )

    def is_success(self):
        # 2xx means success in HTTP status codes.
        return 200 <= self.status_code < 300

    def is_client_error(self):
        # 4xx means the request failed because of client-side issue.
        return 400 <= self.status_code < 500

    def is_server_error(self):
        # 5xx means the request failed because of server-side issue.
        return 500 <= self.status_code < 600

def read_log():
    """Read stdin log lines and return a list of LogEntry objects."""
    # Read all lines from standard input (e.g., `python lab2.py < log.txt`).
    lines = sys.stdin.readlines()
    logging.debug(f"Read {len(lines)} total line(s) from standard input.")

    entries = []
    for line in lines:
        # Parse each line into a LogEntry object.
        entry = LogEntry.from_line(line)
        if entry is not None:
            entries.append(entry)

    logging.debug(f"Parsed {len(entries)} non-empty log entrie(s) into the list.")
    return entries

def successful_reads(entries):
    # Keep only entries with 2xx status code.
    result = [entry for entry in entries if entry.is_success()]
    logging.info(f"Successful entries: {len(result)}")
    return result

def failed_reads(entries):
    # Collect both client errors (4xx) and server errors (5xx).
    errors_4xx = [entry for entry in entries if entry.is_client_error()]
    errors_5xx = [entry for entry in entries if entry.is_server_error()]

    logging.info(f"4xx errors: {len(errors_4xx)}")
    logging.info(f"5xx errors: {len(errors_5xx)}")

    return errors_4xx + errors_5xx

def html_entries(entries):
    # Successful requests that target HTML files only.
    return [
        entry for entry in entries
        if entry.is_success() and entry.path.endswith(".html")
    ]

def print_html_entries(entries):
    # Print entries one by one using LogEntry.__str__.
    htmls = html_entries(entries)
    for entry in htmls:
        print(entry)

def run():
    # Main workflow: read log, compute metrics, print summary.
    logging.info("Start - Processing log file from standard input")
    entries = read_log()
    
    # Lists for tracking
    non_existent_paths = []
    total_bytes = 0
    total_processing_time = 0
    largest_resource = None
    largest_time = 0
    
    logging.debug(f"Processing {len(entries)} valid entries")
    
    for entry in entries:
        # Unpack fields into local variables for readability.
        path = entry.path
        status = entry.status_code
        bytes_sent = entry.bytes_sent
        processing_time = entry.processing_time

        # Track non-existent resources (404)
        if status == 404:
            non_existent_paths.append(path)
            print(f"! {path}")
        
        # Track total bytes
        total_bytes += bytes_sent
        
        # Track total processing time for average
        total_processing_time += processing_time
        
        # Find largest resource by processing time
        if processing_time > largest_time:
            largest_time = processing_time
            largest_resource = path
    
    # Calculate kilobytes (1 KB = 1024 bytes)
    total_kilobytes = total_bytes / 1024
    
    # Calculate average processing time
    avg_processing_time = total_processing_time / len(entries) if entries else 0
    
    # Print results
    print("\n" + "="*50)
    print("SUMMARY REPORT")
    print("="*50)
    
    if largest_resource:
        print(f"Largest resource (by processing time): {largest_resource}")
        print(f"Processing time: {largest_time} ms")
    
    print(f"Number of failed requests (404): {len(non_existent_paths)}")
    print(f"Total bytes sent: {total_bytes} B")
    print(f"Total kilobytes sent: {total_kilobytes:.2f} KB")
    print(f"Average processing time: {avg_processing_time:.2f} ms")

    successful = successful_reads(entries)
    failed = failed_reads(entries)
    print(f"Successful entries: {len(successful)}")
    print(f"Failed entries: {len(failed)}")
    print_html_entries(entries)

    # End marker for logs.
    logging.info("End - Log processing completed successfully")

if __name__ == "__main__":
    # Run the script only when this file is executed directly.
    run()