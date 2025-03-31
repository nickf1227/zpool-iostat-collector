import sys
import csv
import os
import subprocess
import time
import re

# Debug print: script start
print("Starting ioztat monitoring script...")

# Configurable settings
POOL_NAME = "ice"                  # ZFS pool name
IOZTAT_PATH = "./ioztat/ioztat"     # Path to ioztat executable
SAMPLING_INTERVAL = 120              # Sampling interval in seconds
SAMPLING_FREQUENCY = 240            # How often to collect samples in seconds
CSV_OUTPUT_PATH = "/mnt/fire/tn_scripts"  # Output directory for CSV file

# Define the CSV header
csv_header = [
    "timestamp",
    "pool",
    "dataset",
    "read_ops",
    "write_ops",
    "read_throughput_mb_s",
    "write_throughput_mb_s",
    "read_opsize_kb",
    "write_opsize_kb"
]

def parse_ioztat(input_lines, pool_name, current_timestamp):
    data = []
    for line in input_lines:
        line = line.strip()
        if not line:
            continue
        
        # Match lines starting with pool name followed by metrics
        if line.startswith(pool_name):
            fields = re.split(r'\s+', line)
            if len(fields) == 7:
                try:
                    dataset = fields[0]
                    read_ops = int(fields[1])
                    write_ops = int(fields[2])
                    read_bw = int(fields[3])
                    write_bw = int(fields[4])
                    read_opsize = int(fields[5])
                    write_opsize = int(fields[6])

                    # Calculate throughput in MB
                    read_throughput = round(read_bw / (1024 ** 2), 2)
                    write_throughput = round(write_bw / (1024 ** 2), 2)
                    # Calculate opsize in KB
                    read_opsize_kb = round(read_opsize / 1024, 2)
                    write_opsize_kb = round(write_opsize / 1024, 2)

                    new_row = [
                        current_timestamp,
                        pool_name,
                        dataset,
                        read_ops,
                        write_ops,
                        read_throughput,
                        write_throughput,
                        read_opsize_kb,
                        write_opsize_kb
                    ]
                    data.append(new_row)
                except (ValueError, IndexError) as e:
                    print(f"Error parsing line: {line}. Error: {e}")
                    continue
    return data

def collect_ioztat():
    command = f"{IOZTAT_PATH} -ePx {POOL_NAME} {SAMPLING_INTERVAL} 1"
    print(f"Running command: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error running command: {result.stderr}")
        return []
    
    current_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("Command output:")
    print(result.stdout)
    
    input_lines = result.stdout.splitlines()
    data = parse_ioztat(input_lines, POOL_NAME, current_timestamp)
    
    if not data:
        print("No valid data parsed from command output.")
    
    return data

def write_to_csv(data):
    # Ensure the output directory exists
    os.makedirs(CSV_OUTPUT_PATH, exist_ok=True)
    
    csv_file = os.path.join(CSV_OUTPUT_PATH, f"ioztat_metrics_{POOL_NAME}.csv")
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(csv_header)
        writer.writerows(data)

def main():
    while True:
        print(f"\n--- Starting data collection at {time.strftime('%c')} ---")
        data = collect_ioztat()
        if data:
            write_to_csv(data)
        
        sleep_time = SAMPLING_FREQUENCY - SAMPLING_INTERVAL
        print(f"Sleeping for {sleep_time} seconds until next sample...")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
