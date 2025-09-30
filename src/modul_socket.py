import socket
port_liste = []
banner_liste = []
dosya = open("ip.txt", "r")
ipler = dosya.read()
dosya.close()
for ip in ipler.splitlines():
    print(ip)
    for port in range(1, 25):
        try:
            soket = socket.socket()
            soket.connect((str(ip), int(port)))
            banner = soket.recv(1024)
            banner_liste.append(str(banner))
            port_liste.append(str(port))
            soket.close()
            print(port)
            print(banner)
            if "SSH" in str(banner):
                print("Sistem Linux veya network cihazi olabilir")
                log2 = str(ip)+"\n"
                dosya = open("linux.txt", "a")
                dosya.write(log2)
                dosya.close()
        except:
            pass
print(port_liste)
print(banner_liste)
