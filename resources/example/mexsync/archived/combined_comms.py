import multiprocessing
import time

# AFTER LOTS of troubleshooting...
# I combined everything under one script.
# Giving everything another go. I'm not sure if it's the python or 
# the fact I use a mac. Lot's of examples online are not as
# useful as I though due to limitations all based around that.
def text_to_binary(message):
    """Convert text message to binary representation."""
    return ''.join(format(ord(char), '08b') for char in message)

def trojan(queue, message):
    binary_message = text_to_binary(message)
    print(f"Trojan: Converted message '{message}' to binary: {binary_message}")
    
    # Put the entire binary message into the queue
    queue.put(binary_message)
    
    print("Trojan: Binary message sent!")
    
    # Simulate a short delay to mimic transmission time
    time.sleep(2)

def spy(queue):
    # Wait for the Trojan to send the binary message
    print("Spy: Waiting for message...")
    
    # Get the binary message from the shared queue
    binary_message = queue.get()  # This will block until a message is received
    
    print(f"Spy: Received binary message: {binary_message}")
    
    # Simulate processing the received message
    time.sleep(1)
    
    print("Spy: Finished processing the message")

if __name__ == "__main__":
    # Create a shared queue for communication
    queue = multiprocessing.Queue()

    # Accept a non-binary message as input from the user
    message = input("Enter the message to send: ").strip()

    # Start both Trojan and Spy processes using the same queue
    trojan_process = multiprocessing.Process(target=trojan, args=(queue, message))
    spy_process = multiprocessing.Process(target=spy, args=(queue,))

    # Start both processes
    trojan_process.start()
    spy_process.start()

    # Wait for both processes to finish
    trojan_process.join()
    spy_process.join()
