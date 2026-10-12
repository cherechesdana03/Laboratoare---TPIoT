import threading
import time

from echoserver import serve_once
from echoclient import send_message


HOST = "127.0.0.1"
PORT = 5001

NEXT_HOST = "127.0.0.1"
NEXT_PORT = 5002


def on_message(message):
    print("\n[NODE 1] Mesajul a parcurs inelul!")
    print(f"[NODE 1] Mesaj final: {message.decode('utf-8')}")


def run_server():
    serve_once(HOST, PORT, on_message)


if __name__ == "__main__":
    server_thread = threading.Thread(
        target=run_server,
        daemon=True
    )
    server_thread.start()

    time.sleep(1)

    try:
        message = "Salut! Acesta este mesajul initial."
        print(f"[NODE 1] Trimit mesajul: {message}")

        response = send_message(
            NEXT_HOST,
            NEXT_PORT,
            message
        )

        print(f"[NODE 1] Confirmare de la Node 2: {response}")

    except Exception as e:
        print(f"[NODE 1] Eroare de comunicatie: {e}")

    server_thread.join()
