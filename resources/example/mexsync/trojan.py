import time
import win32event
import win32api
import zlib  # For potential compression

# Constants
MUTEX_NAME = "Global\\MexSyncMutex" #Same Mutex name
# So this makes me wonder though...I guess whoever is communicating needs to agree on mutex name in this case beforehand right?
ENCODING = {
    '00': 0.5,  # "00" mapped to 1-second delay, etc.
    '01': 1.0,
    '10': 1.5,
    '11': 2.0
}
EOM_SIGNAL = 3.0  # End-of-message signal (3 seconds)
# https://learn.microsoft.com/en-us/windows/win32/sync/using-mutex-objects
# Used this source to understand how named mutexes work in Windows for interprocess communication.

# Create or open a named mutex. Apparently, Win32 doesn’t care if it already exists; it’ll just reuse it.
mutex = win32event.CreateMutex(None, False, MUTEX_NAME)

def message_to_binary(message):
    # Optionally compress the message
    # Uncomment this block to enable compression
    # try:
    #     message = zlib.compress(message.encode()).decode()
    #     print("Trojan: Message compressed successfully")
    # except Exception as e:
    #     print(f"Trojan: Failed to compress message: {e}")

    # Convert each character to binary and group bits into pairs
    # Inspired by: https://stackoverflow.com/questions/7396849
    # This one-liner converts a string to binary. I adapted it to group bits into pairs for multibit encoding.
    binary_stream = ''.join(format(ord(char), '08b') for char in message)
    grouped_bits = [binary_stream[i:i+2] for i in range(0, len(binary_stream), 2)]
    print(f"Trojan: Message converted to binary pairs: {grouped_bits}")
    return grouped_bits

def send_multibit(bits):
    # Sends multibit data by timing delays. This part feels like semaphore communication, but who’s counting?
    delay = ENCODING[bits] # Map bits to their respective delay
    win32event.WaitForSingleObject(mutex, win32event.INFINITE)
    print(f"Trojan: Sending bits {bits} with delay {delay}s")
    time.sleep(delay)# The covert signal is... waiting.
    win32event.ReleaseMutex(mutex) #SPY's turn now...woot

def send_eom():
    # Special signal to let the Spy know we're done transmitting. Inspired by "end-of-file" logic in file transfers.
    win32event.WaitForSingleObject(mutex, win32event.INFINITE)
    print("Trojan: Sending end-of-message signal")
    time.sleep(EOM_SIGNAL) # Big delay = "Done!"
    win32event.ReleaseMutex(mutex)

if __name__ == "__main__":
    try:
        # Input the secret message to transmit covertly
        message = input("Enter the message to send: ")

        binary_pairs = message_to_binary(message)
        
        start_time = time.time()
        for bits in binary_pairs:
            send_multibit(bits) #send bit pairs
        send_eom() #end transmission signal
        total_time = time.time() - start_time

        # Calculate and print performance metrics
        total_bits = len(binary_pairs) * 2 #same as spy, 2 bits per enc.
        kbps = (total_bits / total_time) / 1000 #KBPS, same as spy
        print(f"Trojan: Transmission completed in {total_time:.2f} seconds")
        print(f"Trojan: Throughput: {kbps:.2f} kbps")
    finally:
        win32api.CloseHandle(mutex) #clean up
