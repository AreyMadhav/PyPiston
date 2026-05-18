# PyPiston

PyPiston is a lightweight cross-platform networking and post-exploitation toolkit written entirely in pure Python with zero external dependencies.

It combines interactive TCP communication, listener mode, SOCKS5 proxy support, port scanning, banner grabbing, hexdump output, and JSON logging into a single portable script that works on Windows, Linux, macOS, WSL, VPS environments, and restricted systems where installing tools like Netcat or Socat may not be possible.

---

# Features

- Interactive TCP client
- Listener mode
- Port scanner
- Service banner grabbing
- SOCKS5 proxy support
- Hexdump output
- JSON output mode
- Cross-platform support
- Zero dependencies
- Single-file portable tool

---

# Requirements

- Python 3.x

No external libraries or packages are required.

---

# Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/PyPiston.git
```

Move into the directory:

```bash
cd PyPiston
```

Make the script executable (Linux/macOS):

```bash
chmod +x pypiston.py
```

---

# Usage

## Help Menu

```bash
python pypiston.py -h
```

or

```bash
python pypiston.py --help
```

---

# Basic TCP Connection

```bash
python pypiston.py <host> <port>
```

## Example

```bash
python pypiston.py example.com 1337
```

---

# Listener Mode

Start a TCP listener:

```bash
python pypiston.py --listen 4444
```

---

# Port Scanner

Scan ports on a target:

```bash
python pypiston.py <host> --scan 1-1000
```

## Example

```bash
python pypiston.py scanme.nmap.org --scan 1-1000
```

---

# Banner Grabbing

Grab service banners from a port:

```bash
python pypiston.py <host> <port> --banner
```

## Example

```bash
python pypiston.py example.com 80 --banner
```

---

# SOCKS5 Proxy Support

Route traffic through a SOCKS5 proxy:

```bash
python pypiston.py <host> <port> --proxy socks5://127.0.0.1:9050
```

---

# Hexdump Mode

Display incoming data in hexadecimal format:

```bash
python pypiston.py <host> <port> --hexdump
```

---

# JSON Output Mode

Display incoming packets/messages in JSON format:

```bash
python pypiston.py <host> <port> --json
```

---

# Example Commands

## Interactive Shell

```bash
python pypiston.py 127.0.0.1 4444
```

## Listener

```bash
python pypiston.py --listen 9001
```

## Port Scan

```bash
python pypiston.py target.com --scan 20-100
```

## SOCKS5 Proxy Connection

```bash
python pypiston.py target.com 80 --proxy socks5://127.0.0.1:9050
```

## Hexdump Traffic

```bash
python pypiston.py target.com 80 --hexdump
```

## JSON Logging

```bash
python pypiston.py target.com 80 --json
```

---

# Supported Platforms

- Windows
- Linux
- macOS
- WSL
- VPS/Cloud Environments
- Restricted CTF Environments

---

# Why PyPiston?

- No dependency hell
- Portable single-file tool
- Works in restricted environments
- Faster setup during CTFs
- Useful for quick networking tasks
- Lightweight alternative to Netcat/Socat

---

# Future Plans

Planned future features:

- UDP mode
- SSL/TLS support
- IPv6 support
- File upload/download
- Reverse shell helpers
- Async socket engine
- WebSocket support
- Raw packet mode
- Session management
- Multi-client listener

---

# Disclaimer

This tool is intended for educational purposes, CTF competitions, lab environments, and authorized security testing only.

Do not use this tool against systems you do not own or have explicit permission to test.

---
# Author
Developed by **AreyMadhav**
---
Made with Python and sleep deprivation.
