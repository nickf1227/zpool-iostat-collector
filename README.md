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

## Prerequisites

- Python 3.x
- ZFS utilities (`zpool` command must be available)
- Tested on Linux/Unix systems with ZFS support

## Installation

1. Clone or download the script to your system.
2. Ensure Python 3 and ZFS utilities are installed:

   ```bash
   # For Ubuntu/Debian
   sudo apt-get install python3 zfsutils-linux
   ```

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

1. **`zpool` command not found**:
   - Ensure ZFS utilities are installed (see [Installation](#installation))

2. **Permission denied errors**:
   - Run the script with `sudo` if needed (e.g., `sudo python3 zpool_iostat.py`)

3. **No data in CSV**:
   - Verify the pool name matches your ZFS pool
   - Check if `zpool iostat <POOL_NAME>` returns valid data manually

4. **Field parsing errors**:
   - Ensure your `zpool iostat` output format matches the expected format (test with `zpool iostat -l -T d -p`)

## Contributing

Contributions are welcome! Open an issue or submit a pull request for improvements.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
