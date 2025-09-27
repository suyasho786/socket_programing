import socket

s = socket.socket()


s.bind(("0.0.0.0", 9090))


s.listen()
print("server is listening")
while True:
    

    
    conn, addr = s.accept()

    # print("server connected to ", addr)

    msg_cl = conn.recv(1024).decode()
    if(msg_cl == "exit"):
        break
    newMsg = msg_cl
    conn.send(newMsg.encode())


conn.close()
s.close()