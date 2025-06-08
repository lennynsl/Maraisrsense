# ==========================================================
# communication_mqtt_ccs811.py
# Version : 1.1.0 (Ajout du support des topics MQTT dynamiques selon le capteur)
# Module pour la communication MQTT des mesures capteurs
# S'adapte au type de capteur (CCS811 ou SDS011)
# ==========================================================

import warnings  # Pour ignorer certains avertissements
import paho.mqtt.client as mqtt  # Client MQTT
import ssl       # Pour la connexion sécurisée
from getmac import get_mac_address  # Pour obtenir l'adresse MAC

class CommunicationCCS811:
    """
    Classe pour gérer la communication MQTT des mesures capteurs.
    Le topic s'adapte dynamiquement selon le type de capteur.
    """
    def __init__(self, adresse_du_borker, port_connexion, client_identification, mots_de_passe):
        """
        Initialise la connexion au broker MQTT et définit le client.
        
        :param adresse_du_borker: Adresse du broker MQTT
        :param port_connexion: Port de connexion au broker
        :param client_identification: Identifiant du client MQTT
        :param mots_de_passe: Mot de passe pour l'authentification
        """
        self.adresse_du_borker = adresse_du_borker
        self.port_connexion = port_connexion
        self.client_identification = client_identification
        self.mots_de_passe = mots_de_passe
        self.adresse_MAC = self.obtenir_adresse_MAC()
        # self.topic_base = f"{self.adresse_MAC}/
        self.topic_base = self.adresse_MAC
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            self.client = mqtt.Client(client_id=client_identification, protocol=mqtt.MQTTv311)
        self.client.username_pw_set(username=self.client_identification, password=self.mots_de_passe)
        self.client.tls_set(cert_reqs=ssl.CERT_NONE)
        self.client.tls_insecure_set(True)
        self.client.connect(self.adresse_du_borker, self.port_connexion)
        self.client.loop_start()

    def envoyer(self, mesure, valeur, unite=None):
        """
        Publie la mesure sur le topic MQTT au format adresse_mac/mesure/unite/valeur.
        
        :param mesure: Nom de la mesure (ex: co2, tvoc, pm25, pm10)
        :param valeur: Valeur de la mesure
        :param unite: Unité de la mesure (ex: ppm, ppb, ugm3)
        """
        if unite is None:
            # Déduction automatique de l'unité selon la mesure
            if mesure.lower() == "co2":
                unite = "ppm"
            elif mesure.lower() == "tvoc":
                unite = "ppb"
            elif mesure.lower() in ["pm25", "pm10"]:
                unite = "ugm3"
            else:
                unite = "valeur"
        topic = f"{self.topic_base}/{mesure.lower()}/{unite}/{valeur}"
        self.client.publish(topic, valeur, retain=True)

    def obtenir_adresse_MAC(self):
        """
        Retourne l'adresse MAC de la machine (format sans ':').
        """
        win_mac = get_mac_address(interface="wlan0")
        return win_mac.replace(":", "")

if __name__ == "__main__" :
    """
    Exemple d'utilisation de la classe CommunicationCCS811.
    """
    adresse_du_borker = "mqtt.marais2025.btssn.ovh"
    port_connexion = 8883
    client_identification = "root" 
    mots_de_passe = "hyrome49#" 
    envoyer = CommunicationCCS811(adresse_du_borker, port_connexion, client_identification, mots_de_passe)
    
    envoyer.envoyer("co2", 500)
    envoyer.envoyer("tvoc", 4)
