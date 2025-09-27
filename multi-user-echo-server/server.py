import socket
import threading


class ClientHandler(threading.Thread):
    def __init__(self, client_socket, client_id, address):
        super().__init__()
        self.client_socket = client_socket
        self.client_id = client_id
        self.address = address
    
    def run(self):
        
        print(f"[client-{self.client_id}] connected from {self.address} ")
        
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break

                print(f"[Client-{self.client_id} Sent : {data.decode()}]")

                self.client_socket.sendall(data)

        except Exception as e:
            print(f"[Client-{self.client_id}] Error: {e}")

        finally:
            self.client_socket.close()
            print(f"[Client -{self.client_id}] Disconnected")


class EchoServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.s = socket.socket()
        self.client_id = 0
    def start(self):

        
        self.s.bind((self.host, self.port))
        self.s.listen()
        print(f"[SERVER] is listening on {self.host}:{self.port}")
        

        try:
            while True:
                client_socket, address = self.s.accept()
                self.client_id += 1 
                handler = ClientHandler(client_socket, self.client_id, address)
                handler.start()

        except KeyboardInterrupt:
            print("\n server is shutting down...")

        finally:
            self.s.close()



if __name__ == "__main__":
    
    server = EchoServer("0.0.0.0", 8080)
    server.start()

