import socket

class EchoClient:

    def __init__(self, port = 8080, address = "127.0.0.1"):
        self.port = port
        self.address = address
    

    def start(self):
        # self.s = socket.socket()
        # self.s.connect((self.address, self.port))
        with socket.socket() as s:
            s.connect((self.address, self.port))

            print(f"[client]connected to server at {self.port}")

            try:
                while True:
                    client_command = input("client> ")

                    if(client_command in ["quit", "exit"]):
                        break
                    s.send(client_command.encode())

                    server_response = s.recv(1024).decode()
                    
                    print("server responded: ", server_response)

            except :
                print("\n[client]: closes the connection")


if __name__ == "__main__":
    client = EchoClient()

    client.start()


