import json
import logging
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class Tool:
    def __init__(self, key, socket):
        self.key = key
        self.socket = socket

    def aes_encrypt(self, plaintext):
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        return cipher.iv + ct_bytes

    def aes_decrypt(self, ciphertext):
        iv = ciphertext[:AES.block_size]
        ct = ciphertext[AES.block_size:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ct), AES.block_size)
        return decrypted.decode()

    def recv(self) -> str:
        data = b""
        try:
            while True:
                chunk = self.socket.recv(1024)
                if not chunk:
                    break
                data += chunk
                try:
                    decrypted = self.aes_decrypt(data)
                    return json.loads(decrypted)
                except ValueError:
                    continue
        except Exception as e:
            print(f"Error while receiving data: {e}")

    def send(self,data):
        try:
            msg = json.dumps(data)
            encrypted_msg = self.aes_encrypt(msg)
            self.socket.send(encrypted_msg)
        except (TypeError, ValueError) as e:
            print("some error Happened: ", e)
        except Exception as e:
            print(f"Error sending data: {e}")
