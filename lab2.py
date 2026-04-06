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
    
    logging.info("End - Log processing completed successfully")

if __name__ == "__main__":
    run()