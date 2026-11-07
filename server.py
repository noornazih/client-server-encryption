import socket
from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad

HOST = "127.0.0.1"
PORT = 8000 
DES_key = b"BANK2026"   # 8 bytes, 64 bits, 56 bits effective key length


def decrypt(ciphertext):
    cipher = DES.new(DES_key, DES.MODE_ECB)
    return unpad(cipher.decrypt(ciphertext), 8).decode("utf-8") # Remove padding and decode to string


def receive_all(connection): # Receive all data from the connection until the client closes it
    data = b"" 
    while True:
        chunk = connection.recv(1024) 
        if not chunk: # If no more data is received, break the loop
            break
        data += chunk
    return data


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Create a TCP socket
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow the socket to be reused immediately after the program exits
server.bind((HOST, PORT))
server.listen(1)
print(f"[SERVER] Mainframe listening on {HOST}:{PORT} ...")

while True:
    connection, address = server.accept()
    print(f"\n[SERVER] Connection from {address[0]}:{address[1]}")

    ciphertext = receive_all(connection)
    connection.close()

    print(f"Cipher text: {ciphertext.hex().upper()}")
    # One line per 8-byte block, so identical blocks are easy to spot (Appendix B)
    for i in range(0, len(ciphertext), 8):
        print(f"  Block {i // 8 + 1}: {ciphertext[i:i + 8].hex().upper()}") # Print each 8-byte block in hex format

    try:
        print(f"Plain text: {decrypt(ciphertext)}")
    except ValueError:
        print("Message is corrupted! (wrong key or bad padding)")