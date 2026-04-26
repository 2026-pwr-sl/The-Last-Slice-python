def read_log(filename):
    """
    Read Apache log file and return entries as a dictionary.
    
    Based on Apache Common Log Format (CLF):
    %h %l %u %t \"%r\" %>s %b
    From: https://httpd.apache.org/docs/2.4/logs.html#common
    """
    log_data = {}
    
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            
            # According to Apache docs: format is:
            # IP - - [timestamp] "request" status size
            before, request, after = line.split('"')
            
            # Parse %h (client IP), %l (RFC 1413), %u (user), %t (time)
            before_parts = before.split()
            ip = before_parts[0]  # %h - client IP address
            # %l and %u are the '-' fields (not used in this lab)
            # %t - timestamp, removing brackets [ ]
            date = before_parts[3].strip('[').strip(']') if len(before_parts) > 3 else ""
            
            # Parse %>s (status) and %b (response size)
            after_parts = after.strip().split()
            status = int(after_parts[0]) if after_parts else 0  # %>s - status code
            # %b - size in bytes, '-' means 0
            size = 0 if len(after_parts) < 2 or after_parts[1] == "-" else int(after_parts[1])
            
            # Store the entry
            if ip not in log_data:
                log_data[ip] = []
            
            log_data[ip].append({
                "date": date,
                "request": request,  # \"%r\" - request line
                "status": status,
                "size": size
            })
    
    return log_data


# Global cache
_log_data = None


def get_log_data(filename="logfile.txt"):
    """Helper function to ensure log data is loaded only once."""
    global _log_data
    if _log_data is None:
        _log_data = read_log(filename)
    return _log_data


def ip_requests_number(ip_address):
    """Return number of requests from a given IP address."""
    log_data = get_log_data()
    return len(log_data.get(ip_address, []))


def ip_find(most_active=True):
    """Return IPs with most (most_active=True) or least (most_active=False) requests."""
    log_data = get_log_data()
    
    if not log_data:
        return []
    
    ip_requests = {ip: len(requests) for ip, requests in log_data.items()}
    
    if most_active:
        target = max(ip_requests.values())
    else:
        target = min(ip_requests.values())
    
    return [ip for ip, count in ip_requests.items() if count == target]


def longest_request():
    """Return the longest request string along with its IP address."""
    log_data = get_log_data()
    
    longest_request_str = ""
    longest_ip = ""
    max_length = 0
    
    for ip, entries in log_data.items():
        for entry in entries:
            request = entry["request"]
            if len(request) > max_length:
                max_length = len(request)
                longest_request_str = request
                longest_ip = ip
    
    return longest_ip, longest_request_str


def non_existent():
    """Return unique request strings that resulted in HTTP 404."""
    log_data = get_log_data()
    
    unique_404 = set()
    for ip, entries in log_data.items():
        for entry in entries:
            if entry["status"] == 404:
                unique_404.add(entry["request"])
    
    return list(unique_404)


def run(filename="logfile.txt"):
    """Main function that calls all remaining functions."""
    print(f"Analyzing log file: {filename}")
    print("Based on Apache Common Log Format (CLF)")
    print("Documentation: https://httpd.apache.org/docs/2.4/logs.html#common\n")
    
    log_data = get_log_data(filename)
    
    print(f"Total unique IPs: {len(log_data)}")
    print(f"Total requests: {sum(len(e) for e in log_data.values())}")
    
    print("\n--- IP Request Counts  ---")
    if log_data:
        sample_ip = list(log_data.keys())[0]
        print(f"Requests from {sample_ip}: {ip_requests_number(sample_ip)}")
    
    print("\n--- Most/Least Active IPs ---")
    print(f"Most active: {ip_find(most_active=True)}")
    print(f"Least active: {ip_find(most_active=False)}")
    
    print("\n--- Longest Request ---")
    ip, req = longest_request()
    print(f"IP: {ip}\nRequest: {req}")
    
    print("\n--- Non-existent Pages (404) ---")
    print(f"Unique 404 requests: {non_existent()}")


if __name__ == "__main__":
    run()