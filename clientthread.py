# La connexion au serveur s'établie au début du programme
# Les échanges de données se font ensuite entre les clients connectés au serveur
# Le serveur doit être exécuté sur une machine accessible par les clients
# et les clients doivent spécifier l'adresse IP et le port du serveur pour se connecter


import socket  # operation reseaux
import threading  # operation pour utiliser des threads
import re  # regular expressions, extractions d'infos (username)
import time  # operation lié au temps

# class heritant de threading.thread, pour gérer la communication avec un client côté serveur


class ClientListener(threading.Thread):

    def __init__(self, server, soc, address):
        super(ClientListener, self).__init__()
        self.server = server  # pour communiquer avec serveur
        self.socket = soc   # socket associé au client
        self.address = address  # adresse du client
        self.listening = True  # pour savoir si le thread doit continuer à écouter msg du client
        self.username = "No username"  # initialise le nom d'utilisateur à "No username"

    def run(self):
        # la methode fonctionne dès que le thread est démaré et ecoute en boucle les données
        # provenant du client via le socket
        while self.listening:
            data = ""
            try:
                data = self.socket.recv(4096).decode('UTF-8')
            except socket.error:
                print("Unable to receive data")
            self.handle_msg(data)  # pour traiter les données une fois reçu
            time.sleep(0.1)  # avec une pause de 0.1 seconde
        print("Ending client thread for", self.address)

    def quit(self):  # client se deco avec étape
        self.listening = False
        self.socket.close()
        self.server.remove_socket(self.socket)
        self.server.echo("{0} has quit\n".format(self.username))

    # traite message reçu, exemple : "username a rejoint" / "a quitté" / "chaine vide"
    # sinon echo relaye au serveur pour que tous les clients voient
    def handle_msg(self, data):
        print(self.address, "sent :", data)
        username_result = re.search('^USERNAME (.*)$', data)
        if username_result:
            self.username = username_result.group(1)
            self.server.echo("{0} has joined.\n".format(self.username))
        elif data == "QUIT":
            self.quit()
        elif data == "":
            self.quit()
        else:
            self.server.echo(data)
