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




## L2_03 - Proxy intre doua procese (Intre un Server si un Client)


rezultate proxy
 ```text
# Server:
Serverul asteapta proxy-ul...
# Proxy:
Proxy-ul asteapta clientul...
# Client:
Stabileste conexiunea
Clientul a trimis: Salut, Server!
# Proxy:
Proxy-ul a acceptat clientul: ('127.0.0.1', 50166) 
Proxy-ul a primit: Salut, Server C!
# Server:
Serverul a primit: Salut, Server C!
Serverul a trimis: Serverul confirma: Salut, Server C!
# Proxy:P roxy-ul a primit raspunsul: Serverul confirma: Salut, Server C!
Proxy-ul a trimis raspunsul clientului.
# Client:
Clientul a primit: Serverul confirma: Salut, Server C!
```
## Concluzii și observații – Comunicarea printr-un proxy TCP

### 1. Scopul experimentului

Scopul experimentului a fost înțelegerea modului în care un proxy intermediază comunicarea dintre un client și un server. Au fost utilizate trei programe Python: `client.py`, `proxy.py` și `server.py`, care comunică folosind socketuri TCP.

### 2. Desfășurarea comunicației

Procesul de comunicare s-a desfășurat în următoarea ordine:

1. **Serverul (`server.py`)** a deschis un socket TCP pe portul `5001` și a așteptat o conexiune de la proxy, folosind metodele `bind()`, `listen()` și `accept()`.
2. **Proxy-ul (`proxy.py`)** a deschis un socket de ascultare pe portul `5000` și a așteptat conexiunea clientului.
3. **Clientul (`client.py`)** s-a conectat la proxy prin metoda `connect()` și a transmis mesajul „Salut, Server C!” folosind `sendall()`.
4. Proxy-ul a recepționat mesajul cu `recv()`, apoi a inițiat o conexiune TCP separată către server, folosind `connect()` pe portul `5001`.
5. Serverul a recepționat mesajul, a generat răspunsul „Serverul confirma: Salut, Server C!” și l-a trimis înapoi proxy-ului.
6. Proxy-ul a recepționat răspunsul serverului și l-a retransmis clientului prin conexiunea TCP inițială.

### 3. Legătura cu teoria de la curs

Experimentul ilustrează utilizarea socketurilor la nivelul transport și rolul protocolului TCP în comunicarea dintre aplicații.

- **TCP (Transmission Control Protocol)** este un protocol orientat pe conexiune, care asigură livrarea fiabilă și ordonată a fluxului de octeți.
- **Adresa IP** identifică endpointul de rețea, iar **portul** identifică endpointul aplicației cu care se realizează comunicarea.
- Metoda `bind()` asociază socketul cu o adresă și un port local, `listen()` permite așteptarea conexiunilor, `accept()` acceptă o conexiune, iar `connect()` inițiază o conexiune către un server.
- Metodele `sendall()` și `recv()` sunt utilizate pentru transmiterea și recepția datelor prin TCP.

În acest experiment, proxy-ul utilizează două conexiuni TCP distincte: una între client și proxy și alta între proxy și server. Prin urmare, clientul nu comunică direct cu serverul final, ci transmite datele printr-un proces intermediar.

### 4. Observații asupra rezultatelor

În Command Prompt s-a observat că mesajul transmis de client a fost recepționat de proxy și apoi de server. Serverul a generat un răspuns, care a fost transmis în sens invers, prin proxy, până la client.

Adresa `127.0.0.1` reprezintă adresa de loopback, utilizată pentru comunicarea locală pe același calculator. Portul `50166`, afișat de proxy în adresa clientului, este un port-sursă temporar alocat de sistemul de operare, în timp ce porturile `5000` și `5001` sunt porturile configurate pentru proxy și server.

Rezultatul confirmă funcționarea mecanismului de intermediere: proxy-ul primește datele, le retransmite serverului și returnează răspunsul clientului. În acest fel, proxy-ul acționează ca un releu la nivelul aplicației.

### 5. Limitări

Exemplul transmite un singur mesaj text și un singur răspuns. Deși TCP asigură un flux fiabil de octeți, nu păstrează automat delimitarea mesajelor aplicației. Pentru transferul unor fișiere sau al unor volume mai mari de date ar fi necesare mecanisme suplimentare pentru delimitarea datelor, verificarea completitudinii transferului și tratarea erorilor.

**Concluzie:** Experimentul demonstrează principiul unui proxy TCP simplu și evidențiază diferența dintre comunicarea directă client–server și comunicarea realizată printr-un intermediar.
