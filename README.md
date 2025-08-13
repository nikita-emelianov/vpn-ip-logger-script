# VPN IP Logger

Continuously logs your public IP address to help verify your VPN connection is always active.

## Setup

Install the required library:

```
pip3 install requests
```

## Usage

**1. Start the Script**

Run this command in your terminal to start the logger in the background:

```
nohup python3 ip_monitor.py &
```

**2. Stop the Script**

To stop the script, run this single command:

```
pkill -f ip_monitor.py
```

## Output Files

  * **`ip_summary.txt`**: A live summary of IP counts, updated after every check. This is the main file to watch.
  * **`ip_log.txt`**: A detailed, timestamped log of every IP check.
