import socket


s = socket.socket()

s.connect(("127.0.0.1", 9090))

while True:
    msg = input("client > ")

    s.send(msg.encode())
    msg_server = s.recv(1024).decode()

    if(len(msg_server) > 0):
        
        print("message from server to client:", msg_server)
    else:
        break

s.close()

