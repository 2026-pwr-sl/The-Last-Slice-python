import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def parse_log_line(line):
    """Parse a single log line and return a dictionary."""
    parts = line.strip().split()
    if len(parts) != 4:
        return None
    
    return {
        'path': parts[0],
        'status_code': int(parts[1]),
        'bytes_sent': int(parts[2]),
        'processing_time': int(parts[3])
    }

def main():
    logging.info("Start - Processing log file from standard input")
    
    # Read all lines from standard input
    lines = sys.stdin.readlines()
    logging.debug(f"Read {len(lines)} lines from input")
    
    # Parse all log entries
    entries = []
    for line_num, line in enumerate(lines, 1):
        entry = parse_log_line(line)
        if entry:
            entries.append(entry)
            logging.debug(f"Line {line_num} parsed: {entry}")
        else:
            logging.warning(f"Line {line_num} has invalid format: {line.strip()}")
    
    # Lists for tracking
    non_existent_paths = []
    total_bytes = 0
    total_processing_time = 0
    largest_resource = None
    largest_time = 0
    
    logging.debug(f"Processing {len(entries)} valid entries")
    
    for entry in entries:
        path = entry['path']
        status = entry['status_code']
        bytes_sent = entry['bytes_sent']
        processing_time = entry['processing_time']
        
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
    
    logging.info("End - Log processing completed successfully")

if __name__ == "__main__":
    main()