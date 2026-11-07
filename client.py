import socket
import sys
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad

HOST = "127.0.0.1" 
PORT = 8000 
DES_key = b"BANK2026"   # 8 bytes, 64 bits, 56 bits effective key length (must match the server)


def encrypt(message):
    cipher = DES.new(DES_key, DES.MODE_ECB)
    return cipher.encrypt(pad(message.encode("utf-8"), 8)) # Encode to bytes, pad to a multiple of 8, then encrypt



message = input("Enter a transaction: ")   # Get the transaction message from the user

ciphertext = encrypt(message) 

print(f"Plain text:  {message}")
print(f"Cipher text: {ciphertext.hex().upper()}")
# One line per 8-byte block, so identical blocks are easy to spot (Appendix B)
for i in range(0, len(ciphertext), 8):
    print(f"  Block {i // 8 + 1}: {ciphertext[i:i + 8].hex().upper()}") # Print each 8-byte block in hex format

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Create a TCP socket
client.connect((HOST, PORT))   # Connect to the server (the mainframe)
client.sendall(ciphertext)     # Send all the encrypted bytes
client.close()                 # Closing tells the server the message is complete
print("[CLIENT] Encrypted transaction sent to mainframe.")