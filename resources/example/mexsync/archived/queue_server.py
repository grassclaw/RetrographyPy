from multiprocessing.managers import BaseManager
from multiprocessing import Lock

# I created a manager to expose the Queue and Lock
class QueueManager(BaseManager): pass

if __name__ == "__main__":
    from multiprocessing import Queue

    # This is to ensure the processes are using the same queue
    queue = Queue()
    lock = Lock()

    # Registershared queue and lock with manager
    QueueManager.register('get_queue', callable=lambda: queue)
    QueueManager.register('get_lock', callable=lambda: lock)

    # Start the manager on a specific address and port
    manager = QueueManager(address=('', 50000), authkey=b'secret')

    # Start the manager server
    server = manager.get_server()
    print("Queue server is running...")

    # Run the server indefinitely
    server.serve_forever()
