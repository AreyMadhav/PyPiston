#!/usr/bin/env python3

import socket
import threading
import sys
import os
import json
import base64
import struct
import argparse
import time

VERSION = "1.0"

BUFFER_SIZE = 4096


# =========================================================
# BANNER
# =========================================================
def banner():
    print(rf"""
██████╗ ██╗   ██╗██████╗ ██╗███████╗████████╗ ██████╗ ███╗   ██╗
██╔══██╗╚██╗ ██╔╝██╔══██╗██║██╔════╝╚══██╔══╝██╔═══██╗████╗  ██║
██████╔╝ ╚████╔╝ ██████╔╝██║███████╗   ██║   ██║   ██║██╔██╗ ██║
██╔═══╝   ╚██╔╝  ██╔═══╝ ██║╚════██║   ██║   ██║   ██║██║╚██╗██║
██║        ██║   ██║     ██║███████║   ██║   ╚██████╔╝██║ ╚████║
╚═╝        ╚═╝   ╚═╝     ╚═╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═══╝

                PyPiston v{VERSION}
      Cross-platform networking toolkit
               Author: AreyMadhav
""")


# =========================================================
# HEXDUMP
# =========================================================
def hexdump(data):

    for i in range(0, len(data), 16):

        chunk = data[i:i + 16]

        hex_bytes = " ".join(
            f"{b:02x}" for b in chunk
        )

        ascii_bytes = "".join(
            chr(b) if 32 <= b <= 126 else "."
            for b in chunk
        )

        print(
            f"{i:08x}  {hex_bytes:<48}  {ascii_bytes}"
        )


# =========================================================
# SOCKS5 SUPPORT
# =========================================================
def socks5_connect(
    proxy_host,
    proxy_port,
    target_host,
    target_port
):

    s = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    s.connect((proxy_host, proxy_port))

    # Greeting
    s.sendall(b"\x05\x01\x00")

    response = s.recv(2)

    if response != b"\x05\x00":
        raise Exception(
            "SOCKS5 authentication failed"
        )

    host_bytes = target_host.encode()

    request = (
        b"\x05"
        b"\x01"
        b"\x00"
        b"\x03"
        + bytes([len(host_bytes)])
        + host_bytes
        + struct.pack(">H", target_port)
    )

    s.sendall(request)

    response = s.recv(10)

    if len(response) < 2 or response[1] != 0x00:
        raise Exception(
            "SOCKS5 connection failed"
        )

    return s


# =========================================================
# PORT SCANNER
# =========================================================
def port_scan(host, ports):

    print(f"\n[+] Scanning {host}\n")

    for port in ports:

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.settimeout(0.5)

        result = sock.connect_ex((host, port))

        if result == 0:
            print(f"[OPEN] {port}")

        sock.close()


# =========================================================
# BANNER GRABBER
# =========================================================
def grab_banner(host, port):

    try:

        s = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        s.settimeout(2)

        s.connect((host, port))

        banner = s.recv(1024)

        print(
            banner.decode(errors="ignore")
        )

        s.close()

    except Exception as e:
        print(f"[!] Failed: {e}")


# =========================================================
# LISTENER MODE
# =========================================================
def listener(port):

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.bind(("0.0.0.0", port))

    server.listen(1)

    print(f"[+] Listening on 0.0.0.0:{port}")

    client, addr = server.accept()

    print(
        f"[+] Connection from {addr[0]}:{addr[1]}"
    )

    def recv_thread():

        while True:

            try:

                data = client.recv(BUFFER_SIZE)

                if not data:
                    break

                print(
                    data.decode(errors="ignore"),
                    end=""
                )

            except:
                break

    threading.Thread(
        target=recv_thread,
        daemon=True
    ).start()

    while True:

        try:

            cmd = input()

            client.sendall(
                (cmd + "\n").encode()
            )

        except KeyboardInterrupt:

            client.close()

            break


