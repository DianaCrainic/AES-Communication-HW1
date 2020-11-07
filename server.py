import sys
import os
import socket
import hashlib
from Crypto.Cipher import AES


k_prim = "1234567890123456"


def generate_key():
    k = os.urandom(16)  # ECB or CFB
    return k


def server_program(port):
    host = socket.gethostname()

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(1)
    conn, address = server_socket.accept()
    print("M-am conectat cu nodul A")
    
    k = generate_key()
    aes = AES.new(k_prim, AES.MODE_ECB)
    
    conn.send(aes.encrypt(k))
    print("TRIMIT LUI A CHEIA K CRIPTATA: ", aes.encrypt(k))
        

    conn.close() 

if __name__ == '__main__':
    port = int(sys.argv[1])
    server_program(port)