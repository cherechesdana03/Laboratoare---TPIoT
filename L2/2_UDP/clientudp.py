import socket # va fi alocat pentru handling sockets
import struct
import os

def udp_client():
    server_ip = '127.0.0.1'
    server_port = 15001

    # Fișierul care trebuie trimis
    fisier = 'fisier_dummy.txt'

    # Dimensiunea unei bucăți de date
    dimensiune_pachet = 1024

    # Valoare specială care marchează sfârșitul fișierului
    END = 0xFFFFFFFF

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s: # crearea socket-ului
    #pentru procesul CLIENT
    # AF_INET selecteaza IPv4
    # SOCK_DGRAM selecteaza protocolul de trsnaport UDP
        s.settimeout(1.0)

        try:
            with open(fisier, 'rb') as f:
                secventa = 0

                while True:
                    date = f.read(dimensiune_pachet)

                    # Dacă nu mai există date, terminăm transferul
                    if not date:
                        break

                    # Numărul secvenței este transmis pe 4 octeți
                    pachet = struct.pack('!I', secventa) + date

                    # Retransmitem dacă nu primim confirmarea
                    for incercare in range(5):
                        s.sendto(pachet, (server_ip, server_port))

                        try:
                            raspuns, _ = s.recvfrom(1024)
                            confirmare = struct.unpack('!I', raspuns[:4])[0]

                            if confirmare == secventa:
                                break

                        except socket.timeout:
                            print(
                                f"Timeout pentru pachetul {secventa}. "
                                f"Reîncercarea {incercare + 1}/5"
                            )
                    else:
                        print("Transfer întrerupt: serverul nu confirmă pachetul.")
                        return

                    print(f"Pachetul {secventa} a fost transmis.")
                    secventa += 1

                # Trimitem marcajul de sfârșit
                pachet_final = struct.pack('!I', END)

                for incercare in range(5):
                    s.sendto(pachet_final, (server_ip, server_port))

                    try:
                        raspuns, _ = s.recvfrom(1024)
                        confirmare = struct.unpack('!I', raspuns[:4])[0]

                        if confirmare == END:
                            print("Fișierul a fost transferat cu succes!")
                            break

                    except socket.timeout:
                        print("Se retransmite marcajul de sfârșit...")
                else:
                    print("Serverul nu a confirmat terminarea transferului.")

        except FileNotFoundError:
            print(f"Fișierul '{fisier}' nu a fost găsit.")

if __name__ == "__main__":
    udp_client()
