import socket
import struct

def udp_server():
    server_ip = '127.0.0.1' # adresa destinatiei
    server_port = 15001 # portul UDP la care serverul asteapta date

    END = 0xFFFFFFFF
    fisier_primit = 'fisier_primit.bin'
    dimensiune_pachet = 1024

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((server_ip, server_port))
        # "bind" = procesul SERVER solicita sistemului de operare sa asocieze socket-ul de adresa
        # locala si portul respectiv definite prin "server_ip" si "server_port"

        print(
            f"Serverul UDP este pornit și ascultă "
            f"pe {server_ip}:{server_port}..."
        )

        asteptat = 0
        f = None

        while True:
            data, addr = s.recvfrom(dimensiune_pachet + 4)

            # Primele 4 octeți conțin numărul secvenței
            secventa = struct.unpack('!I', data[:4])[0]
            continut = data[4:]

            if secventa == END:
                # Confirmăm sfârșitul transferului
                s.sendto(struct.pack('!I', END), addr)

                if f is not None:
                    f.close()
                    f = None

                print("Transferul fișierului s-a încheiat.")
                print(f"Fișier salvat: {fisier_primit}")

                break

            # Scriem fiecare pachet o singură dată,
            # în ordinea corectă
            if secventa == asteptat:
                if f is None:
                    f = open(fisier_primit, 'wb')

                f.write(continut)
                print(
                    f"Am primit pachetul {secventa}, "
                    f"{len(continut)} octeți."
                )
                asteptat += 1

            # Confirmăm pachetul deja primit.
            # Dacă a fost retransmis, nu îl scriem din nou.
            if secventa < asteptat:
                s.sendto(struct.pack('!I', secventa), addr)
                ## "sendto" = clientul trimite prin aceasta instructiune datagrama catre destinatia
                # indicata (aici este identica cu sursa)

            # Pachetele sosite în afara ordinii nu sunt
            # confirmate; clientul le va retransmite.

        if f is not None:
            f.close()

if __name__ == "__main__":
    udp_server()
