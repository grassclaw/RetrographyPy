import time
import win32event
import win32api
import zlib
import hashlib


# Constants
MUTEX_NAME = "Global\\MexSyncMutex"
ENCODING = {
    '0000': 0.01, '0001': 0.02, '0010': 0.03, '0011': 0.04,
    '0100': 0.05, '0101': 0.06, '0110': 0.07, '0111': 0.08,
    '1000': 0.09, '1001': 0.10, '1010': 0.11, '1011': 0.12,
    '1100': 0.13, '1101': 0.14, '1110': 0.15, '1111': 0.16
}
EOM_SIGNAL = 3.0  # End-of-message signal (3 seconds)

# Create or open a named mutex
mutex = win32event.CreateMutex(None, False, MUTEX_NAME)

# def generate_dynamic_signature(message, key="shared_key"):
#     """Generate a dynamic signature using a hash of the key and message."""
#     combined = key + message
#     hash_digest = hashlib.sha256(combined.encode()).hexdigest()  # SHA-256 hash
#     signature = bin(int(hash_digest[:2], 16))[2:].zfill(8)  # First 8 bits as binary
#     print(f"Trojan: Generated dynamic signature: {signature}")
#     return signature

def message_to_binary(message):
    """Compress a message, add a signature, and group into 4-bit chunks."""
    try:
        # Compress the message using zlib
        compressed_data = zlib.compress(message.encode())
        print(f"Trojan: Compressed data: {compressed_data}")

        # Convert compressed bytes to binary string
        compressed_binary = ''.join(format(byte, '08b') for byte in compressed_data)
        print(f"Trojan: Compressed binary: {compressed_binary}")

        # Generate dynamic signature
        # signature = generate_dynamic_signature(message)
        # Add a signature and group into 4-bit chunks
        signature = '11111111'  # Unique start marker
        binary_stream = signature + compressed_binary  # Use the compressed binary, not the raw message
        print(f"Trojan: Binary stream with signature: {binary_stream}")

        # Ensure the binary string is divisible by 4 for clean chunks
        if len(binary_stream) % 4 != 0:
            padding_length = 4 - (len(binary_stream) % 4)
            binary_stream += '0' * padding_length
            print(f"Trojan: Added {padding_length} bits of padding.")

        grouped_bits = [binary_stream[i:i+4] for i in range(0, len(binary_stream), 4)]
        print(f"Trojan: Message with signature and padding: {grouped_bits}")
        return grouped_bits
    except Exception as e:
        print(f"Error: {e}")
        return None

def send_multibit(bits):
    """Send 4-bit chunks using timing delays."""
    delay = ENCODING[bits]
    win32event.WaitForSingleObject(mutex, win32event.INFINITE)
    print(f"Trojan: Sending bits {bits} with delay {delay:.2f}s")
    time.sleep(delay)
    win32event.ReleaseMutex(mutex)

def send_eom():
    """Send end-of-message signal."""
    win32event.WaitForSingleObject(mutex, win32event.INFINITE)
    print("Trojan: Sending end-of-message signal")
    time.sleep(EOM_SIGNAL)
    win32event.ReleaseMutex(mutex)

if __name__ == "__main__":
    try:
        message = input("Enter the message to send: ")
        binary_quads = message_to_binary(message)

        start_time = time.time()
        for bits in binary_quads:
            send_multibit(bits)
        send_eom()

        total_time = time.time() - start_time
        total_bits = len(binary_quads) * 4
        kbps = (total_bits / total_time) / 1000

        binary_string = ''.join(binary_quads)
        print(f"Trojan: Full message sent: {binary_string}")
        print(f"Trojan: Transmission completed in {total_time:.2f} seconds")
        print(f"Trojan: Throughput: {kbps:.2f} kbps")
    finally:
        win32api.CloseHandle(mutex)
