import sys
import socket
from Crypto.Cipher import AES
from Crypto import Random

BLOCKSIZE = 16

k_prim = "1234567890123456"
iv = "1212312341234567"

def pad(block):
    padding_length = BLOCKSIZE - (len(block) % BLOCKSIZE)
    return block + padding_length * chr(padding_length)


def xor_bytes(a, b):
    return b''.join([bytes([i ^ j]) for i, j in zip(a, b)])


def encrypt_CFB(decrypted_key, current_block, iv):
    cipher = AES.new(decrypted_key, AES.MODE_ECB)
    encrypted_block = cipher.encrypt(iv)
    return xor_bytes(encrypted_block, current_block)


def client_program(port1, port2):
    host = socket.gethostname() 

    client_socket1 = socket.socket()
    client_socket1.connect((host, port1)) 
    client_socket2 = socket.socket()
    client_socket2.connect((host, port2))

    mode = input(" Modul de criptare este -> ")  # take input

    client_socket2.send(mode.encode())  # B

    #astept cheia de la server
    encrypted_key = client_socket1.recv(16)

    print("Cheia criptata de la KM:", encrypted_key)

    client_socket2.send(encrypted_key)
    print("TRIMIT LUI B CHEIA CRIPTATA ")

    cipher = AES.new(k_prim, AES.MODE_ECB)
    decrypted_key = cipher.decrypt(encrypted_key)

    #astept initializarea comunicarii de la B
    print("Confirm initializarea comunicarii. ")
    client_socket2.recv(8)

    cipher = AES.new(decrypted_key, AES.MODE_ECB)

    first_iteration = 0
    eof = 1
    f = open("file.txt", 'r')

    encrypted_block1 = ""
    while eof:
        block = f.read(BLOCKSIZE)

        print("\nBLOCUL DE CRIPTAT ESTE: ", block)

        if len(block) != BLOCKSIZE:
            eof = 0
            block = pad(block)

        if mode == "ecb":
            encrypted_block = cipher.encrypt(block)
            client_socket2.send(encrypted_block)
            print("BLOCUL TRIMIS LUI B ESTE: ", encrypted_block)

        else:

            if first_iteration == 0:
                encrypted_block1 = encrypt_CFB(decrypted_key, block.encode(), iv.encode())
                first_iteration = first_iteration + 1
                print("BLOCUL TRIMIS ESTE: ", encrypted_block1)
                client_socket2.send(encrypted_block1)
            else:
                encrypted_block = encrypt_CFB(decrypted_key, block.encode(), encrypted_block1)

                print("BLOCUL TRIMIS ESTE: ", encrypted_block)

                client_socket2.send(encrypted_block)

    client_socket1.close()  # close the connection
    client_socket2.close()


if __name__ == '__main__':
    port1 = int(sys.argv[1])
    port2 = int(sys.argv[2])
    client_program(port1, port2)
