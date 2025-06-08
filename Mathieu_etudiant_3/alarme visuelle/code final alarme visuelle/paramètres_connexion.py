import paho.mqtt.client as mqtt
import ssl
# Classe pour la connexion au broker MQTT
class MQTTClient:
    def __init__(self, broker, port, username, password):
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port

        # Authentification
        self.client.username_pw_set(username, password)

        # Connexion TLS
        self.client.tls_set(cert_reqs=ssl.CERT_NONE)
        self.client.tls_insecure_set(True)

    def connect(self):
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            print("Connexion au broker MQTT réussie.")
        except Exception as rc:
            print(f"Erreur de connexion au broker : {rc}")
            exit(1)

    def publish(self, topic, payload):
        self.client.publish(topic, payload)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("Déconnecté du broker MQTT.")
