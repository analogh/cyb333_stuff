#! /usr/bin/env python3
# scanner.py - Port Scanner

import socket
import sys
import time
from datetime import datetime

def parse_ports(port_range):
    """Parses a port range string (e.g., '20-100' or '22,80,443') into a list of integers."""
    ports = set()
    try:
        # Handles range
        if '-' in port_range:
            start, end = map(int, port_range.split('-'))
            ports.update(range(start, end + 1))
        # Handles comma-separated list
        elif ',' in port_range:
            ports.update(map(int, port_range.split(',')))
        # Handles single port
        else:
            ports.add(int(port_range))
            
    except ValueError:
        print("ERROR: Invalid port format. Use '20-100' or '22,80,443'.")
        sys.exit(1)
        
    # Validates port numbers
    valid_ports = set()
    for port in ports:
        if 1 <= port <= 65535:
            valid_ports.add(port)
        else:
            print(f"ERROR: Invalid port number: {port}. Must be 1-65535.")
            
    if not valid_ports:
        print("ERROR: No valid ports to scan.")
        sys.exit(1)
        
    return sorted(list(valid_ports))

def scan_port(ip, port, timeout=0.5):
    """Attempts to connect to a specific port on the target IP."""
    
    # Creates a new socket object (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout) # Set a small timeout for performance
    
    # Uses connect_ex() for faster scanning. It returns an error code instead of raising an exception.
    # 0 means the connection was successful (port is open).
    result = s.connect_ex((ip, port))
    
    s.close()
    
    return result == 0

def run_scanner():
    """Main function to handle target host resolution and port scanning."""
    
    # 1. Checks for correct number of arguments (host and ports)
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <host> <port_range_or_list>")
        print("Example: python scanner.py 127.0.0.1 20-100")
        print("Example: python scanner.py scanme.nmap.org 22,80,443")
        sys.exit(1)
        
    target_host = sys.argv[1]
    port_range_str = sys.argv[2]
    
    # SecurityCheck: Enforces authorized target rule
    if target_host not in ('127.0.0.1', 'localhost', 'scanme.nmap.org'):
        print(f"\nSECURITY VIOLATION: Scanning of target '{target_host}' is not authorized.")
        print("You are ONLY authorized to scan 127.0.0.1 (localhost) or scanme.nmap.org.")
        sys.exit(1)
        
    # 2. Error Handling: Resolves hostname to IP address
    try:
        target_ip = socket.gethostbyname(target_host)
    except socket.gaierror:
        # Error handling for unreachable hosts/invalid hostnames
        print(f"\nERROR: Hostname '{target_host}' could not be resolved.")
        sys.exit(1)

    print("-" * 50)
    print(f"Scanning Target: {target_host} ({target_ip})")
    print(f"Scan Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)

    # 3. Parses and validates ports
    ports_to_scan = parse_ports(port_range_str)
    
    # 4. Scans all ports
    open_ports = []
    
    for port in ports_to_scan:
        if scan_port(target_ip, port):
            print(f"Port {port}: OPEN")
            open_ports.append(port)
        else:
            # Display closed ports for full documentation output
            print(f"Port {port}: CLOSED") 
        
        # Implements a brief delay to avoid flooding target
        time.sleep(0.01) 
            
    print("-" * 50)
    if open_ports:
        print(f"Scan Complete. Open Ports found: {', '.join(map(str, open_ports))}")
    else:
        print("Scan Complete. No open ports found in the specified range.")
    print(f"Scan Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)


if __name__ == "__main__":
    try:
        run_scanner()
    except KeyboardInterrupt:
        print("\nScan aborted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)