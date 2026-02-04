# # Le serveur doit être conçu pour gérer les connexions et coordonner les échanges de données
# entre les clients.

# Ce code représente un serveur qui écoute les connexions entrantes sur un port spécifié,
# gère chaque client dans un thread distinct (ClientListener)
# et peut envoyer des messages à tous les clients connectés
# Le serveur peut être interrompu proprement en recevant les signaux d'interruption (Ctrl+C)
# ou de terminaison

import socket  # operation reseaux
import signal  # identifie les signaux (d'interruption)
import sys  # utilisé pour sortir du programme
import time  # operation lié au temps
import json
from clientthread import ClientListener


class Server():
 # crée un socket d'écoute, lié à une adresse ip vide, un port et accepte jusqu'à une co en attente
    def __init__(self, port):

        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(('', port))
        self.listener.listen(1)
        print("Listening on port", port)
        self.clients_sockets = []
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    # signal d'interruption pour que le serveur ferme le socket d'écoute et envoi message "quit"
    # aux clients co
    def signal_handler(self, signal, frame):
        self.listener.close()
        self.echo("QUIT")

    def run(self):  # boucle infinie pour clients et gerer la communication avec client
        while True:
            print("listening new customers")
            try:
                (client_socket, client_adress) = self.listener.accept()
            except socket.error:
                sys.exit("Cannot connect clients")
            self.clients_sockets.append(client_socket)
            print("Start the thread for client:", client_adress)
            client_thread = ClientListener(self, client_socket, client_adress)
            client_thread.start()
            time.sleep(0.1)

    def remove_socket(self, socket):  # retirer sockets de liste client actifs
        self.clients_sockets.remove(socket)

    def echo(self, data):  # prend message pour envoyer aux clients actifs
        print("echoing:", data)
        for sock in self.clients_sockets:
            try:
                sock.sendall(data.encode("UTF-8"))
            except socket.error:
                print("Cannot send the message")


if __name__ == "__main__":  # instance de la classe server est crée avec port puis demarre serveur
    server = Server(8080)
    server.run()
