
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 5000))

    mesaj = "Salut, Server C!"
    s.sendall(mesaj.encode())

    print("Clientul a trimis:", mesaj)

    raspuns = s.recv(1024).decode()
    print("Clientul a primit:", raspuns)
