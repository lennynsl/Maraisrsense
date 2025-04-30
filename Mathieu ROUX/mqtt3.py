import paho.mqtt.client as mqtt
import ssl
import uuid
import time

class CommunicationPM: 
    def __init__(self, broker_address, port, topic1, topic2, client_id, password):
        self.broker_address = broker_address
        self.port = port
        self.topic1 = topic1
        self.topic2 = topic2
        self.client_id = client_id
        self.password = password

        self.client = mqtt.Client(client_id=self.client_id)
        self.client.username_pw_set(username=self.client_id, password=self.password)

        # 🔐 Désactiver la vérification SSL
        self.client.tls_set(cert_reqs=ssl.CERT_NONE)
        self.client.tls_insecure_set(True)

        self.client.connect(self.broker_address, self.port)
        self.client.loop_start()

    def envoyer_mesures(self, pm25, pm10): 
        self.client.publish(self.topic1, pm25, retain=True)
        self.client.publish(self.topic2, pm10, retain=True)

    def get_mac_address():
        mac = uuid.getnode()
        mac_formatted = ':'.join(f'{(mac >> ele) & 0xff:02x}' for ele in range(40, -1, -8))
        return mac_formatted

if __name__ == "__main__" :
    broker_address = "mqtt.marais2025.btssn.ovh"
    port = 8883
    topic1 = "/adressemac/capteurpm/pm25"
    topic2 = "/adressemac/capteurpm/pm10"
    client_id = "root"
    password = "hyrome49#"

    capteur = CommunicationPM(broker_address, port, topic1, topic2, client_id, password)
    capteur.envoyer_mesures(8, 4)
    time.sleep(2)  # pour laisser le temps d’envoyer avant que le script se termine