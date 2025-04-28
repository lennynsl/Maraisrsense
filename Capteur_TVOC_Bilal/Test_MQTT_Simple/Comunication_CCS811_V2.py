import paho.mqtt.client as mqtt
import ssl
import time
from getmac import get_mac_address

class CommunicationCCS811: 
    def __init__(self, adresse_du_borker, port_connexion, client_identification, mots_de_passe):
        self.adresse_du_borker = adresse_du_borker
        self.port_connexion = port_connexion
        self.client_identification = client_identification
        self.mots_de_passe = mots_de_passe
        self.adresse_MAC = self.obtenir_adresse_MAC()
        self.topic_base = f"/{self.adresse_MAC}/capteurTVOC"
        self.client = mqtt.Client(client_identification)
        self.client.username_pw_set(username=self.client_identification, password=self.mots_de_passe)
        self.client.tls_set(cert_reqs=ssl.CERT_NONE)
        self.client.tls_insecure_set(True)
        self.client.connect(self.adresse_du_borker, self.port_connexion)
        self.client.loop_start()

    def envoyer(self, capteur, valeur): 
        topic = f"{self.topic_base}/{capteur}"
        self.client.publish(topic, valeur, retain=True)

    def obtenir_adresse_MAC(self):
        win_mac = get_mac_address(interface="wlan0")
        return win_mac.replace(":", "")

if __name__ == "__main__" :
    adresse_du_borker = "mqtt.marais2025.btssn.ovh"
    port_connexion = 8883
    client_identification = "root" 
    mots_de_passe = "hyrome49#" 
    envoyer = CommunicationCCS811(adresse_du_borker, port_connexion, client_identification, mots_de_passe)
    
    envoyer.envoyer("CO2", 500)
    envoyer.envoyer("TVOC", 4)

    time.sleep(0.5)
