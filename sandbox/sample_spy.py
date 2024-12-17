import time
import win32event
import win32api
import zlib
import hashlib

# Constants
MUTEX_NAME = "Global\\MexSyncMutex"
DECODING = {
    0.01: '0000', 0.02: '0001', 0.03: '0010', 0.04: '0011',
    0.05: '0100', 0.06: '0101', 0.07: '0110', 0.08: '0111',
    0.09: '1000', 0.10: '1001', 0.11: '1010', 0.12: '1011',
    0.13: '1100', 0.14: '1101', 0.15: '1110', 0.16: '1111'
}
EOM_THRESHOLD = 2.5  # End-of-message signal threshold
SIGNATURE = '11111111'  # Unique start marker

# Wait for the Trojan to create the mutex
while True:
    try:
        mutex = win32event.OpenMutex(win32event.SYNCHRONIZE, False, MUTEX_NAME)
        print("Spy: Mutex found!")
        break
    except Exception:
        print("Spy: Waiting for Trojan to create the mutex...")
        time.sleep(0.1)
        
# def generate_dynamic_signature(key="shared_key", message="placeholder"):
#     """Regenerate the dynamic signature using the same key."""
#     combined = key + message
#     hash_digest = hashlib.sha256(combined.encode()).hexdigest()
#     signature = bin(int(hash_digest[:2], 16))[2:].zfill(8)
#     print(f"Spy: Regenerated dynamic signature: {signature}")
    # return signature

def receive_multibit():
    recorded_bits = []  # List to store all bits after the signature
    buffer = ""
    recording = False
    signature = SIGNATURE

    while True:
        start_time = time.perf_counter()
        win32event.WaitForSingleObject(mutex, win32event.INFINITE)
        elapsed_time = time.perf_counter() - start_time
        win32event.ReleaseMutex(mutex)

        if elapsed_time > EOM_THRESHOLD:
            if recording:
                print("Spy: End-of-message signal detected.")
            return recorded_bits  # Return all recorded bits after EOM

        closest = min(DECODING.keys(), key=lambda x: abs(x - elapsed_time))
        bits = DECODING[closest]
        print(f"Spy: Received bits {bits} (Elapsed time: {elapsed_time:.3f}s)")

        if not recording:
            # Append bits to the buffer until the signature is found
            buffer += bits
            if signature in buffer:
                print("Spy: Signature detected! Starting to record bits.")
                recording = True
                buffer = buffer[buffer.find(signature) + len(signature):]  # Remove the signature
                recorded_bits.append(buffer)  # Add any bits after the signature
        else:
            # Append bits to the recorded list
            recorded_bits.append(bits)

def binary_to_ascii(binary_list):
    """Convert 4-bit binary chunks to ASCII message."""
    binary_string = ''.join(binary_list)
    
    # Ensure alignment to 8 bits
    if len(binary_string) % 8 != 0:
        padding_length = 8 - (len(binary_string) % 8)
        binary_string += '0' * padding_length  # Pad with zeros
        print(f"Spy: Added {padding_length} bits of padding for alignment.")
    
    # Split into 8-bit chunks and convert to ASCII
    byte_chunks = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    ascii_chars = [chr(int(byte, 2)) for byte in byte_chunks if len(byte) == 8]
    return ''.join(ascii_chars)

def decompress_message(binary_string):
    """Decompress the binary string using zlib."""
    try:
        # Ensure the binary string is aligned to 8 bits
        if len(binary_string) % 8 != 0:
            padding_length = 8 - (len(binary_string) % 8)
            binary_string = binary_string[:-(padding_length)]  # Remove padding
            print(f"Spy: Removed {padding_length} bits of padding for alignment.")

        # Convert binary string to bytes
        byte_stream = bytes(int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8))
        print(f"Spy: Reconstructed byte stream: {byte_stream}")

        # Decompress the bytes back to the original message
        decompressed_message = zlib.decompress(byte_stream).decode()
        print("Spy: Message successfully decompressed.")
        return decompressed_message
    except Exception as e:
        print(f"Spy: Decompression failed: {e}")
        return "ERROR: Unable to decompress message"

if __name__ == "__main__":
    try:
        print("Spy: Receiving binary stream...")
        start_time = time.time()

        # Call receive_multibit and get all recorded bits after the signature
        recorded_bits = receive_multibit()
        total_time = time.time() - start_time

        # Join the recorded bits into a single binary string
        binary_string = ''.join(recorded_bits)
        print(f"Spy: Combined binary stream: {binary_string}")

        # Decompress the message
        message = decompress_message(binary_string)

        # Output the final message
        print(f"Spy: Full message received: {message}")
        print(f"Spy: Transmission completed in {total_time:.2f} seconds")
    finally:
        win32api.CloseHandle(mutex)
