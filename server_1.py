import socket
import json
import termcolor
from rich.console import Console
from rich.table import Table
from rich.live import Live
import time
from Crypto.Cipher import AES
import logging
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

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
# key = get_random_bytes(16)
key = b'just for test123'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "localhost"
PORT = 6969
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()

def show_stats(cpu_percent, V_ram, dsk_usage):
    console = Console()

    def create_table():
        table = Table(title="System Stats")
        table.add_column("Metric", justify="left", style="cyan", no_wrap=True)
        table.add_column("Value", justify="right", style="magenta")
        table.add_row("CPU Usage", f"{cpu_percent}%")
        table.add_row("Memory Usage", f"{V_ram}%")
        table.add_row("Disk Usage", f"{dsk_usage}%")
        return table

    with Live(console=console, refresh_per_second=1):

        console.print(create_table())

def send(data):
    msg = json.dumps(data)
    msg = aes_encrypt(msg, key)
    conn.send(msg)

def color_text(text, color):
    return termcolor.colored(text, color)


def recv() -> str:
    data = b""
    try:
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break
            data += chunk
            try:
                decrypted = aes_decrypt(data, key)
                return json.loads(decrypted)
            except (ValueError, json.JSONDecodeError):
                continue
    except Exception as e:
        return None


print(color_text("this is just for test", "red"))
while True:
    prompt = input("[" + color_text("*", "blue")+ "]"+ color_text("Connected to ", "green") + f"{addr}~ ")
    send(prompt)
    from_client = recv()
    if from_client.startswith("####CPUM#### "):
        initial = from_client.split("####CPUM#### ")[1].split("-")
        show_stats(initial[0], initial[1], initial[2])
    else:
        print(from_client)


