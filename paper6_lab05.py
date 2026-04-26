def read_log(filename):
    """Read Apache log file and return entries as a dictionary."""
    log_data = {}
    
    with open(filename, "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            line = line.strip()
            
            if not line:
                continue
            
            before, request, after = line.split('"')
            
            before_parts = before.split()
            ip = before_parts[0]
            date = before_parts[3].strip('[') if len(before_parts) > 3 else ""
            
            after_parts = after.strip().split()
            status = int(after_parts[0]) if after_parts else 0
            size = 0 if len(after_parts) < 2 or after_parts[1] == "-" else int(after_parts[1])
            
            # Using IP as key - this is the answer to "Can any log entry field be used as a key?"
            # But note: if same IP appears multiple times, we need to store multiple entries
            if ip not in log_data:
                log_data[ip] = []
            log_data[ip].append({
                "date": date,
                "request": request,
                "status": status,
                "size": size
            })
    
    return log_data

_log_data = None

def get_log_data():
    """Helper function to ensure log data is loaded."""
    global _log_data
    if _log_data is None:
        _log_data = read_log("logfile.txt")
    return _log_data


def ip_requests_number(ip_address):
    """Return number of requests from a given IP address."""
    log_data = get_log_data()
    if ip_address in log_data:
        return len(log_data[ip_address])
    return 0


def run():
    """Main function that calls the remaining functions."""
    filename = "logfile.txt"
    log_data = read_log(filename)
    
    print("Task 4: Log data loaded")
    print(f"Total unique IPs: {len(log_data)}")
    print(f"Total requests: {sum(len(entries) for entries in log_data.values())}")
    
    # Show first IP and its requests
    first_ip = list(log_data.keys())[0]
    print(f"Sample - IP: {first_ip}, Requests: {len(log_data[first_ip])}\n")
    
    # Test ip_requests_number
    print("Testing ip_requests_number")
    test_ip = "192.168.1.10"
    count = ip_requests_number(test_ip)
    print(f"Requests from {test_ip}: {count}")
    
    test_ip2 = "10.0.0.15"
    count2 = ip_requests_number(test_ip2)
    print(f"Requests from {test_ip2}: {count2}")


if __name__ == "__main__":
    run()