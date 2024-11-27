import time
import win32event
import win32api
# import zlib  # For potential compression handling

# Constants
MUTEX_NAME = "Global\\MexSyncMutex" # Name matches Trojan to share instance
DECODING = {
    0.5: '00', # Decode 1.0s as "00", etc.
    1.0: '01',
    1.5: '10',
    2.0: '11'
}
EOM_THRESHOLD = 2.5  # Detect end-of-message signal threshold(3 seconds)

# Inspired by: https://learn.microsoft.com/en-us/windows/win32/sync
# Studied Win32 API for mutex behavior to understand how WaitForSingleObject works.
# Wait for the Trojan to create the mutex
while True:
    try:
        # Open an existing mutex created by Trojan...
        # it seemed to work though even if SPY started it
        mutex = win32event.OpenMutex(win32event.SYNCHRONIZE, False, MUTEX_NAME)
        print("Spy: Mutex found!")
        break
    except Exception:
        print("Spy: Waiting for Trojan to create the mutex...")
        time.sleep(0.1)

# Measures the delay between acquiring the mutex and decodes it into bits.
def receive_multibit():
    start_time = time.perf_counter()
    win32event.WaitForSingleObject(mutex, win32event.INFINITE)
    elapsed_time = time.perf_counter() - start_time
    win32event.ReleaseMutex(mutex)
    if elapsed_time > EOM_THRESHOLD:# End-of-message detection
        return None  # Return None to indicate the transmission is over
    # Find the closest matching delay in DECODING (source: trial and error + common sense)
    closest = min(DECODING.keys(), key=lambda x: abs(x - elapsed_time))
    bits = DECODING[closest]
    print(f"Spy: Received bits {bits} (Elapsed time: {elapsed_time:.2f}s)")
    return bits

if __name__ == "__main__":
    try:
        binary_stream = []
        print("Spy: Receiving binary stream...") # Initial status
        start_time = time.time()
        while True:
            bits = receive_multibit()
            if bits is None: # End-of-message signal received
                break
            binary_stream.append(bits)
        total_time = time.time() - start_time

        # Convert binary stream back into the original message
        binary_string = ''.join(binary_stream)
        message = ''.join(chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8))
    #    # Calculate and print performance metrics...consolidated to one line
    #   total_time = time.time() - start_time
    #         total_bits = len(binary_stream) * 2  # Two bits per encoding
    #         kbps = (total_bits / total_time) / 1000  # Kilobits per second

        # Optionally decompress the message
        # Uncomment this block to handle decompressed data
        # try:
        #     message = zlib.decompress(message.encode()).decode()
        #     print("Spy: Decompressed message successfully")
        # except Exception as e:
        #     print(f"Spy: Failed to decompress message: {e}")

        total_bits = len(binary_stream) * 2
        print(f"Spy: Full message received: {message}")
        print(f"Spy: Transmission completed in {total_time:.2f} seconds")
        print(f"Spy: Throughput: {(total_bits / total_time) / 1000:.2f} kbps")
    finally:
        win32api.CloseHandle(mutex)  # Clean up
