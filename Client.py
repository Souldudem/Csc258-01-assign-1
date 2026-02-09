#!/usr/bin/env python3
"""
CSC258 - Distributed Systems
Programming Assignment #1 (Client-Server / System Architecture)

Author: Soulius Jones
Instructor: Dr. Abeer Abdel Khaleq

Client Requirements Implemented:
- Establish connection to server.
- Send a message to the server with a client number starting at 1.
- Receive the message from the server and display it.
- Close the connection.
- Handle common networking errors.

Usage examples:
  python client.py --client-number 1 --message "Hello Server!"
  python client.py --client-number 2
"""

import socket
import json
import argparse


HOST = "127.0.0.1"
PORT = 5000
RECV_BUFFER = 4096

def send_json(sock: socket.socket, payload: dict) -> None:
        """Send a JSON object as a newline-terminated line."""
        sock.sendall((json.dumps(payload) + "\n").encode("utf-8"))


def recv_json(sock: socket.socket) -> dict:
        raw_chunk=[]
        while True:
                part = sock.recv(RECV_BUFFER)
                if not part:
                        raise ConnectionError("Server disconnected before sending a response.")
                raw_chunk.append(part)
                joined = b"".join(raw_chunk)
                if b"\n" in joined:
                    line, _rest = joined.split(b"\n", 1)
                    return json.loads(line.decode("utf-8"))

def start_client (client_number: int, message: str) -> None:
       request = {"client_number":client_number, "message": message}

       try:
              with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(10)                 # don’t hang forever
                    sock.connect((HOST, PORT))          # establish connection to server
                    send_json(sock, request)       # send request payload
                    response = recv_json(sock)
                    
                    print("---- Server Response ----")
                    print(json.dumps(response, indent=2))     # wait for server response
               
       except ConnectionRefusedError:
                    print("[Client] ERROR: Connection refused. Is the server running?")
       except socket.timeout:
                    print("[Client] ERROR: Timeout. Server may be slow or unreachable")
       except json.JSONDecodeError as e:
                    print(f"[Client] ERROR: Could not parse server response as JSON: {e}")
       except OSError as e:
                    print(f"[Client] ERROR: Socket/OS error: {e}")
       except Exception as e:
                    print(f"[Client] ERROR: Unexpected error: {e}")


def main() -> None:
    """Parse command-line arguments and run the client once."""
    message_parser = argparse.ArgumentParser(description="CSC258 PA1 Client")
    message_parser.add_argument("--client-number", type=int, required=True,
                        help="Client number starting from 1 (e.g., 1, 2, 3...)")
    message_parser.add_argument("--message", type=str, default="Hello from client!",
                        help="Message to send to the server")
    args = message_parser.parse_args()

    start_client(args.client_number, args.message)


if __name__ == "__main__":
    main()
        

        