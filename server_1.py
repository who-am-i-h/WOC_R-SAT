import socket
import json
import termcolor
from rich.console import Console
from rich.table import Table
from rich.live import Live
import time

def rich_stats(cpu_percent, V_ram, dsk_usage):
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



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "localhost"
PORT = 6969

s.bind((HOST, PORT))
s.listen(1)

conn, addr = s.accept()

def send(data):
    msg = json.dumps(data)
    conn.send(msg.encode())

def color_text(text, color):
    return termcolor.colored(text, color)

print(color_text("this is just for test", "red"))
def recv() -> str:
    data = ""
    while True:
        try:
            data = data + conn.recv(1024).decode().rstrip()
            return json.loads(data) 
        except ValueError:
            continue
while True:
    prompt = input("[" + color_text("*", "blue")+ "]"+ color_text("Connected to ", "green") + f"{addr}~ ")
    send(prompt)
    from_client = recv()
    if from_client.startswith("####CPUM#### "):
        initial = from_client.split("####CPUM#### ")[1].split("-")
        rich_stats(initial[0], initial[1], initial[2])
    else:
        print(from_client)


