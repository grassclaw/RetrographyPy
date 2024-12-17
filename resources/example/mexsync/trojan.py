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
DECODING_REVERSE = {v: k for k, v in ENCODING.items()}  # Delay -> Bits (optional)
EOM_SIGNAL = 3.0  # End-of-message signal (3 seconds)
SWITCH_MARKER = '1111'  # Special marker to switch roles
SIGNATURE = '11111111'  # Unique start marker, I wanted to make this dynamic but no go
EOM_THRESHOLD = 2.5  # End-of-message signal threshold

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
        signature = SIGNATURE
        # Generate dynamic signature
        # signature = generate_dynamic_signature(message)
        # Add a signature and group into 4-bit chunks
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

def send_switch_marker():
    """Send a switch marker to signal the Spy to respond."""
    print("Trojan: Sending switch marker...")
    send_multibit(SWITCH_MARKER)

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

def receive_multibit():
    """Receive 4-bit chunks based on timing, record after detecting the signature."""
    recorded_bits = []  # List to store all bits after the signature
    buffer = ""         # Temporary buffer to detect the signature
    recording = False   # Flag to start recording bits
    signature = SIGNATURE

    while True:
        start_time = time.perf_counter()
        win32event.WaitForSingleObject(mutex, win32event.INFINITE)
        elapsed_time = time.perf_counter() - start_time
        win32event.ReleaseMutex(mutex)

        if elapsed_time > EOM_THRESHOLD:
            if recording:
                print("Trojan: End-of-message signal detected. Recording complete.")
            break  # Stop recording on EOM signal

        # Decode the timing into bits
        closest = min(DECODING_REVERSE.keys(), key=lambda x: abs(x - elapsed_time))
        bits = DECODING_REVERSE[closest]
        print(f"Trojan: Received bits {bits} (Elapsed time: {elapsed_time:.3f}s)")

        if not recording:
            # Append bits to buffer until the signature is found
            buffer += bits
            if signature in buffer:
                print("Trojan: Signature detected! Starting to record bits.")
                recording = True
                buffer = buffer[buffer.find(signature) + len(signature):]  # Remove the signature
                recorded_bits.append(buffer)  # Add leftover bits after the signature
        else:
            # Append bits until EOM signal is received
            recorded_bits.append(bits)

    # Ensure alignment to 8 bits
    binary_stream = ''.join(recorded_bits)
    if len(binary_stream) % 8 != 0:
        padding_length = 8 - (len(binary_stream) % 8)
        binary_stream = binary_stream[:-padding_length]  # Trim extra padding
        print(f"Trojan: Trimmed {padding_length} bits of extra padding.")

    return binary_stream

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
    #     message = input("Enter the message to send: ")
    #     binary_quads = message_to_binary(message)

    #     start_time = time.time()
    #     for bits in binary_quads:
    #         send_multibit(bits)
    #     send_eom()

    #     total_time = time.time() - start_time
    #     total_bits = len(binary_quads) * 4
    #     kbps = (total_bits / total_time) / 1000

    #     binary_string = ''.join(binary_quads)
    #     print(f"Trojan: Full message sent: {binary_string}")
    #     print(f"Trojan: Transmission completed in {total_time:.2f} seconds")
    #     print(f"Trojan: Throughput: {kbps:.2f} kbps")
    # finally:
    #     win32api.CloseHandle(mutex)
        while True:
                    # Send a message
                    message = input("Enter the message to send (or 'exit' to quit): ")
                    if message.lower() == "exit":
                        break

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

                    # Wait for a response
                    print("Trojan: Waiting for response...")
                    response_bits = receive_multibit()

                    # Combine the received bits into a binary string
                    response_binary = ''.join(response_bits)
                    print(f"Trojan: Combined response binary stream: {response_binary}")

                    # Decompress the response
                    response_message = decompress_message(response_binary)
                    print(f"Trojan: Response received: {response_message}")

                    if response_message and response_message.lower() == "exit":
                        print("Trojan: Spy exited communication.")
                        break
    finally:
        win32api.CloseHandle(mutex)