# =========================================================
# CLIENT MODE
# =========================================================
def client_mode(args):

    try:

        # SOCKS5
        if args.proxy:

            if not args.proxy.startswith(
                "socks5://"
            ):

                raise Exception(
                    "Only SOCKS5 proxies supported"
                )

            proxy = args.proxy.replace(
                "socks5://",
                ""
            )

            proxy_host, proxy_port = proxy.split(":")

            proxy_port = int(proxy_port)

            s = socks5_connect(
                proxy_host,
                proxy_port,
                args.host,
                args.port
            )

            print(
                f"[+] Connected through SOCKS5 proxy "
                f"{proxy_host}:{proxy_port}"
            )

        else:

            s = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            s.connect(
                (args.host, args.port)
            )

        print(
            f"[+] Connected to "
            f"{args.host}:{args.port}"
        )

        print(
            "[+] Interactive mode enabled"
        )

        print(
            "[+] Ctrl+C to quit\n"
        )

        # RECEIVE THREAD
        def recv_thread():

            while True:

                try:

                    data = s.recv(BUFFER_SIZE)

                    if not data:

                        print(
                            "\n[!] Connection closed"
                        )

                        os._exit(0)

                    # JSON MODE
                    if args.json:

                        obj = {
                            "host": args.host,
                            "port": args.port,
                            "length": len(data),
                            "timestamp": time.time(),
                            "data": base64.b64encode(
                                data
                            ).decode()
                        }

                        print(
                            json.dumps(
                                obj,
                                indent=4
                            )
                        )

                    # HEXDUMP MODE
                    elif args.hexdump:

                        hexdump(data)

                    # NORMAL OUTPUT
                    else:

                        print(
                            data.decode(
                                errors="ignore"
                            ),
                            end="",
                            flush=True
                        )

                except:

                    os._exit(0)

        threading.Thread(
            target=recv_thread,
            daemon=True
        ).start()

        # SEND LOOP
        while True:

            try:

                msg = input()

                s.sendall(
                    (msg + "\n").encode()
                )

            except KeyboardInterrupt:

                print("\n[!] Disconnected")

                s.close()

                break

    except Exception as e:

        print(f"[!] Error: {e}")


# =========================================================
# ARGUMENTS
# =========================================================
parser = argparse.ArgumentParser(
    description="PyPiston"
)

parser.add_argument(
    "host",
    nargs="?"
)

parser.add_argument(
    "port",
    nargs="?",
    type=int
)

parser.add_argument(
    "--hexdump",
    action="store_true",
    help="Display incoming data as hex"
)

parser.add_argument(
    "--json",
    action="store_true",
    help="Display incoming data as JSON"
)

parser.add_argument(
    "--proxy",
    help="SOCKS5 proxy support"
)

parser.add_argument(
    "--listen",
    type=int,
    help="Listener mode"
)

parser.add_argument(
    "--scan",
    help="Port scan (example: 1-1000)"
)

parser.add_argument(
    "--banner",
    action="store_true",
    help="Grab service banner"
)

args = parser.parse_args()

banner()


# =========================================================
# LISTENER MODE
# =========================================================
if args.listen:

    listener(args.listen)

    sys.exit(0)


# =========================================================
# PORT SCANNER
# =========================================================
if args.scan:

    if not args.host:

        print("[!] Host required")

        sys.exit(1)

    start, end = args.scan.split("-")

    ports = range(
        int(start),
        int(end) + 1
    )

    port_scan(args.host, ports)

    sys.exit(0)


# =========================================================
# BANNER GRABBER
# =========================================================
if args.banner:

    if not args.host or not args.port:

        print(
            "[!] Host and port required"
        )

        sys.exit(1)

    grab_banner(
        args.host,
        args.port
    )

    sys.exit(0)


# =========================================================
# NORMAL CLIENT MODE
# =========================================================
if args.host and args.port:

    client_mode(args)

else:

    parser.print_help()
