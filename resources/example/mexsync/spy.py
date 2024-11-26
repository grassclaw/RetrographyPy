import time
import win32event
import win32api

# Constants
MUTEX_NAME = "Global\\MexSyncMutex"
DECODING = {
    0.5: '00',
    1.0: '01',
    1.5: '10',
    2.0: '11'
}
EOM_THRESHOLD = 2.5  # Threshold to detect end-of-message signal (3 seconds)

# Wait for the Trojan to create the mutex
while True:
    try:
        mutex = win32event.OpenMutex(win32event.SYNCHRONIZE, False, MUTEX_NAME)
        print("Spy: Mutex found!")
        break
    except Exception:
        print("Spy: Waiting for Trojan to create the mutex...")
        time.sleep(0.1)

def receive_multibit():
    start_time = time.perf_counter()
    win32event.WaitForSingleObject(mutex, win32event.INFINITE)
    elapsed_time = time.perf_counter() - start_time
    win32event.ReleaseMutex(mutex)
    if elapsed_time > EOM_THRESHOLD:
        return None  # End-of-message signal detected
    # Decode timing into bits
    closest = min(DECODING.keys(), key=lambda x: abs(x - elapsed_time))
    bits = DECODING[closest]
    print(f"Spy: Received bits {bits} (Elapsed time: {elapsed_time:.2f}s)")
    return bits

if __name__ == "__main__":
    try:
        binary_stream = []
        print("Spy: Receiving binary stream...")
        start_time = time.time()
        while True:
            bits = receive_multibit()
            if bits is None:
                break
            binary_stream.append(bits)
        total_time = time.time() - start_time

        # Convert binary stream back into the original message
        binary_string = ''.join(binary_stream)
        message = ''.join(chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8))
        total_bits = len(binary_stream) * 2

        print(f"Spy: Full message received: {message}")
        print(f"Spy: Transmission completed in {total_time:.2f} seconds")
        print(f"Spy: Throughput: {(total_bits / total_time) / 1000:.2f} kbps")
    finally:
        win32api.CloseHandle(mutex)
