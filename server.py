import socket

host = "127.0.0.1"
port = 2121

with socket.socket() as soket:
    soket.bind((host, port))
    soket.listen()
    conn, addr = soket.accept()
    with conn:
        print("Baglanti yapildi:", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
