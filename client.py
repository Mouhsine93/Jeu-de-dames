# Ce code est conçu pour une communication client-serveur asynchrone,
# où le client (programme) peut envoyer et recevoir des messages avec le serveur tout
# en continuant à effectuer d'autres opérations grâce à l'utilisation de threads
import json
import threading  # operation pour utiliser des threads
import socket  # operation reseaux
import time  # operation lié au temps
import re  # extraction d'infos (username)


class Client:
    def __init__(self, username, server, port, on_listen: callable):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server, port))  # se connecter au serveur
        self.username = username
        self.send("USERNAME {0}".format(username))  # envoie du nom au serveur
        self.listening = True
        self.on_listen = on_listen

    def listener(self):

        while self.listening:  # crée une boucle pour recevoir données du serveur
            data = ""
            try:
                data = self.socket.recv(4096).decode('UTF-8')
            except socket.error:
                print("Unable to receive data")
            print("data received")
            if data[0] == "{":
                ddata = json.loads(data)
                if self.username != ddata['playername']:
                    self.on_listen(ddata)
                else:
                    print("data blocked")
            time.sleep(0.1)

    def listen(self):
        # crée un thread pour ecouter messages du serveur en async
        self.listen_thread = threading.Thread(target=self.listener)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    def send(self, message):  # envoi message aux serveurs, nom d'utilisateur et ajuste format message
        try:
            username_result = re.search('^USERNAME (.*)$', message)
            if not username_result:
                message = "{1}".format(self.username, message)
            self.socket.sendall(message.encode("UTF-8"))
        except socket.error:
            print("unable to send message")

    def tidy_up(self):  # stop co serveur
        self.listening = False
        self.socket.close()

    def handle_msg(self, data):  # traite les messages reçus
        if data == "QUIT":
            self.tidy_up()
        elif data == "":
            self.tidy_up()
        elif data[0] == "{":
            x = json.loads(data)
            if x['playername'] != self.username:
                return x
