import paho.mqtt.client as mqtt
import json

BROKER = "mqtt.marais2025.btssn.ovh"
PORT = 8883
USERNAME = "root"
PASSWORD = "hyrome49#"


def on_connect(client, userdata, flags, rc):
    """
    Callback lors de la connexion au broker MQTT.
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
    Callback lors de la réception d'un message MQTT.
    """
    try:
        data = json.loads(msg.payload.decode())
        print(f"[{msg.topic}] Seuils reçus : {data}")
    except Exception as e:
        print(f"Erreur décodage message sur {msg.topic} : {e}")


def main():
    client = mqtt.Client()
    client.username_pw_set(USERNAME, PASSWORD)
    client.tls_set()
    client.tls_insecure_set(True)
    client.on_connect = on_connect
    client.on_message = on_message

    print("Connexion au broker...")
    client.connect(BROKER, PORT)
    client.loop_forever()


if __name__ == "__main__":
    main()
