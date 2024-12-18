import socket
import json
import termcolor

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
    (prompt)
    print(recv())


