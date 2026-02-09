#!/usr/bin/env python3
"""
CSC258 - Distributed Systems
Programming Assignment #1: Multiple Client Demonstration

Author: Soulius Jones

Purpose:
    Spawns multiple client threads, each sending a unique client_number starting from 1.
    Demonstrates that the server can handle multiple clients.

How to run:
    python multi_client.py --num-clients 10
"""

import threading
import time
from Client import start_client  # re-use your client logic


def client_worker(client_number: int) -> None:
    msg = f"Hello from client {client_number}!"
    start_client(client_number, msg)


def main(num_clients: int) -> None:
    threads = []
    for i in range(1, num_clients + 1):
        t = threading.Thread(target=client_worker, args=(i,))
        threads.append(t)
        t.start()
        time.sleep(0.05)  # tiny stagger helps output readability

    for t in threads:
        t.join()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-clients", type=int, default=5)
    args = parser.parse_args()
    main(args.num_clients)
