import paho.mqtt.client as mqtt
#classe pour la connexion au broker MQTT
class MQTTClient:
    def __init__(self, broker, port):
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port

    def connect(self):
        self.client.connect(self.broker, self.port, 60)

    def publish(self, topic, payload):
        self.client.publish(topic, payload)

    def disconnect(self):
        self.client.disconnect()

#choisir le message à envoyer
def choose_message(key):
    if key == "on":
        return "on"
    elif key == "off":
        return "off"
    elif key == "toggle":
        return "toggle"
    else:
        return None

#paramètres de connexion au broker MQTT
mqtt_client = MQTTClient(broker="mqtt.marais2025.btssn.ovh", port=8883)
mqtt_client.connect()

while True:
    key = input("Entrez une commande (on, off, toggle): ")
    
    # Choisir le message à envoyer
    message = choose_message(key)
    
    if message:
        # Publier le message sur le topic unique
        mqtt_client.publish("shellyplus1-80646fdb37f8/command/switch:0", message)
        print(f"Message envoyé: {message}")
    else:
        print("Clé invalide. Veuillez entrer une commande valide.")

mqtt_client.disconnect()