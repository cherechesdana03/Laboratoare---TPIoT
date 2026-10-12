import socket


def serve_once(HOST, PORT, on_message=None):
    """Accepta o conexiune TCP, confirma mesajul si il proceseaza."""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)

        print(f"[SERVER] Asculta pe {HOST}:{PORT}")

        conn, addr = s.accept()

        with conn:
            print(f"[SERVER] Conexiune de la {addr}")

            data = conn.recv(1024)

            if data:
                print(f"[SERVER] Mesaj primit: {data.decode()}")

                # Comportamentul de ecou din fisierul original
                conn.sendall(data)

                if on_message is not None:
                    on_message(data)
