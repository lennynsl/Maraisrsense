import paho.mqtt.client as mqtt
import ssl
import time
from getmac import get_mac_address


class CommunicationCCS811:
    """
    Classe pour gérer la communication MQTT avec le capteur CCS811.
    """

    def __init__(self, broker_address, port, client_id, password):
        self.broker_address = broker_address
        self.port = port
        self.client_id = client_id
        self.password = password
        self.mac_address = self.get_mac_address()
        self.topic_base = f"/{self.mac_address}/"
        self.client = mqtt.Client(client_id)
        self.client.username_pw_set(username=self.client_id, password=self.password)
        self.client.tls_set(cert_reqs=ssl.CERT_NONE)
        self.client.tls_insecure_set(True)
        self.client.connect(self.broker_address, self.port)
        self.client.loop_start()

    def envoyer(self, capteur, valeur):
        topic = f"{self.topic_base}{capteur}"
        self.client.publish(topic, valeur, retain=True)

    def get_mac_address(self):
        mac = get_mac_address(interface="wlan0")
        return mac.replace(":", "")


if __name__ == "__main__":
    broker_address = "mqtt.marais2025.btssn.ovh"
    port = 8883
    client_id = "root"
    password = "hyrome49#"
    communication = CommunicationCCS811(broker_address, port, client_id, password)
    communication.envoyer("CO2", 500)
    communication.envoyer("TVOC", 4)
    time.sleep(0.5)
