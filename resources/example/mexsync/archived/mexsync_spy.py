from multiprocessing.managers import BaseManager
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

# Decryption helper functions
# Again, lots of stack overflow here.
def decrypt_message(key, encrypted_message):
    """Decrypt the message using AES."""
    iv = encrypted_message[:16]  # Extract the IV from the encrypted message
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message[16:]) + decryptor.finalize()
    #from documentation 
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_message = unpadder.update(decrypted_message) + unpadder.finalize()
    
    return unpadded_message.decode()

if __name__ == "__main__":
    # Connect to the queue server running on localhost:50000
    # Ensuring we're on the same queue. Lots of this from documentation.
    class QueueManager(BaseManager): pass
    QueueManager.register('get_queue')
    QueueManager.register('get_lock')

    manager = QueueManager(address=('localhost', 50000), authkey=b'secret')
    manager.connect()  # Connect to the server

    # Get the shared queue and lock
    queue = manager.get_queue()
    lock = manager.get_lock()

    # Explicitly acquire and release the lock for mutual exclusion
    lock.acquire()
    try:
        # Receive the encryption key
        encryption_key = queue.get()
        print("Spy: Handshake completed. Encryption key received.")

        # Receive the encrypted message
        encrypted_message = queue.get()
        print("Spy: Encrypted message received.")

        # print(encryption_key)
        # print(encrypted_message)
        # Decrypt and display the message
        decrypted_message = decrypt_message(encryption_key, encrypted_message)
        print(f"Spy: Decrypted message: {decrypted_message}")
    finally:
        # Release the lock after the critical section
        lock.release()

    time.sleep(1)
