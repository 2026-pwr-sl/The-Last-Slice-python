import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def read_log():
    """Read stdin log lines and return a list of typed tuple entries."""
    lines = sys.stdin.readlines()
    logging.debug(f"Read {len(lines)} total line(s) from standard input.")

    entries = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        parts = stripped.split()
        entry = (
            parts[0],
            int(parts[1]),
            int(parts[2]),
            int(parts[3])
        )
        entries.append(entry)

    logging.debug(f"Parsed {len(entries)} non-empty log entrie(s) into the list.")
    return entries

def successful_reads(entries):
    result = [e for e in entries if 200 <= e[1] < 300]
    logging.info(f"Successful entries: {len(result)}")
    return result

def failed_reads(entries):
    errors_4xx = [e for e in entries if 400 <= e[1] < 500]
    errors_5xx = [e for e in entries if 500 <= e[1] < 600]

    logging.info(f"4xx errors: {len(errors_4xx)}")
    logging.info(f"5xx errors: {len(errors_5xx)}")

    return errors_4xx + errors_5xx

def html_entries(entries):
    return [
        e for e in entries
        if 200 <= e[1] < 300 and e[0].endswith(".html")
    ]

def print_html_entries(entries):
    htmls = html_entries(entries)
    for e in htmls:
        print(e)

def run():
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
        path, status, bytes_sent, processing_time = entry
        
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

    
    logging.info("End - Log processing completed successfully")

if __name__ == "__main__":
    run()