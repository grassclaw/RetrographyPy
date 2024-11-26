import time
import win32event
import win32api

# Constants
MUTEX_NAME = "Global\\MexSyncMutex"
ENCODING = {
    '00': 0.5,
    '01': 1.0,
    '10': 1.5,
    '11': 2.0
}
EOM_SIGNAL = 3.0  # End-of-message signal (3 seconds)

# Create or open a named mutex
mutex = win32event.CreateMutex(None, False, MUTEX_NAME)

def message_to_binary(message):
    # Convert each character to binary and group bits into pairs
    binary_stream = ''.join(format(ord(char), '08b') for char in message)
    grouped_bits = [binary_stream[i:i+2] for i in range(0, len(binary_stream), 2)]
    print(f"Trojan: Message converted to binary pairs: {grouped_bits}")
    return grouped_bits

def send_multibit(bits):
    delay = ENCODING[bits]
    win32event.WaitForSingleObject(mutex, win32event.INFINITE)
    print(f"Trojan: Sending bits {bits} with delay {delay}s")
    time.sleep(delay)
    win32event.ReleaseMutex(mutex)

def send_eom():
    win32event.WaitForSingleObject(mutex, win32event.INFINITE)
    print("Trojan: Sending end-of-message signal")
    time.sleep(EOM_SIGNAL)
    win32event.ReleaseMutex(mutex)

if __name__ == "__main__":
    try:
        message = input("Enter the message to send: ")
        binary_pairs = message_to_binary(message)
        
        start_time = time.time()
        for bits in binary_pairs:
            send_multibit(bits)
        send_eom()
        total_time = time.time() - start_time

        # Calculate and print performance metrics
        total_bits = len(binary_pairs) * 2
        kbps = (total_bits / total_time) / 1000
        print(f"Trojan: Transmission completed in {total_time:.2f} seconds")
        print(f"Trojan: Throughput: {kbps:.2f} kbps")
    finally:
        win32api.CloseHandle(mutex)
