from multiprocessing.managers import BaseManager
import os
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

# Encryption helper functions
# I largely had help from stackoverflow on this.
def encrypt_message(key, message):
    """Encrypt the message using AES."""
    iv = os.urandom(16)  # Initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()
    encrypted_message = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_message  # Send the IV with the encrypted message

if __name__ == "__main__":
    # LOTS of this is in documentation and is common knowledge.
    # I didn't invent anything new here.
    # Connect to the queue server running on localhost:50000
    # I was originally trying to do it on two scripts which 
    # failed and I finally realized they weren't sharing the same queue
    class QueueManager(BaseManager): pass
    QueueManager.register('get_queue')
    QueueManager.register('get_lock')

    manager = QueueManager(address=('localhost', 50000), authkey=b'secret')
    manager.connect()  # Connect to the server

    # Get the shared queue and lock
    queue = manager.get_queue()
    lock = manager.get_lock()

    # I wanted to practice doing a handshake encryption key
    # Generate a symmetric encryption key for AES (256-bit key)
    encryption_key = os.urandom(32)

    # Demonstrate mutual exclusion
    # Explicitly acquire and release the lock 
    lock.acquire()
    try:
        # Perform the handshake by sending the encryption key
        queue.put(encryption_key)
        print("Trojan: Handshake completed. Encryption key sent.")

        # Accept a message as input from the user
        message = input("Enter the message to send: ").strip()

        # Encrypt and send the message
        encrypted_message = encrypt_message(encryption_key, message)
        queue.put(encrypted_message)
        print(f"Trojan: Encrypted message sent!")
    finally:
        # Release the lock after the critical section
        lock.release()

    # Simulate a short delay to mimic transmission time
    time.sleep(1)
