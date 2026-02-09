# CSC258 Programming Assignment #1 - Client/Server Application
**Author:** Soulius Jones  
**Instructor:** Dr. Abeer Abdel Khaleq  

## 1. Required Environment
- Python 3.9+ (standard library only; no pip installs required)
- OS: Windows / macOS / Linux (works on all)

## 2. Project Files
- server.py: TCP server, accepts clients, adds receive timestamp, replies
- client.py: TCP client, sends client_number + message, prints response
- multi_client.py: runs many clients to demonstrate concurrency

## 3. Virtual Environment Setup (Recommended)

### Windows (PowerShell)
```powershell
cd csc258_pa1
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
macOS / Linux
cd csc258_pa1
python3 -m venv .venv
source .venv/bin/activate
python --version


4. How to Run
Step A: Start the server (Terminal 1)
python server.py
Expected: server prints that it is listening on HOST:PORT.

Step B: Run one client (Terminal 2)
python client.py --client-number 1 --message "Hello Server!"
Expected: client prints JSON response including a received_time timestamp.

Step C: Run multiple clients (Terminal 2)
python multi_client.py --num-clients 10
Expected: multiple client responses print; server logs multiple accepted connections.

5. Error Handling Test (for screenshot)
Stop server with Ctrl+C

Run:

python client.py --client-number 1 --message "Test when server is off"
Expected: client prints "Connection refused. Is the server running?"


## Optional: Google Cloud Shell editor run
If using Google Cloud Shell:
1) Upload or create files in Cloud Shell
2) Run the same commands above:
   - python server.py
   - python client.py ...
   - python multi_client.py ...
That README is exactly what graders look for.

