# CSC258 Programming Assignment #1 – Client/Server Application

**Author:** Soulius Jones  
**Instructor:** Dr. Abeer Abdel Khaleq  

---

## 1. Required Environment
- Python 3.9 or higher
- Uses only Python standard library (no external packages)
- OS: Windows, macOS, or Linux

---

## 2. Project Files
- `server.py` – TCP server that receives client messages, adds receive time, and replies
- `client.py` – TCP client that sends a client number and message
- `multi_client.py` – Demonstrates multiple clients connecting concurrently

---

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

## 4. How to Run
Step A: Start the Server (Terminal 1)
python server.py
Expected output:

Server starts listening on HOST:PORT

Displays connection messages when clients connect

Step B: Run a Single Client (Terminal 2)
python client.py --client-number 1 --message "Hello Server!"
Expected output:

Client prints JSON response

Response includes server receive timestamp

Step C: Run Multiple Clients
python multi_client.py --num-clients 10
Expected output:

Multiple client responses printed

Server logs multiple accepted connections

## 5. Error Handling Demonstration (Screenshot)
Stop the server using Ctrl+C

Run:

python client.py --client-number 1 --message "Test when server is off"
Expected output:

Client prints: Connection refused. Is the server running?

## 6. Google Cloud Shell (Optional)
This project can also be run using Google Cloud Shell:

Upload project files to Cloud Shell

Run the same commands:

python server.py

python client.py ...

python multi_client.py ...

