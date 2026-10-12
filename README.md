# Proiect L1 - Transmitere mesaj într-un inel de 3 procese (TCP/UDP)

Acest repository conține rezolvarea task-ului de transmitere a unui mesaj în inel folosind socket-uri.

## Rezultatele execuției (Console Output)

**Terminal Node 2 (Pornit primul, ascultă mesajul):**
```text
[SERVER] Asculta pe 127.0.0.1:5002
[SERVER] Conexiune de la ('127.0.0.1', 55585)
[SERVER] Mesaj primit: Salut! Acesta este mesajul initial.
[NODE 2] Retransmit mesajul: Salut! Acesta este mesajul initial. -> Node 2
[CLIENT] Raspuns de la 127.0.0.1:5003: Salut! Acesta este mesajul initial. -> Node 2
```

**Terminal Node 3 (Pornit al doilea, ascultă mesajul):**
```text
[SERVER] Asculta pe 127.0.0.1:5003
[SERVER] Conexiune de la ('127.0.0.1', 55586)
[SERVER] Mesaj primit: Salut! Acesta este mesajul initial. -> Node 2
[NODE 3] Retransmit mesajul: Salut! Acesta este mesajul initial. -> Node 2 -> Node 3
[CLIENT] Raspuns de la 127.0.0.1:5001: Salut! Acesta este mesajul initial. -> Node 2 -> Node 3
```
**Terminal Node 1 (Pornit ultimul, este initiatorul mesajul):**
```text
[SERVER] Asculta pe 127.0.0.1:5001
[NODE 1] Trimit mesajul: Salut! Acesta este mesajul initial.
[CLIENT] Raspuns de la 127.0.0.1:5002: Salut! Acesta este mesajul initial.
[NODE 1] Confirmare de la Node 2: Salut! Acesta este mesajul initial.
[SERVER] Conexiune de la ('127.0.0.1', 55587)
[SERVER] Mesaj primit: Salut! Acesta este mesajul initial. -> Node 2 -> Node 3
[NODE 1] Mesajul a parcurs inelul!
[NODE 1] Mesaj final: Salut! Acesta este mesajul initial. -> Node 2 -> Node 3
```

# Analizaa conexiunilor si porturilor (cu comanda netstat)

## Am verificat starea porturilor 

**Pentru Node 1 (portul :5001)**
 ```text
 Comanda: netstat -ano | findstr ":5001"
 Observații: Folosit procesul cu PID 6576. 0.0.0.0 este adresa IPv4 nespecificată.
```
**Pentru Node 2 (Port :5002):**
 ```text
Comanda: netstat -ano | findstr ":5002"

Observații: Serverul TCP este în starea LISTENING, așteptând conexiuni de la client. 127.0.0.1 este adresa de localhost. PID-ul procesului este 12188.
```
**Pentru Node 3 (Port :5003):**
 ```text
Comanda: netstat -ano | findstr ":5003"

Observații: Server TCP în starea LISTENING. PID-ul asociat este 4708.
```
