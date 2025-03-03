import time
import win32event
import win32api

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

# Function to convert messages to binary
def message_to_binary(message):
    """Convert a message to binary and add a signature."""
    binary_stream = SIGNATURE + ''.join(format(ord(char), '08b') for char in message)
    grouped_bits = [binary_stream[i:i+4] for i in range(0, len(binary_stream), 4)]
    return grouped_bits

# Function to convert binary to message
def binary_to_message(binary_string):
    """Convert binary string to a message."""
    byte_chunks = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    message = ''.join(chr(int(byte, 2)) for byte in byte_chunks)
    return message

# Function to send 4-bit chunks
def send_multibit(bits):
    """Send 4-bit chunks using timing delays."""
    delay = ENCODING[bits]
    win32event.WaitForSingleObject(mutex, win32event.INFINITE)
    time.sleep(delay)
    win32event.ReleaseMutex(mutex)

# Function to send end-of-message signal
def send_eom():
    """Send end-of-message signal."""
    win32event.WaitForSingleObject(mutex, win32event.INFINITE)
    time.sleep(EOM_SIGNAL)
    win32event.ReleaseMutex(mutex)

# Function to send switch marker
def send_switch_marker():
    """Send switch marker to signal role switch."""
    send_multibit(SWITCH_MARKER)

# Function to receive bits and detect message
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
                print("End-of-message signal detected.")
            break  # Stop recording on EOM signal

        closest = min(DECODING_REVERSE.keys(), key=lambda x: abs(x - elapsed_time))
        bits = DECODING_REVERSE[closest]

        if not recording:
            buffer += bits
            if SIGNATURE in buffer:
                recording = True
                buffer = buffer[buffer.find(SIGNATURE) + len(SIGNATURE):]
                recorded_bits.append(buffer)
        else:
            if bits == SWITCH_MARKER:
                print("Switch marker detected. Switching roles.")
                break
            recorded_bits.append(bits)

    received_binary = ''.join(recorded_bits)
    print(f"Received binary: {received_binary}")  # Debugging statement
    return received_binary

# Main function for role selection and dynamic switching
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
            response_binary = receive_multibit()
            response_message = binary_to_message(response_binary)
            print(f"Response received: {response_message}")

    elif role == "S":
        while True:
            print("Listening for incoming message...")
            received_binary = receive_multibit()
            message = binary_to_message(received_binary)
            print(f"Message received: {message}")

            response = input("Enter response (or 'exit' to quit): ")
            if response.lower() == "exit":
                break

            response_binary = message_to_binary(response)
            for bits in response_binary:
                send_multibit(bits)
            send_switch_marker()  # Signal Trojan to take control
            send_eom()

    else:
        print("Invalid selection. Please restart and choose 'T' or 'S'.")

if __name__ == "__main__":
    main()
