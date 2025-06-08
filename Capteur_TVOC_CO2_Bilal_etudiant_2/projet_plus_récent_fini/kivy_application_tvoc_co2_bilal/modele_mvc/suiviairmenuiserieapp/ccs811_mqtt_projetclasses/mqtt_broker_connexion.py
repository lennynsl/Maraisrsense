"""
mqtt_broker_connexion.py
------------------------
Script utilitaire pour se connecter à un broker MQTT et afficher tous les messages reçus.
Permet de diagnostiquer la communication MQTT et de vérifier la réception des topics.

Ce script est utile pour surveiller en temps réel tous les messages transitant sur le broker MQTT.
Il n'est pas utilisé dans l'application principale.

Remarque : Le topic '#' permet de s'abonner à tous les topics du broker, ce qui est pratique pour le diagnostic mais à éviter en production pour des raisons de sécurité et de performance.
"""

import paho.mqtt.client as mqtt

# ================== CONFIGURATION ==================
BROKER_ADDRESS = "mqtt.marais2025.btssn.ovh"  # Adresse du broker MQTT
BROKER_PORT = 8883         # 8883 pour SSL, sinon 1883 pour non sécurisé
USERNAME = "root"          # Utilisateur Mosquitto
PASSWORD = "hyrome49#"      # Mot de passe Mosquitto
TOPIC = "#"                # '#' pour s'abonner à tous les topics
USE_TLS = True             # True si SSL/TLS sur port 8883

def on_connect(client, userdata, flags, rc):
    """
    Callback lors de la connexion au broker.
    S'abonne à tous les topics si la connexion est réussie.
    """
    if rc == 0:
        print(" Connecté au broker MQTT !")
        client.subscribe(TOPIC)
        print(f" Abonné au topic '{TOPIC}' (tous les topics)")
    else:
        print(f" Échec de connexion. Code de retour : {rc}")

def on_message(client, userdata, msg):
    """
    Callback lors de la réception d'un message.
    Affiche le topic et le contenu du message.
    """
    print(f" Message reçu -> Topic : {msg.topic} | Payload : {msg.payload.decode()}")

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)

if USE_TLS:
    client.tls_set()

client.on_connect = on_connect
client.on_message = on_message

print(f"  Connexion à {BROKER_ADDRESS}:{BROKER_PORT}...")
client.connect(BROKER_ADDRESS, BROKER_PORT)

client.loop_forever()