import sys
import socket
import base64
from Crypto.Cipher import AES

k_prim = "1234567890123456"
iv = "1212312341234567"

BLOCKSIZE = 16

def unpad(block):
    padding_length = ord(block[-1])
    if 0 < padding_length < BLOCKSIZE:
        return block[:-padding_length]
    return block

def unpad_CFB(block):
    padding_length = block[-1]
    if 0 < padding_length < BLOCKSIZE:
        return block[:-padding_length]
    return block

def xor_bytes(a, b):
    return b''.join([bytes([i ^ j]) for i, j in zip(a, b)])


def decrypt_CFB(decrypted_key, current_block, iv):
    cipher = AES.new(decrypted_key, AES.MODE_ECB)
    decrypted_block = cipher.encrypt(iv)
    return xor_bytes(decrypted_block, current_block)

def server_program(port):
    host = socket.gethostname()

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(1)
    conn, address = server_socket.accept()
    print("M-am conectat cu nodul A")

    #primirea modului de criptare
    mode = conn.recv(3).decode()
    print("AM PRIMIT MODUL DE CRIPTARE: ", mode)

    # primirea cheii criptate (16 biti)
    encrypted_key = conn.recv(16)
    print("Cheia criptata de la A:", encrypted_key)
    

    # decriptarea cheii - apelarea functiei din biblioteca aes
    cipher = AES.new(k_prim, AES.MODE_ECB)
    decrypted_key = cipher.decrypt(encrypted_key)
    print("Cheia decriptata de la A:", decrypted_key)

    #initierea comunicarii - ex trimiterea unui octet
    message = "12345678"
    conn.send(message.encode())
    print("Am initiat comunicarea cu A")
    final_text = ''

    cipher = AES.new(decrypted_key, AES.MODE_ECB)

    first_iteration = 0
    decrypted_block1 = ""
    first_block = ""


    while True:

        if mode == "ecb":
            block = conn.recv(16)
            print("PRIMESC BLOCUL: ", block)

            decrypted_block = cipher.decrypt(block)

            unpadded_block = unpad(decrypted_block.decode())

            
            print("BLOCUL DECRIPTAT ESTE: ", unpadded_block)
            final_text = final_text + str(unpadded_block)

            if len(unpadded_block) != len(decrypted_block):
                break

        else:
            block = conn.recv(16)
            print("\nPRIMESC BLOCUL: ", block)

            if first_iteration == 0:
                first_iteration = first_iteration + 1

                first_block = block
                decrypted_block1 = decrypt_CFB(decrypted_key, block, iv.encode())

                unpadded_block = unpad_CFB(decrypted_block1)

                new_text = str(unpadded_block)
                final_text = final_text + new_text[2:-1]
                print("BLOCUL ORIGINAL ESTE: ", new_text[2:-1])

                if len(unpadded_block) != len(decrypted_block1):
                    break

            else:
                decrypted_block = decrypt_CFB(decrypted_key, block, first_block)
                unpadded_block = unpad_CFB(decrypted_block)

                new_text = str(unpadded_block)
                final_text = final_text + new_text[2:-1]
                print("BLOCUL ORIGINAL ESTE: ", new_text[2:-1])

                if len(unpadded_block) != len(decrypted_block):
                    break

    print("\nTextul obtinut: ", final_text)

    conn.close() 



if __name__ == '__main__':
    port1 = int(sys.argv[1])
    server_program(port1)
    
