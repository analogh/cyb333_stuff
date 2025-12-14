#! /usr/bin/env python3
# client.py - Socket Connection Client

import socket
import sys

# DefinesHost and Port of the server to connect to
HOST = '127.0.0.1' 
PORT = 4065        

def start_client():
    """Initializes and runs the TCP client."""
    
    # 1. Creates a socket object (AF_INET for IPv4, SOCK_STREAM for TCP)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(f"Error creating socket: {e}")
        sys.exit(1)

    # 2. Attempts to connect to the server
    try:
        s.connect((HOST, PORT))
        print(f"Successfully connected to server at {HOST}:{PORT}")
    
    # Error Handling for connection failure
    except ConnectionRefusedError:
        print(f"ERROR: Connection refused. Is the server running on {HOST}:{PORT}?")
        s.close()
        sys.exit(1)
    except socket.gaierror:
        print(f"ERROR: Address-related error connecting to the server.")
        s.close()
        sys.exit(1)
    except socket.error as e:
        print(f"An unexpected error occurred during connection: {e}")
        s.close()
        sys.exit(1)
        
    # 3. Message Exchange Loop
    while True:
        try:
            # Gets input from the user
            message = input("Enter message (or 'quit' to exit): ")
            
            # Checks for disconnection command
            if message.lower().strip() == 'quit':
                print("Sending quit signal to server...")
                s.sendall(message.encode('utf-8')) # Send the signal
                break

            # Sends message to the server
            s.sendall(message.encode('utf-8'))
            
            # Receives response from the server
            data = s.recv(1024)
            if not data:
                print("Server closed the connection unexpectedly.")
                break
            
            print(f"Server response: {data.decode('utf-8')}")
            
        except socket.error as e:
            print(f"Error during message exchange: {e}")
            break
            
    # 4. Clean disconnection process
    print("Client gracefully shutting down.")
    s.close()

if __name__ == "__main__":
    start_client()