
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 5001))
    s.listen(1)

    print("Serverul asteapta proxy-ul...")

    conn, addr = s.accept()

    with conn:
        mesaj = conn.recv(1024).decode()
        print("Serverul a primit:", mesaj)

        raspuns = "Serverul confirma: " + mesaj
        conn.sendall(raspuns.encode())

        print("Serverul a trimis:", raspuns)
