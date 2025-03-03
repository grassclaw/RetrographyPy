import time
import win32event
import win32api
import random

# Constants
MUTEX_NAME = "Global\\MexSyncMutex"
ENCODING = {
    '0000': 0.01, '0001': 0.02, '0010': 0.03, '0011': 0.04,
    '0100': 0.05, '0101': 0.06, '0110': 0.07, '0111': 0.08,
    '1000': 0.09, '1001': 0.10, '1010': 0.11, '1011': 0.12,
    '1100': 0.13, '1101': 0.14, '1110': 0.15, '1111': 0.16
}
DECODING_REVERSE = {v: k for k, v in ENCODING.items()}  # Reverse lookup for decoding
EOM_SIGNAL = 3.0  # End-of-message signal (3 seconds)
SWITCH_MARKER = '1111'  # Special marker to switch roles
SIGNATURE = '11111111'  # Start marker
EOM_THRESHOLD = 2.5  # End-of-message signal threshold

# Create or open a named mutex
mutex = win32event.CreateMutex(None, False, MUTEX_NAME)

### MESSAGE ENCODING/DECODING ###
def message_to_binary(message):
    """Convert a message to binary and add a signature."""
    binary_stream = SIGNATURE + ''.join(format(ord(char), '08b') for char in message)
    grouped_bits = [binary_stream[i:i+4] for i in range(0, len(binary_stream), 4)]

    print(f"DEBUG: Message '{message}' -> Binary: {binary_stream}")  # Debugging output
    return grouped_bits

def binary_to_message(binary_string):
    """Convert binary string to a message."""
    if len(binary_string) % 8 != 0:
        print("Receiver: Binary data is not aligned to 8 bits, fixing...")
        padding_needed = 8 - (len(binary_string) % 8)
        binary_string = binary_string.ljust(len(binary_string) + padding_needed, '0')  # Pad to align

    byte_chunks = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    print(f"Receiver: Byte chunks: {byte_chunks}")  # Debugging output

    try:
        message = ''.join(chr(int(byte, 2)) for byte in byte_chunks)
    except ValueError:
        print("Receiver: Error decoding binary to ASCII.")
        message = "ERROR: Decoding failed"
    
    return message

### MESSAGE TRANSMISSION ###
def send_multibit(bits):
    """Send 4-bit chunks using timing delays with jitter for stealth."""
    base_delay = ENCODING[bits]
    jitter = random.uniform(-0.005, 0.005)  # Small random jitter
    delay = base_delay + jitter

    win32event.WaitForSingleObject(mutex, win32event.INFINITE)
    print(f"Sent bits {bits} with delay {delay:.3f}s (base: {base_delay:.3f}s, jitter: {jitter:.3f}s)")
    time.sleep(delay)
    win32event.ReleaseMutex(mutex)

def send_eom():
    """Send end-of-message signal."""
    print("Sender: Sending End-of-Message (EOM) signal.")
    win32event.WaitForSingleObject(mutex, win32event.INFINITE)
    time.sleep(EOM_SIGNAL)
    win32event.ReleaseMutex(mutex)

def send_switch_marker():
    """Send switch marker to signal role switch."""
    print("Sender: Sending Switch Marker.")
    send_multibit(SWITCH_MARKER)

### MESSAGE RECEPTION ###
def receive_multibit():
    """Receive 4-bit chunks based on timing, record after detecting the signature."""
    recorded_bits = []
    buffer = ""
    recording = False

    while True:
        start_time = time.perf_counter()
        win32event.WaitForSingleObject(mutex, win32event.INFINITE)
        elapsed_time = time.perf_counter() - start_time
        win32event.ReleaseMutex(mutex)

        if elapsed_time > EOM_THRESHOLD:
            if recording:
                print("Receiver: End-of-message signal detected.")
            break  # Stop recording on EOM signal

        # Ensure timing matches expected values
        if not any(abs(x - elapsed_time) < 0.01 for x in DECODING_REVERSE.keys()):
            print(f"Receiver: Ignoring unexpected timing {elapsed_time:.3f}s")
            continue  # Skip invalid readings

        # Decode timing into bits
        closest = min(DECODING_REVERSE.keys(), key=lambda x: abs(x - elapsed_time))
        bits = DECODING_REVERSE[closest]

        print(f"Receiver: Detected elapsed time {elapsed_time:.3f}s -> Received bits {bits}")

        if not recording:
            buffer += bits
            if SIGNATURE in buffer:
                print("Receiver: Signature detected! Starting to record bits.")
                recording = True
                buffer = buffer[buffer.find(SIGNATURE) + len(SIGNATURE):]
                recorded_bits.append(buffer)
        else:
            recorded_bits.append(bits)

    # Ensure received binary is aligned to 8-bit chunks
    received_binary = ''.join(recorded_bits)
    if len(received_binary) % 8 != 0:
        padding_needed = 8 - (len(received_binary) % 8)
        received_binary = received_binary.ljust(len(received_binary) + padding_needed, '0')  # Pad with zeros
        print(f"Receiver: Added {padding_needed} bits of padding for alignment.")

    print(f"Receiver: Full received binary: {received_binary}")
    return received_binary

### MAIN FUNCTION ###
def main():
    print("Select role: [T]rojan (Sender) | [S]py (Receiver)")
    role = input("Enter role (T/S): ").strip().upper()

    if role == "T":
        while True:
            message = input("Enter the message to send (or 'exit' to quit): ")
            if message.lower() == "exit":
                break

            binary_quads = message_to_binary(message)
            for bits in binary_quads:
                send_multibit(bits)
            send_eom()

            print("Waiting for response...")

            while True:
                response_binary = receive_multibit()
                
                if response_binary.strip() == "":  # Ignore empty responses
                    print("No valid response received, waiting...")
                    time.sleep(0.1)  # Prevent CPU overuse
                    continue
                
                response_message = binary_to_message(response_binary)
                print(f"Response received: {response_message}")
                break  # Exit loop when a valid response is received

    elif role == "S":
        while True:
            print("Listening for incoming message...")
            received_binary = receive_multibit()
            message = binary_to_message(received_binary)
            print(f"Message received: {message}")

            response = input("Enter response (or 'exit' to quit): ").strip()
            if not response:
                response = "ACK"  # Default acknowledgment if no response is given
            if response.lower() == "exit":
                break

            response_binary = message_to_binary(response)
            for bits in response_binary:
                send_multibit(bits)
            send_switch_marker()
            send_eom()

    else:
        print("Invalid selection. Please restart and choose 'T' or 'S'.")

if __name__ == "__main__":
    main()
