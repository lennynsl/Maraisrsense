# ==========================================================
# communication_mqtt_ccs811.py
# Version : 1.1.0 (Ajout du support des topics MQTT dynamiques selon le capteur)
# Module pour la communication MQTT des mesures capteurs
# S'adapte au type de capteur (CCS811)
# ==========================================================
"""
Module : communication_mqtt_ccs811.py

Ce module fournit une classe pour envoyer les mesures du capteur CCS811 sur un broker MQTT.
Les topics sont structurés comme suit : <adresse_mac>/<mesure>/<unite>/<valeur>
Exemple : 112233445566/co2/ppm/500

Structure des topics MQTT :
    - Chaque mesure est publiée sur un topic unique, incluant l'adresse MAC de l'appareil pour l'identification.
    - Le paramètre `retain=True` permet de conserver la dernière valeur sur le broker.

Robustesse :
    - Les erreurs de connexion ou d'envoi sont journalisées, mais n'interrompent pas l'application principale.

Sécurité :
    - La connexion utilise TLS (SSL) pour sécuriser les échanges avec le broker MQTT. Le paramètre `tls_insecure_set(True)` désactive la vérification stricte du certificat, ce qui est adapté à un usage pédagogique ou en environnement contrôlé, mais déconseillé en production.

Utilisation typique :
    mqtt = CommunicationCCS811(adresse_broker, port, identifiant, mot_de_passe)
    mqtt.envoyer("co2", 500, "ppm")
"""

import warnings
import paho.mqtt.client as mqtt
import ssl
from getmac import get_mac_address
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

class CommunicationCCS811:
    """
    Classe pour gérer la communication MQTT des mesures capteurs CCS811.
    Permet d'envoyer les mesures sur le broker MQTT.
    Les topics sont structurés comme suit :
        <adresse_mac>/<mesure>/<unite>/<valeur>
    Exemple : 112233445566/co2/ppm/500
    """

    def __init__(self, adresse_broker, port_connexion, identifiant_client, mot_de_passe):
        """
        Initialise la connexion au broker MQTT et définit le client.
        :param adresse_broker: Adresse du broker MQTT
        :param port_connexion: Port de connexion au broker
        :param identifiant_client: Identifiant du client MQTT
        :param mot_de_passe: Mot de passe pour l'authentification
        """
        try:
            self.adresse_broker = adresse_broker
            self.port_connexion = port_connexion
            self.identifiant_client = identifiant_client
            self.mot_de_passe = mot_de_passe
            self.adresse_mac = self.obtenir_adresse_mac()
            self.topic_base = self.adresse_mac
            self.client = mqtt.Client(client_id=identifiant_client, protocol=mqtt.MQTTv311)
            self.client.username_pw_set(username=self.identifiant_client, password=self.mot_de_passe)
            self.client.tls_set(cert_reqs=ssl.CERT_NONE)
            self.client.tls_insecure_set(True)
            self.client.connect(self.adresse_broker, self.port_connexion)
            self.client.loop_start()
            logger.info("Connexion MQTT établie avec succès.")
        except Exception as exception:
            logger.error(f"Erreur lors de l'initialisation de CommunicationCCS811 : {exception}")

    def _journaliser_erreur(self, message, exception):
        """
        Journalise une erreur MQTT.
        :param message: Message d'erreur
        :param exception: Exception associée
        """
        logger.error(f"{message} : {exception}")

    def _publier(self, topic, valeur):
        """
        Publie une valeur sur un topic MQTT.
        :param topic: Nom du topic
        :param valeur: Valeur à publier
        """
        try:
            self.client.publish(topic, valeur, retain=True)
            logger.info(f"Mesure envoyée sur le topic {topic} : {valeur}")
        except Exception as exception:
            self._journaliser_erreur(f"Erreur lors de l'envoi MQTT sur {topic}", exception)

    def envoyer(self, mesure, valeur, unite=None):
        """
        Publie la mesure sur le topic MQTT au format adresse_mac/mesure/unite/valeur.
        :param mesure: Nom de la mesure (ex: co2, tvoc)
        :param valeur: Valeur de la mesure
        :param unite: Unité de la mesure (ex: ppm, ppb)
        Si l'unité n'est pas précisée, elle est déduite automatiquement selon la mesure.
        """
        try:
            if unite is None:
                # Déduction automatique de l'unité selon la mesure
                if mesure.lower() == "co2":
                    unite = "ppm"
                elif mesure.lower() == "tvoc":
                    unite = "ppb"
                else:
                    unite = "valeur"
            topic = f"{self.topic_base}/{mesure.lower()}/{unite}/{valeur}"
            self.client.publish(topic, valeur, retain=True)
            logger.info(f"Mesure envoyée sur le topic {topic} : {valeur} {unite}")
        except Exception as exception:
            logger.error(f"Erreur lors de l'envoi MQTT sur {topic} : {exception}")

    def obtenir_adresse_mac(self):
        """
        Retourne l'adresse MAC de la machine (format sans ':').
        :return: str adresse MAC
        """
        try:
            win_mac = get_mac_address(interface="wlan0")
            return win_mac.replace(":", "")
        except Exception as exception:
            logger.error(f"Erreur lors de la récupération de l'adresse MAC : {exception}")
            return "indisponible"