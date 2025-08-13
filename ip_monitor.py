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
SUMMARY_FILE = 'ip_summary.txt'
IP_CHECK_URL = 'https://api.ipify.org'
CHECK_INTERVAL = 2

# --- Globals ---
ip_counts = defaultdict(int)
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_dir, LOG_FILE)
summary_file_path = os.path.join(script_dir, SUMMARY_FILE)

def get_public_ip():
    """
    Fetches the current public IP address.
    Returns the IP address as a string or an error message.
    """
    try:
        response = requests.get(IP_CHECK_URL, timeout=5)
        response.raise_for_status()
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        return f"Error: Could not retrieve IP. {e}"

def log_ip(ip_address):
    """
    Appends the IP address and timestamp to the detailed log file.
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} - {ip_address}\n"
    with open(log_file_path, 'a') as f:
        f.write(log_entry)

def update_summary_file():
    """
    Writes the current IP counts to the summary file.
    This function is called after every check.
    """
    summary_lines = []
    summary_lines.append("--- IP Address Connection Summary (Live) ---")
    summary_lines.append(f"Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if not ip_counts:
        summary_lines.append("No IP addresses recorded yet.")
    else:
        sorted_ips = sorted(ip_counts.items(), key=lambda item: item[1], reverse=True)
        header = f"\n{'Count':<10} {'IP Address'}"
        separator = "-" * 30
        
        summary_lines.append(header)
        summary_lines.append(separator)
        for ip, count in sorted_ips:
            summary_lines.append(f"{count:<10} {ip}")
        summary_lines.append(separator)

    summary_text = "\n".join(summary_lines)

    try:
        with open(summary_file_path, 'w') as f:
            f.write(summary_text)
    except IOError as e:
        # Print error to the console if file writing fails
        print(f"\nError writing summary file: {e}")

def signal_handler(sig, frame):
    """
    Handles termination signals for a clean exit message.
    """
    print("\nTermination signal received. Exiting.")
    sys.exit(0)

def main():
    """
    Main function to run the IP checking loop.
    """
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("Starting IP logger...")
    print(f"Press Ctrl+C to stop the script.")
    print(f"Logging to: {log_file_path}")
    print(f"Real-time summary at: {summary_file_path}")

    try:
        while True:
            current_ip = get_public_ip()
            if current_ip:
                log_ip(current_ip)
                ip_counts[current_ip] += 1
                
                # Update the summary file in real-time
                update_summary_file()
                
                print(f"\rCurrent IP: {current_ip} | Checks: {sum(ip_counts.values())}", end="")

            time.sleep(CHECK_INTERVAL)
    finally:
        print("\nScript terminated.")

if __name__ == "__main__":
    main()
