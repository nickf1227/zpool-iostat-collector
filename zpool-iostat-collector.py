import sys
import csv
import os
import subprocess
import time
import re

# Debug print: script start
print("Starting zpool_iostat script...")

# Configurable settings
POOL_NAME = "tank"               # ZFS pool name
SAMPLING_INTERVAL = 10          # Sampling interval in seconds (e.g., 60 for 1-minute samples)
SAMPLING_FREQUENCY = 60        # How often to collect samples in seconds (e.g., 300 = 5 minutes)
CSV_OUTPUT_PATH = "."           # Output directory for CSV file

# Define the CSV header
csv_header = [
    "timestamp",
    "pool",
    "alloc",
    "free",
    "read_ops",
    "write_ops",
    "read_bw (MB/s)",
    "write_bw (MB/s)",
    "total_wait_read (ms)",
    "total_wait_write (ms)",
    "disk_wait_read (ms)",
    "disk_wait_write (ms)",
    "syncq_wait_read (ms)",
    "syncq_wait_write (ms)",
    "asyncq_wait_read (ms)",
    "asyncq_wait_write (ms)",
    "scrub_wait (ms)",
    "trim_wait (ms)",
    "rebuild_wait (ms)"
]

def convert_bandwidth_to_mb(value):
    if value == '-':
        return 0.0
    return round(int(value) / (1024 * 1024), 2)

def convert_wait_to_ms(value):
    if value == '-':
        return 0.0
    return round(int(value) / 1_000_000, 2)

def parse_zpool_iostat(input_lines, pool_name, current_timestamp):
    data = []
    
    for line in input_lines:
        line = line.strip()
        if not line:
            continue
        
        # Capture data line for the pool
        if line.startswith(pool_name):
            fields = re.split(r'\s+', line)
            if len(fields) >= 18:  # Ensure there are enough fields (adjusted from 19)
                try:
                    new_row = [
                        current_timestamp,  # Use generated timestamp
                        pool_name,
                        fields[1],   # alloc
                        fields[2],   # free
                        fields[3],   # read_ops
                        fields[4],   # write_ops
                        convert_bandwidth_to_mb(fields[5]),   # read_bw
                        convert_bandwidth_to_mb(fields[6]),   # write_bw
                        convert_wait_to_ms(fields[7]),   # total_wait_read
                        convert_wait_to_ms(fields[8]),   # total_wait_write
                        convert_wait_to_ms(fields[9]),   # disk_wait_read
                        convert_wait_to_ms(fields[10]),  # disk_wait_write
                        convert_wait_to_ms(fields[11]),  # syncq_wait_read
                        convert_wait_to_ms(fields[12]),  # syncq_wait_write
                        convert_wait_to_ms(fields[13]),  # asyncq_wait_read
                        convert_wait_to_ms(fields[14]),  # asyncq_wait_write
                        convert_wait_to_ms(fields[15]),  # scrub_wait
                        convert_wait_to_ms(fields[16]),  # trim_wait
                        convert_wait_to_ms(fields[17])   # rebuild_wait
                    ]
                    data.append(new_row)
                except (ValueError, IndexError) as e:
                    print(f"Error parsing line: {line}. Error: {e}")
                    continue

    return data

def collect_zpool_iostat():
    command = f"zpool iostat -l -T d -p {POOL_NAME} {SAMPLING_INTERVAL} 1"
    print(f"Running command: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {result.stderr}")
        return []
    
    # Generate current timestamp
    current_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    print("Command output:")
    print(result.stdout)
    input_lines = result.stdout.splitlines()
    data = parse_zpool_iostat(input_lines, POOL_NAME, current_timestamp)
    if not data:
        print("No data parsed from command output. Check field alignment.")
    return data

def write_to_csv(data):
    csv_file = os.path.join(CSV_OUTPUT_PATH, f"zpool_iostat_{POOL_NAME}.csv")
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(csv_header)
        writer.writerows(data)

def main():
    while True:
        print(f"\n--- Starting data collection at {time.strftime('%c')} ---")
        data = collect_zpool_iostat()
        if data:
            write_to_csv(data)
        print(f"Sleeping for {SAMPLING_FREQUENCY - SAMPLING_INTERVAL} seconds until next sample...")
        time.sleep(SAMPLING_FREQUENCY - SAMPLING_INTERVAL)

if __name__ == "__main__":
    main()
