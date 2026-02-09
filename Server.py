#!/usr/bin/env python3
"""
CSC258 - Distributed Systems
Programming Assignment #1: Client/Server Socket Application

Author: Soulius Jones
Instructor: Dr. Abeer Abdel Khaleq
Term: Spring 2026 (update if needed)

Purpose:
    This server listens on a TCP socket, accepts multiple clients, receives a JSON
    message with a client number and hello message, adds the time the message was
    received, and sends a JSON response back to the client.

Concurrency:
    The server supports multiple clients by creating a new thread per accepted
    connection (thread-per-client model). This allows simultaneous clients.

Protocol:
    - Client sends one newline-terminated JSON line:
        {"client_number": <int>, "message": <string>}\n
    - Server responds with one newline-terminated JSON line including received_time.

How to run:
    python server.py
"""


import socket
import threading
import json
from datetime import datetime, timezone
from typing import Tuple


HOST = "127.0.0.1"   # Use "0.0.0.0" to allow LAN connections
PORT = 5000          # Change if needed
BACKLOG = 50         # Queue size for pending connections
RECV_BUFFER = 4096   # bytes


def utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp (e.g., 2026-02-08T10:12:33.123Z)."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def send_json_line(conn: socket.socket, payload: dict) -> None:
    """Send a JSON object as a single line (newline-terminated)."""
    data = (json.dumps(payload) + "\n").encode("utf-8")
    conn.sendall(data)


def recv_json_line(conn: socket.socket) -> dict:
    """
    Receive one newline-terminated JSON message.
    For simplicity, this function reads until it sees a newline.
    """
    chunks = []
    while True:
        part = conn.recv(RECV_BUFFER)
        if not part:
            # Client closed connection before sending full line
            raise ConnectionError("Client disconnected before sending a complete message.")
        chunks.append(part)
        joined = b"".join(chunks)
        if b"\n" in joined:
            line, _rest = joined.split(b"\n", 1)
            try:
                return json.loads(line.decode("utf-8"))
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON received: {e}") from e


def handle_client(conn: socket.socket, addr: Tuple[str, int]) -> None:
    """
    Handle a single client connection:
    - Receive JSON
    - Add received timestamp
    - Send JSON response
    """
    try:
        conn.settimeout(10)  # prevent hanging forever if client stalls
        request = recv_json_line(conn)

        # Validate required fields
        if "client_number" not in request or "message" not in request:
            raise ValueError("Request must include 'client_number' and 'message' fields.")

        client_number = request["client_number"]
        message = request["message"]

        received_time = utc_timestamp()
        server_response_text = f"[RECEIVED {received_time}] Client {client_number} said: {message}"

        response = {
            "client_number": client_number,
            "original_message": message,
            "received_time": received_time,
            "server_response": server_response_text,
        }

        send_json_line(conn, response)

    except socket.timeout:
        # Expected if client connects but doesn't send data in time
        err = {"error": "timeout", "detail": "Client timed out while sending data."}
        try:
            send_json_line(conn, err)
        except Exception:
            pass

    except (ValueError, ConnectionError) as e:
        # Invalid JSON, missing fields, or disconnect mid-message
        err = {"error": "bad_request", "detail": str(e)}
        try:
            send_json_line(conn, err)
        except Exception:
            pass

    except OSError as e:
        # Lower-level socket errors (reset, broken pipe, etc.)
        # In many cases, the client is already gone.
        print(f"[Server] Socket/OS error with {addr}: {e}")

    except Exception as e:
        # Catch-all so server does not crash on unexpected bugs
        print(f"[Server] Unexpected error with {addr}: {e}")

    finally:
        try:
            conn.close()
        except Exception:
            pass


def main() -> None:
    """Start the TCP server and accept multiple client connections concurrently."""
    print(f"[Server] Starting on {HOST}:{PORT}")

    # Create TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        # Allow quick restart without 'Address already in use'
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_sock.bind((HOST, PORT))
        server_sock.listen(BACKLOG)

        print("[Server] Listening for connections... (Ctrl+C to stop)")

        try:
            while True:
                conn, addr = server_sock.accept()
                print(f"[Server] Connection accepted from {addr}")

                # Thread per connection => multiple clients concurrently
                t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                t.start()

        except KeyboardInterrupt:
            print("\n[Server] Shutting down (KeyboardInterrupt).")


if __name__ == "__main__":
    main()

                        

                        




