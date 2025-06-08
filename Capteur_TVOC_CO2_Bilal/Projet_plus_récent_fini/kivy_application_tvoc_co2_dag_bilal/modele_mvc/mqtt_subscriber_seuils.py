"""
mqtt_subscriber_seuils.py
-------------------------
Script utilitaire pour s'abonner aux topics MQTT des seuils CO2 et TVOC.
Affiche en temps réel les seuils reçus depuis le broker MQTT.
Utilisé pour le diagnostic et la vérification de la réception des seuils dynamiques.

Ce script est destiné à la surveillance et au diagnostic des seuils reçus via MQTT.
Il n'est pas utilisé dans l'application principale.

Sécurité : La connexion utilise TLS (SSL) pour sécuriser les échanges avec le broker MQTT. Le paramètre `tls_insecure_set(True)` désactive la vérification stricte du certificat, ce qui est adapté à un usage pédagogique ou en environnement contrôlé, mais déconseillé en production.
"""

import paho.mqtt.client as mqtt
import json

BROKER = "mqtt.marais2025.btssn.ovh"
PORT = 8883
USERNAME = "root"
PASSWORD = "hyrome49#"

def on_connect(client, userdata, flags, rc):
    """
    Callback appelé lors de la connexion au broker MQTT.
    Souscrit aux topics des seuils CO2 et TVOC si la connexion est réussie.

    :param client: Le client MQTT
    :param userdata: Données utilisateur fournies lors de la création du client
    :param flags: Drapeaux de connexion
    :param rc: Code de retour de la connexion
    """
    if rc == 0:
        print("Connecté au broker MQTT.")
        client.subscribe("seuil/CO2")
        client.subscribe("seuil/TVOC")
        print("Abonné à seuil/CO2 et seuil/TVOC.")
    else:
        print(f"Échec de connexion : code {rc}")

def on_message(client, userdata, msg):
    """
    Callback appelé à la réception d'un message sur les topics abonnés.
    Décode et affiche le contenu JSON des seuils reçus.

    :param client: Le client MQTT
    :param userdata: Données utilisateur fournies lors de la création du client
    :param msg: Message reçu
    """
    try:
        data = json.loads(msg.payload.decode())
        print(f"[{msg.topic}] Seuils reçus : {data}")
    except Exception as e:
        print(f"Erreur décodage message sur {msg.topic} : {e}")

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set()
client.tls_insecure_set(True)
client.on_connect = on_connect
client.on_message = on_message

# if __name__ == "__main__":
#     print("Connexion au broker MQTT pour surveillance des seuils...")
#     try:
#         client.connect(BROKER, PORT)
#         client.loop_forever()
#     except Exception as e:
#         print(f"Erreur lors de la connexion ou de l'écoute MQTT : {e}")
