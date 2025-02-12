# ZFS Pool Performance Monitor

This script collects performance metrics from a ZFS pool using `zpool iostat` and logs the data to a CSV file for analysis. It is designed to run continuously, capturing metrics at configurable intervals.

## Features

- Collects ZFS pool performance metrics including:
  - Bandwidth (read/write in MB/s)
  - Operations per second (read/write)
  - Wait times (disk, syncq, asyncq, scrub, trim, rebuild)
- Logs data to a CSV file with timestamps
- Configurable sampling intervals and output directory
- Runs continuously until manually stopped


## Installation

1. I have a seperate dataset in my pool `/mnt/tank/tn_scripts` that I use for this purpose, and I highly recommend you should as well.
2. `git clone https://github.com/nickf1227/zpool-iostat-collector.git /mnt/tank/tn_scripts` Replace the path with where you want to store it on your system, and then run it.
3. You can call the script by running `python3 /mnt/tank/tn_scripts/zpool-iostat-collector.py`
4. If you have more than one pool you would like to monitor, you would need to copy the `zpool-iostat-collector.py` file. Something like this could work `cp /mnt/tank/tn_scripts/zpool-iostat-collector.py /mnt/tank/tn_scripts/zpool-iostat-collector-pool1.py && mv /mnt/tank/tn_scripts/zpool-iostat-collector.py /mnt/tank/tn_scripts/zpool-iostat-collector-pool2.py`
5. Then you would have to configure them booth (see below) and call them both individually.



## Configuration

Edit the following variables in the script to match your environment:

```python
POOL_NAME = "ice"               # Name of your ZFS pool
SAMPLING_INTERVAL = 10          # Interval between iostat samples (seconds)
SAMPLING_FREQUENCY = 30         # How often to collect samples (seconds)
CSV_OUTPUT_PATH = "."           # Output directory for CSV file
```

- **SAMPLING_INTERVAL**: How frequently `zpool iostat` takes a snapshot (e.g., 10 = sample every 10 seconds)
- **SAMPLING_FREQUENCY**: How often the script collects data (e.g., 30 = log to CSV every 30 seconds)

## Usage

Run the script:

```bash
python3 zpool_iostat.py
```

The script will:
- Create a CSV file named `zpool_iostat_<POOL_NAME>.csv` in the specified directory
- Run indefinitely until interrupted with `Ctrl+C`

## Sample CSV Output

```csv
timestamp,pool,alloc,free,read_ops,write_ops,read_bw (MB/s),write_bw (MB/s),total_wait_read (ms),total_wait_write (ms),disk_wait_read (ms),disk_wait_write (ms),syncq_wait_read (ms),syncq_wait_write (ms),asyncq_wait_read (ms),asyncq_wait_write (ms),scrub_wait (ms),trim_wait (ms),rebuild_wait (ms)
Mon Mar 20 14:30:00 UTC 2023,ice,100G,500G,150,80,45.2,22.7,1.2,0.8,0.5,0.3,0.1,0.0,0.6,0.5,0.0,0.0,0.0
```

## Logging & Debugging

- The script prints status messages to stdout (e.g., sampling times, errors)
- To disable debug messages, remove/comment the `print` statements in the code

## Troubleshooting

1. **Permission denied errors**:
   - Run the script with `sudo` if needed (e.g., `sudo python3 zpool_iostat.py`)

## Contributing

Contributions are welcome! Open an issue or submit a pull request for improvements.
