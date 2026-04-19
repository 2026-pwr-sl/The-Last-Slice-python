import datetime
import ipaddress

def ip_in_network(ip_str, network_str):
    ip = ipaddress.IPv4Address(ip_str)
    network = ipaddress.IPv4Network(network_str)
    return ip in network

def parse_timestamp(timestamp_str):
    date_part, time_part = timestamp_str.split(":", 1)
    day, month_str, year = date_part.split("/")

    month_map = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
        "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
        "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }

    month = month_map[month_str]

    hour, minute, second = time_part.split(":")

    return datetime.datetime(
        int(year),
        month,
        int(day),
        int(hour),
        int(minute),
        int(second)
    )

class LogEntry:
    def __init__(self, ip, timestamp_str, path, status, bytes_sent):
        self.ip = ipaddress.IPv4Address(ip)
        self.timestamp = parse_timestamp(timestamp_str)
        self.path = path
        self.status = int(status)
        self.bytes_sent = int(bytes_sent)

    def __str__(self):
        return f"{self.ip} [{self.timestamp}] {self.path} {self.status} {self.bytes_sent}"

    def __repr__(self):
        return (
            f"LogEntry(ip={self.ip}, "
            f"timestamp={self.timestamp}, "
            f"path='{self.path}', "
            f"status={self.status}, "
            f"bytes={self.bytes_sent})"
        )

    def is_success(self):
        return 200 <= self.status < 300

    def is_error(self):
        return 400 <= self.status < 600

    def is_from_network(self, network_str):
        network = ipaddress.IPv4Network(network_str)
        return self.ip in network

def parse_log_line(line, default_ip="127.0.0.1", base_time=None):
    parts = line.strip().split()

    if len(parts) != 4:
        raise ValueError(f"Invalid log line: {line}")

    path, status, bytes_sent, processing_time = parts

    if base_time is None:
        base_time = datetime.datetime(2020, 10, 18, 1, 0, 0)

    timestamp = base_time + datetime.timedelta(seconds=int(processing_time))

    timestamp_str = timestamp.strftime("%d/%b/%Y:%H:%M:%S")

    return LogEntry(default_ip, timestamp_str, path, status, bytes_sent)


def read_log_file(file_path):
    entries = []
    base_time = datetime.datetime(2020, 10, 18, 1, 0, 0)

    with open(file_path, "r") as f:
        for line in f:
            if line.strip():
                entry = parse_log_line(line, base_time=base_time)
                entries.append(entry)

    return entries

def display_requests_in_time_range(entries, start_time, end_time):
    if end_time < start_time:
        print("WARNING: End time is earlier than start time!")
        return
    for entry in entries:
        if start_time <= entry.timestamp <= end_time:
            print(entry)


if __name__ == "__main__":
    entries = read_log_file("log.txt")

    print("Loaded entries:", len(entries))

    print("First entry:", entries[0])

    start = parse_timestamp("18/Oct/2020:01:00:05")
    end = parse_timestamp("18/Oct/2020:01:00:20")

    print("\nFiltered entries:")
    display_requests_in_time_range(entries, start, end)