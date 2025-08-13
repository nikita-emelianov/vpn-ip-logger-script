#!/usr/bin/env python3
import requests
import time
import datetime
from collections import defaultdict
import signal
import sys
import os

# --- Configuration ---
LOG_FILE = 'ip_log.txt'
# We will ping a service that returns our public IP address.
IP_CHECK_URL = 'https://api.ipify.org'
# The interval in seconds to check the IP address.
CHECK_INTERVAL = 2

# --- Globals ---
# Use defaultdict to easily handle counting.
ip_counts = defaultdict(int)
# Get the absolute path for the log file
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), LOG_FILE)


def get_public_ip():
    """
    Fetches the current public IP address from the specified URL.
    Returns the IP address as a string or None if it fails.
    """
    try:
        response = requests.get(IP_CHECK_URL, timeout=5)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        # This will catch connection errors, timeouts, etc.
        return f"Error: Could not retrieve IP. {e}"


def log_ip(ip_address):
    """
    Appends the IP address and timestamp to the log file.
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} - {ip_address}\n"
    with open(log_file_path, 'a') as f:
        f.write(log_entry)


def print_summary():
    """
    Prints a summary of the IP addresses and their counts.
    This is called when the script is gracefully shut down.
    """
    print("\n--- IP Address Connection Summary ---")
    print(f"Log file saved to: {log_file_path}")
    if not ip_counts:
        print("No IP addresses were recorded.")
        return

    # Sort the IPs by count in descending order for a clear report
    sorted_ips = sorted(ip_counts.items(), key=lambda item: item[1], reverse=True)

    print(f"{'Count':<10} {'IP Address'}")
    print("-" * 30)
    for ip, count in sorted_ips:
        print(f"{count:<10} {ip}")
    print("-" * 30)
    print("Script terminated.")


def signal_handler(sig, frame):
    """
    Handles termination signals (like Ctrl+C) to ensure the summary is printed.
    """
    print("\nTermination signal received. Generating summary...")
    sys.exit(0)


def main():
    """
    Main function to run the IP checking loop.
    """
    # Set up signal handling for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("Starting IP logger...")
    print(f"Press Ctrl+C to stop the script and see the summary.")
    print(f"Logging to: {log_file_path}")

    try:
        while True:
            current_ip = get_public_ip()
            if current_ip:
                # Log every attempt to the file
                log_ip(current_ip)
                # Increment the counter for this specific IP
                ip_counts[current_ip] += 1
                # Print to console for real-time feedback
                print(f"\rCurrent IP: {current_ip} | Last check: {datetime.datetime.now().strftime('%H:%M:%S')}", end="")

            # Wait for the specified interval
            time.sleep(CHECK_INTERVAL)
    finally:
        # This ensures the summary is printed no matter how the script exits
        print_summary()


if __name__ == "__main__":
    main()
