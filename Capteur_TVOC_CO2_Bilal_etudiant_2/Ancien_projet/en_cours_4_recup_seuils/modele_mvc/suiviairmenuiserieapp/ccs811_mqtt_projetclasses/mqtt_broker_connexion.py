import paho.mqtt.client as mqtt

# ================== CONFIGURATION ==================
BROKER_ADDRESS = "mqtt.marais2025.btssn.ovh"  # Remplace par l'IP publique de ton VPS
BROKER_PORT = 8883         # 8883 pour SSL, sinon 1883 pour non sécurisé
USERNAME = "root"          # Ton utilisateur Mosquitto
PASSWORD = "hyrome49#"      # Ton mot de passe Mosquitto
TOPIC = "#"                # '#' pour s'abonner à tous les topics
USE_TLS = True             # True si tu utilises SSL/TLS sur port 8883, False sinon

# ================== CALLBACKS ==================
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(" Connecté au broker MQTT !")
        client.subscribe(TOPIC)
        print(f" Abonné au topic '{TOPIC}' (tous les topics)")
    else:
        print(f" Échec de connexion. Code de retour : {rc}")

def on_message(client, userdata, msg):
    print(f" Message reçu -> Topic : {msg.topic} | Payload : {msg.payload.decode()}")

# ================== CLIENT MQTT ==================
client = mqtt.Client()

# Authentification
client.username_pw_set(USERNAME, PASSWORD)

# Connexion sécurisée
if USE_TLS:
    client.tls_set()

# Assignation des callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connexion au broker
print(f"  Connexion à {BROKER_ADDRESS}:{BROKER_PORT}...")
client.connect(BROKER_ADDRESS, BROKER_PORT)

# Boucle infinie pour écouter les messages
client.loop_forever()