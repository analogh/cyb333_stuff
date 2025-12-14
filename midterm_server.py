#! /usr/bin/env python3
# server.py - Socket Connection Server

import socket
import sys

# Define Host and Port for the server
HOST = '127.0.0.1'  #  localhost
PORT = 65432        # Arbitrary, non-privileged port

def start_server():
    """Initializes and runs the TCP server."""
    
    # 1. Creates a socket object (AF_INET for IPv4, SOCK_STREAM for TCP)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(f"Error creating socket: {e}")
        sys.exit(1)
        
    print("Socket successfully created.")

    # 2. Binds the socket to the address and port
    try:
        s.bind((HOST, PORT))
    except socket.error as e:
        print(f"Error binding to {HOST}:{PORT}. Error: {e}")
        s.close()
        sys.exit(1)

    # 3. Listens for incoming connections (allow a maximum of 5 queued connections)
    s.listen(5)
    print(f"Server is listening on {HOST}:{PORT}...")
    
    # Main server loops to continuously accept connections
    while True:
        # 4. Accepts a new connection
        # The accept() method blocks until a client connects.
        # conn is a new socket object for the conversation.
        # addr is the address of the client (IP, port).
        try:
            conn, addr = s.accept()
            print(f"Connection from: {addr}")
            
            # Starts message exchange loop
            while True:
                # 5. Receives data from the client (max 1024 bytes)
                data = conn.recv(1024)
                
                # Checks for empty data (client disconnection)
                if not data:
                    print(f"Client {addr} disconnected.")
                    break
                
                # Decodes and display the received message
                message = data.decode('utf-8')
                print(f"Received from client: {message}")
                
                # Checks for a specific exit command
                if message.lower().strip() == 'quit':
                    print("Client requested graceful shutdown.")
                    conn.sendall("ACK - Server closing connection.".encode('utf-8'))
                    break
                
                # 6. Sends a response back to the client
                response = f"ACK: Received your message '{message[:20]}...'"
                conn.sendall(response.encode('utf-8'))
                
        except socket.error as e:
            print(f"An error occurred during communication: {e}")
            
        finally:
            # 7. Proper shutdown/disconnection handling
            if 'conn' in locals() and conn:
                conn.close()
            # Loop continues to listen for the next client

if __name__ == "__main__":
    start_server()