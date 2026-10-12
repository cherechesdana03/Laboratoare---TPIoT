from echoserver import serve_once
from echoclient import send_message


HOST = "127.0.0.1"
PORT = 5002

NEXT_HOST = "127.0.0.1"
NEXT_PORT = 5003


def forward_message(message):
    text = message.decode("utf-8")
    forwarded = text + " -> Node 2"

    print(f"[NODE 2] Retransmit mesajul: {forwarded}")

    send_message(NEXT_HOST, NEXT_PORT, forwarded)


if __name__ == "__main__":
    serve_once(HOST, PORT, forward_message)
