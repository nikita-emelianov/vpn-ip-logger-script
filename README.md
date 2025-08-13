# VPN IP Logger

This script is a simple tool designed to run in the background on macOS or Linux to continuously monitor and log your public IP address. Its primary purpose is to help you verify that your VPN connection is stable and that your real IP is not being exposed.

It checks your public IP address every 2 seconds and records every check with a timestamp in a log file. When the script is stopped, it generates a final summary report counting how many times each IP address was detected.

## Requirements

  * Python 3
  * The `requests` library

## How to Use

### 1\. Installation

Before running the script, you need to install the `requests` library. Open your terminal and run:

```
pip3 install requests
```

### 2\. Running the Script

Save the script as `ip_monitor.py`.

To run it in the background so it continues working even after you close the terminal, navigate to its directory and use `nohup`:

```
nohup python3 ip_monitor.py &
```

The `&` sends the process to the background.

### 3\. Stopping the Script & Getting the Summary

The script needs to be stopped gracefully to generate the final summary file.

**Step 1: Find the Process ID (PID)**
Use the `pgrep` command to find the script's PID:

```
pgrep -f ip_monitor.py
```

This will return a number, which is the PID.

**Step 2: Terminate the Process**
Use the `kill` command with the PID you just found:

```
kill <PID_from_pgrep>
```

For example, if `pgrep` returned `12345`, you would run `kill 12345`.

## Output Files

The script will create two files in the same directory:

1.  **`ip_log.txt`**
      * This is a detailed, running log.
      * Every check is recorded here with a timestamp (e.g., `2023-10-27 10:30:00 - 8.8.8.8`).
      * This file can get very large over time.
2.  **`ip_summary.txt`**
      * This file is **only created when you stop the script**.
      * It provides a clean summary of all unique IP addresses that were detected and the total count for each one. This is the best file to look at to quickly verify your VPN's consistency.
