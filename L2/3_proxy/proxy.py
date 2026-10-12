
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy:
    proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy.bind(("127.0.0.1", 5000))
    proxy.listen(1)

    print("Proxy-ul asteapta clientul...")

    client, addr = proxy.accept()

    with client:
        print("Proxy-ul a acceptat clientul:", addr)

        mesaj = client.recv(1024)
        print("Proxy-ul a primit:", mesaj.decode())

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.connect(("127.0.0.1", 5001))
            server.sendall(mesaj)

            raspuns = server.recv(1024)
            print("Proxy-ul a primit raspunsul:", raspuns.decode())

        client.sendall(raspuns)
        print("Proxy-ul a trimis raspunsul clientului.")
