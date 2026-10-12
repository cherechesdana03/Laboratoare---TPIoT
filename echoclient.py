import socket


def send_message(HOST, PORT, message):
    """Trimite un mesaj unui server TCP si returneaza ecoul."""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message.encode("utf-8"))

        data = s.recv(1024)

    response = data.decode("utf-8")
    print(f"[CLIENT] Raspuns de la {HOST}:{PORT}: {response}")

    return response
