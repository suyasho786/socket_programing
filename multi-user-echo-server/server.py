import socket
import threading
import queue

class ClientHandler(threading.Thread):
    def __init__(self, task_queue, worker_id):
        super().__init__(daemon=True)
        self.task_queue = task_queue
        self.worker_id = worker_id

    def run(self):
        while True:
            conn, client_id, address = self.task_queue.get()
            try:
                print(f"[Worker-{self.worker_id}] Connected to Client-{client_id} at {address}")
                while True:
                    data = conn.recv(1024)
                    if not data:  
                        break
                    client_msg = data.decode().strip()
                    print(f"[Client-{client_id}] Message: {client_msg}")
                    # send back as bytes
                    conn.sendall((client_msg + '\n').encode())
            except Exception as e:
                print(f"[Worker-{self.worker_id}] Error Client-{client_id}: {e}")
            finally:
                conn.close()                  
                self.task_queue.task_done()
                print(f"[Worker-{self.worker_id}] Finished Client-{client_id}")


class EchoServer:
    def __init__(self, host="0.0.0.0", port=8081, num_workers=3):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # allow immediate reuse of the port
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.num_workers = num_workers
        self.task_queue = queue.Queue()
        self.client_id = 0

    def run_workers(self):
        for i in range(self.num_workers):
            handler = ClientHandler(self.task_queue, i + 1)
            handler.start()
        print(f"[SERVER] Started with {self.num_workers} worker threads")

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"[SERVER] Listening on {self.host}:{self.port}")

        self.run_workers()

        try:
            while True:
                conn, addr = self.socket.accept()
                self.client_id += 1
                print(f"[SERVER] Accepted Client-{self.client_id} from {addr}")
                self.task_queue.put((conn, self.client_id, addr))
        except KeyboardInterrupt:
            print("\n[SERVER] Shutting down...")
        finally:
            self.socket.close()


if __name__ == "__main__":
    server = EchoServer("0.0.0.0", 8081, num_workers=3)
    server.start()
