import socket

host = "127.0.0.1"
port = 2121

with socket.socket() as soket:
    soket.connect((host, port))
    soket.sendall(b"merhaba siber")
    data = soket.recv(1024)
print(data)
