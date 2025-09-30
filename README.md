# 🔐 Cyber-Security Toolkit
*A mini security lab for learning & experimenting with networking and vulnerability scanning.*

This repository contains **educational scripts** for:
- Socket programming (client/server)
- Basic vulnerability checks (SQLi, XSS, open ports)
- Simple fuzzing utilities
- Example datasets (IPs, logs, payloads)

⚠️ **Disclaimer**: This project is for **educational purposes only**.  
Use it **only on systems you own or have explicit permission to test**.

---

## 📚 Table of Contents
- [📂 Project Structure](#-project-structure)
- [🛠 Features](#-features)
- [🚀 Usage](#-usage)
  - [▶️ Client/Server](#️-clientserver)
  - [🔍 Vulnerability Checks](#-vulnerability-checks)
  - [🌀 Fuzzing](#-fuzzing)
- [📦 Data Files](#-data-files)
- [👩‍💻 Contributing](#-contributing)
- [📄 License](#-license)

---

## 📂 Project Structure

```bash
CYBER-SECURITY/
├─ data/ # Example datasets
│ ├─ fuzzing.txt # Payload list for fuzzing
│ ├─ ip.txt # IP addresses to test
│ ├─ log.txt # Log file
│ └─ usom.txt # Blocklist (sample from USOM)
│
├─ src/
│ ├─ vulnerabilities/ # Vulnerability checks
│ │ ├─ sqli.py # Basic SQL injection test
│ │ ├─ xss.py # Basic reflected XSS test
│ │ └─ ports.py # Open ports & banner grabbing
│ │
│ ├─ client.py # TCP client
│ ├─ server.py # TCP server
│ ├─ modul_socket.py # Reusable socket functions
│ ├─ core.py # Session builder (HTTP requests with retry)
│ ├─ models.py # Finding dataclass (standardized results)
│ ├─ USOM-KONTROL.py # Script to check URLs/IPs against USOM blocklist
│ ├─ USOM.py # Alternative USOM handler
│ └─ USOM2.py # Another USOM version
│
├─ tools/
│ └─ fuzzing.py # Script to run fuzzing payloads
│
└─ README.md # This documentation

```


---

## 🛠 Features
✔️ **Client/Server scripts** with Python sockets  
✔️ **Reusable socket module** for experiments  
✔️ **Vulnerability scanners**:
- SQL Injection (query tampering)
- Reflected XSS detection
- Open Port banner grabber  
✔️ **Fuzzing utility** to test inputs with payload lists  
✔️ **Datasets** (IPs, payloads, logs, USOM blocklist)

---

## 🚀 Usage

### ▶️ Client/Server
Run the server first:
```bash
python -m src.server
```


Then start the client in another terminal:
```bash
python -m src.client
```
Communication will happen over TCP sockets.


### 🔍 Vulnerability Checks
All vulnerability scripts rely on src/core.py + src/models.py.

SQL Injection check:
```bash
python -m src.vulnerabilities.sqli "https://example.com/?id=1"
```

XSS check:
```bash
python -m src.vulnerabilities.xss "https://example.com/?q=test"
```


Open Ports:
```bash
python -m src.vulnerabilities.ports example.com 80 443 8080
```

### 🌀 Fuzzing
Run the fuzzing tool against a target:
```bash
python -m tools.fuzzing --target https://example.com --payloads data/fuzzing.txt
```