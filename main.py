import socket
import http.client
import re

# http://10.10.202.98:3010/
host = "10.10.202.98"
port = 3010
path = "/"
number = 0

#AD_INET è la famiglia di indirizzi ip utilizzabili, in questo caso IPv4. SOCK_STREAM significa TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        #(host,port) è una tupla, e' un singolo argomento per connect
        s.connect((host, port))

        """"
        faccio una formatted string, la richiesta è una GET al path / utilizzando il protocollo HTTP 1.1, 
        poi creo un header con un host pari all'hos che ho definito e lascio 2 righe vuote come terminazione 
        dell'header
        """
        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
        #non posso mandare la stringa formattata ma devo mandare i bytes
        s.sendall(request.encode())

        #creo una response che e' una byte string vuota
        response = b""

        while True:
            data = s.recv(4096)
            if not data:
                break
            response = response + data

        print(response)

        #r e' una stringa grezza cioe' non interpreta i caratteri di escape come /n
        #.*? significa zero o più caratteri possibili (.*) prendendo il numero minore possibile di caratteri (?)
        #(\d+) cerco uno o piu' caratteri numerici e li metto in un gruppo

        print("\n\n1")
        pattern = r"<h3>Its currenly on port <u><a.*?>(\d+)</a>"

        print("\n\n2")
        match = re.search(pattern, response.decode())

        print(match)
        if match:
            newPort = match.group(1)
            print("Nuova porta: " + newPort)
        else:
            print("Porta non trovata")

    except Exception as e:
        print(e)
      ####