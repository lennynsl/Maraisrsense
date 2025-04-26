import paho.mqtt.client as mqtt
import ssl
import time
from getmac import get_mac_address

class CommunicationCCS811: 
    def __init__(self, adresse_du_borker, port_connexion, topic_TVOC, topic_CO2, client_identification, mots_de_passe):
        self.adresse_du_borker = adresse_du_borker
        self.port_connexion = port_connexion
        self.topic_TVOC = topic_TVOC
        self.topic_CO2 = topic_CO2
        self.client_identification = client_identification
        self.mots_de_passe = mots_de_passe
        self.client = mqtt.Client(client_identification=self.client_identification)
        self.client.username_pw_set(username=self.client_identification, password=self.mots_de_passe)
        self.client.tls_set(cert_reqs=ssl.CERT_NONE)
        self.client.tls_insecure_set(True)
        self.client.connect(self.adresse_du_borker, self.port_connexion)
        self.client.loop_start()

    def mesures_à_envoyer(self, TVOC, CO2): 
        self.client.publish(self.topic_TVOC, TVOC, retain=True)
        self.client.publish(self.topic_CO2, CO2, retain=True)

    def obtenir_adresse_MAC():
        win_mac = get_mac_address(interface="wlan0")
        MAC_formatté = win_mac.replace(":", "")
        return MAC_formatté

if __name__ == "__main__" :
    
    adresse_du_borker = "mqtt.marais2025.btssn.ovh"
    port_connexion = 8883
    topic_TVOC = "/d2e09263c6cc/capteurTVOC/TVOC"
    topic_CO2 = "/d2e09263c6cc/capteurTVOC/CO2"
    client_identification = "root" 
    mots_de_passe = "hyrome49#" 

    capteur = CommunicationCCS811(adresse_du_borker, port_connexion, topic_TVOC, topic_CO2, client_identification, mots_de_passe)
    capteur.mesures_à_envoyer(500, 4) # Exemple de valeurs à envoyer
    time.sleep(0.5) # Attendre un peu pour s'assurer que les messages sont envoyés