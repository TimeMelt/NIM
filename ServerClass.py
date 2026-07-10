"""
    Server
    =======

    - This is the server class that allows queues to be visible across multiple threads
    - also manages log files that for displaying weights and expectation values over each round/epoch

"""

from pathlib import Path
from multiprocessing import Queue
from multiprocessing.managers import BaseManager
import threading, os
from Config import settings

class QueueManager(BaseManager): pass

class Server(threading.Thread):
    def __init__(self, queue_count):
        super().__init__()
        self.queue_list = { f"get_queue_{_}": Queue() for _ in range(queue_count)}
        for name, qobj in self.queue_list.items():
            QueueManager.register(name, callable=lambda q=qobj: q)
        self.manager = QueueManager(address=(settings["queue_address"], settings["queue_port"]), authkey=settings["queue_authkey"])
        self.server = self.manager.get_server()

    def run(self):
        try:
            os.makedirs(settings["log_dir"])
            print("logs directory initialized.")
        except:
            print("logs directory already exists, cleaning now...")
            for log_file in Path(f"./{settings["log_dir"]}").glob('*.log'):
                if log_file.is_file():
                    log_file.unlink()
                    print(f"Deleted: {log_file.name}")
        try:
            print("server running...")
            self.server.serve_forever()
        except:
            print("server failed.")

if __name__ == "__main__":
    servo = Server(settings["node_count"])
    servo.start()
