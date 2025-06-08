# ==========================================================
# modele_accueil.py
# Version : 1.5.0 (Respect des exigences industrielles, gestion des seuils, robustesse, conformité MVC)
# Modèle principal pour la gestion des données capteurs (CCS811)
# ==========================================================
"""
Module : modele_accueil.py

Ce module définit le modèle principal de l'application pour la gestion des mesures du capteur CCS811,
la communication MQTT, la gestion dynamique des seuils et la robustesse de la collecte de données.
Il assure la conformité industrielle et la traçabilité des mesures.

Robustesse :
    - Toutes les opérations critiques (lecture capteur, envoi MQTT, réception seuils) sont protégées par des blocs try/except.
    - Les erreurs sont journalisées et n'interrompent pas l'application.

Conformité industrielle :
    - Les seuils par défaut sont conformes aux recommandations pour la sécurité en atelier.
    - Les moyennes sont calculées pour assurer la traçabilité des mesures.

Utilisation :
    modele = ModeleAccueil()
    modele.lire_donnees_capteur()
    co2, tvoc = modele.get_co2_tvoc()
"""

# Importations standards et modules internes
import datetime  # Pour la gestion des dates et heures
import json  # Pour décoder le message MQTT des seuils
import threading  # Pour lancer le client MQTT secondaire en thread
import warnings  # Pour la gestion des avertissements
import logging  # Pour le suivi des événements

from suiviairmenuiserieapp.ccs811_mqtt_projetclasses.gestion_tvoc_co2 import GestionTVOC_CO2  # Gestion capteur I2C CCS811
from suiviairmenuiserieapp.ccs811_mqtt_projetclasses.communication_mqtt_ccs811 import CommunicationCCS811  # Communication MQTT

# Configuration du logger pour le suivi des événements et erreurs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

class ModeleAccueil:
    """
    Modèle principal du projet.
    Gère la logique métier liée au capteur CCS811 (CO2/TVOC), les seuils dynamiques,
    la communication MQTT et le calcul des moyennes.
    Ce modèle est responsable de la robustesse applicative et de la conformité industrielle.
    """

    def __init__(self, controleur=None):
        """
        Initialise le modèle :
        - Prépare les variables de mesures, seuils, et état du capteur.
        - Instancie le capteur CCS811.
        - Instancie la communication MQTT pour l'envoi des mesures.
        - Lance un thread pour écouter les seuils MQTT en temps réel.
        :param controleur: Référence au contrôleur principal (pour notifier la vue)
        """
        # Initialisation des valeurs pour CO2 et TVOC
        self.co2 = 0  # Valeur initiale de CO2 (ppm)
        self.tvoc = 0  # Valeur initiale de TVOC (ppb)
        self.capteurs = {}  # Dictionnaire pour stocker les données des capteurs supplémentaires
        self.capteur_disponible = True  # Suivi de l'état du capteur
        # Compteurs et sommes cumulées pour les moyennes
        self.nb_co2 = 0
        self.somme_co2 = 0
        self.nb_tvoc = 0
        self.somme_tvoc = 0
        self.type_capteur = "CCS811"  # Uniquement "CCS811"
        self.capteur_ccs811 = None
        # Seuils dynamiques pour CO2 et TVOC (modifiables via MQTT)
        self.seuils = {
            "co2": self._seuils_par_defaut("co2"),
            "tvoc": self._seuils_par_defaut("tvoc")
        }
        self.controleur = controleur  # Référence au contrôleur principal
        self.seuils_mis_a_jour = False  # Indique si les seuils ont été mis à jour récemment

        # Initialisation du capteur CCS811 (I2C)
        try:
            self.capteur_ccs811 = GestionTVOC_CO2()
            logger.info("Capteur CCS811 initialisé dans ModeleAccueil.")
        except Exception as exception:
            logger.error(f"Erreur d'initialisation du capteur CCS811 : {exception}")
            self.capteur_ccs811 = None
            self.capteur_disponible = False

        # Initialisation de l'objet MQTT pour publier les mesures
        try:
            import socket
            broker_host = "mqtt.marais2025.btssn.ovh"
            try:
                socket.create_connection((broker_host, 8883), timeout=5)
                reseau_ok = True
            except Exception as net_exc:
                logger.warning(f"Réseau injoignable ou port MQTT fermé : {net_exc}")
                reseau_ok = False

            if reseau_ok:
                try:
                    default_timeout = socket.getdefaulttimeout()
                    socket.setdefaulttimeout(7)
                    self.mqtt_sender = CommunicationCCS811(
                        broker_host, 8883, "root", "hyrome49#"
                    )
                    socket.setdefaulttimeout(default_timeout)
                except Exception as exception:
                    logger.error(f"Erreur lors de l'initialisation de CommunicationCCS811 : {exception}")
                    self.mqtt_sender = None
            else:
                logger.warning("MQTT non initialisé car le réseau n'est pas disponible.")
                self.mqtt_sender = None
        except Exception as exception:
            logger.error(f"Erreur d'initialisation MQTT : {exception}")
            self.mqtt_sender = None

        # Lancement du thread pour écouter les seuils MQTT (asynchrone)
        try:
            threading.Thread(target=self._init_mqtt_seuils, daemon=True).start()
        except Exception as exception:
            logger.error(f"Erreur lors du lancement du thread MQTT seuils : {exception}")

    def _seuils_par_defaut(self, type_mesure):
        """
        Retourne les seuils par défaut pour un type de mesure.
        :param type_mesure: "co2" ou "tvoc"
        :return: dict avec seuil_correct et seuil_limite
        Les seuils sont conformes aux recommandations industrielles.
        """
        if type_mesure == "co2":
            return {"seuil_correct": 1000, "seuil_limite": 2000}
        elif type_mesure == "tvoc":
            return {"seuil_correct": 500, "seuil_limite": 1000}
        return {"seuil_correct": 0, "seuil_limite": 0}

    def _mettre_a_jour_seuils_depuis_donnees(self, type_mesure, donnees_seuils):
        """
        Met à jour les seuils pour un type de mesure à partir d'un dictionnaire de données.
        :param type_mesure: "co2" ou "tvoc"
        :param donnees_seuils: dict contenant les seuils
        :return: True si mise à jour, False sinon
        Cette méthode permet une adaptation dynamique des seuils via MQTT.
        """
        if "seuil_correct" in donnees_seuils and "seuil_limite" in donnees_seuils:
            self.seuils[type_mesure] = {
                "seuil_correct": donnees_seuils["seuil_correct"],
                "seuil_limite": donnees_seuils["seuil_limite"]
            }
            logger.info(f"[MQTT] Seuils {type_mesure.upper()} reçus (démarrage ou mise à jour) : {self.seuils[type_mesure]}")
            return True
        return False

    def _gerer_erreur_mqtt(self, message, exception):
        """
        Log l'erreur MQTT de manière centralisée.
        :param message: Message d'erreur
        :param exception: Exception capturée
        Permet une gestion robuste des erreurs réseau.
        """
        logger.error(f"{message} : {exception}")

    def _init_mqtt_seuils(self):
        """
        Lance un client MQTT secondaire pour écouter les seuils CO2/TVOC.
        Dès qu'un seuil est reçu, il est appliqué et la vue est notifiée.
        Cette méthode fonctionne en thread séparé pour ne pas bloquer l'application principale.
        """
        try:
            import paho.mqtt.client as mqtt

            def on_connect(client, userdata, flags, rc):
                # Souscrit aux topics de seuils dès la connexion MQTT
                try:
                    if rc == 0:
                        client.subscribe("seuil/CO2")
                        client.subscribe("seuil/TVOC")
                        logger.info("Souscrit aux topics seuil/CO2 et seuil/TVOC")
                except Exception as exception:
                    logger.error(f"Erreur lors de la souscription aux topics seuils : {exception}")

            def on_message(client, userdata, msg):
                # Décode et applique les seuils reçus via MQTT
                try:
                    donnees = json.loads(msg.payload.decode())
                    mise_a_jour = False
                    if msg.topic == "seuil/CO2":
                        mise_a_jour = self._mettre_a_jour_seuils_depuis_donnees("co2", donnees)
                    elif msg.topic == "seuil/TVOC":
                        mise_a_jour = self._mettre_a_jour_seuils_depuis_donnees("tvoc", donnees)
                    # Si seuils mis à jour, notifier la vue via le contrôleur
                    if mise_a_jour:
                        self.seuils_mis_a_jour = True
                        if self.controleur is not None:
                            from kivy.clock import Clock
                            Clock.schedule_once(lambda dt: self.controleur.mettre_a_jour_affichage_seuils(), 0)
                except Exception as exception:
                    logger.error(f"Erreur décodage seuils MQTT : {exception}")

            client = mqtt.Client()
            client.username_pw_set("root", "hyrome49#")
            client.tls_set()
            client.tls_insecure_set(True)
            client.on_connect = on_connect
            client.on_message = on_message
            try:
                client.connect("mqtt.marais2025.btssn.ovh", 8883)
                client.loop_forever()
            except Exception as exception:
                logger.error(f"Erreur connexion MQTT seuils : {exception}")
        except Exception as exception:
            logger.error(f"Erreur lors de l'initialisation du client MQTT seuils : {exception}")

    def set_type_capteur(self, type_capteur):
        """
        Permet de changer dynamiquement le type de capteur utilisé.
        (Actuellement, seul CCS811 est supporté)
        :param type_capteur: str, nom du capteur
        """
        if type_capteur == "CCS811":
            self.type_capteur = type_capteur
            logger.info(f"Type de capteur changé pour : {type_capteur}")
        else:
            logger.warning(f"Type de capteur non supporté : {type_capteur}")

    def lire_donnees_capteur(self):
        """
        Lit les données du capteur CCS811.
        Met à jour les valeurs internes (CO2, TVOC) et l'état du capteur.
        Si le capteur est déconnecté, tente une reconnexion automatique.
        Cette méthode garantit la robustesse de la collecte de données (aucun crash si capteur absent).
        """
        capteur = self.capteur_ccs811
        if not capteur:
            try:
                self.capteur_ccs811 = GestionTVOC_CO2()
                capteur = self.capteur_ccs811
                logger.info("Capteur CCS811 reconnecté et initialisé.")
                self.capteur_disponible = True
            except Exception as exception:
                logger.error("Capteur CCS811 non initialisé, lecture impossible.")
                self.co2, self.tvoc = 0, 0
                self.capteur_disponible = False
                return
        try:
            co2, tvoc = capteur.obtenir_mesure()
            if co2 is not None and tvoc is not None:
                self.co2 = co2
                self.tvoc = tvoc
                self.capteur_disponible = True
                # Incrémentation des compteurs et sommes pour la moyenne
                self.nb_co2 += 1
                self.somme_co2 += co2
                self.nb_tvoc += 1
                self.somme_tvoc += tvoc
            else:
                self.capteur_ccs811 = None
                self.co2, self.tvoc = 0, 0
                self.capteur_disponible = False
        except Exception as exception:
            logger.error(f"Erreur lors de la lecture du capteur CCS811 : {exception}")
            self.capteur_ccs811 = None
            self.co2, self.tvoc = 0, 0
            self.capteur_disponible = False

    def get_co2_tvoc(self):
        """
        Retourne les valeurs actuelles du capteur CCS811.
        :return: tuple (co2, tvoc)
        """
        return self.co2, self.tvoc

    def verifier_seuils(self):
        """
        Vérifie les seuils pour le capteur CCS811 selon les seuils reçus par MQTT.
        Retourne un dictionnaire d'alertes pour l'affichage.
        Utilise en priorité les seuils reçus du broker, sinon les valeurs par défaut.
        :return: dict {"co2": "normal|danger", "tvoc": "normal|danger", "capteur": "connecte|deconnecte"}
        """
        seuils_co2 = self.seuils.get("co2", {})
        if not ("seuil_correct" in seuils_co2 and "seuil_limite" in seuils_co2):
            seuil_co2 = self._seuils_par_defaut("co2")
        else:
            seuil_co2 = seuils_co2

        seuils_tvoc = self.seuils.get("tvoc", {})
        if not ("seuil_correct" in seuils_tvoc and "seuil_limite" in seuils_tvoc):
            seuil_tvoc = self._seuils_par_defaut("tvoc")
        else:
            seuil_tvoc = seuils_tvoc

        # Fonction interne pour déterminer l'état d'alerte selon la valeur et les seuils
        def obtenir_alerte(valeur, seuil):
            # Retourne l'état d'alerte selon la valeur et les seuils
            if valeur is None:
                return "indisponible"
            if valeur < seuil["seuil_limite"]:
                return "normal"
            return "danger"

        alertes = {
            "co2": obtenir_alerte(self.co2, seuil_co2),
            "tvoc": obtenir_alerte(self.tvoc, seuil_tvoc),
            "capteur": "connecte" if self.capteur_disponible else "deconnecte"
        }
        return alertes

    def get_moyenne_journaliere(self):
        """
        Calcule et retourne les moyennes journalières formatées pour affichage.
        :return: dict {"co2": "Moy : ... ppm", "tvoc": "Moy : ... ppb"}
        """
        moyenne_co2 = self.somme_co2 / self.nb_co2 if self.nb_co2 else 0
        moyenne_tvoc = self.somme_tvoc / self.nb_tvoc if self.nb_tvoc else 0
        return {
            "co2": f"Moy : {moyenne_co2:.0f} ppm",
            "tvoc": f"Moy : {moyenne_tvoc:.0f} ppb"
        }

    def envoyer_mesures_mqtt(self):
        """
        Envoie les dernières valeurs lues au broker MQTT (sans relire les capteurs).
        Utilise la classe CommunicationCCS811 pour publier sur le broker.
        Cette méthode assure la traçabilité des mesures.
        """
        logger.info(f"[MQTT] Envoi des mesures au broker : type_capteur={self.type_capteur}, valeurs={self.get_co2_tvoc()}")
        if self.mqtt_sender:
            try:
                self.mqtt_sender.envoyer("co2", self.co2, "ppm")
                self.mqtt_sender.envoyer("tvoc", self.tvoc, "ppb")
            except Exception as exception:
                logger.error(f"Erreur lors de l'envoi périodique MQTT : {exception}")
                self.mqtt_sender = None

    def reset_seuils_mis_a_jour(self):
        """
        Remet à False le flag après affichage d'une notification de seuils mis à jour.
        """
        self.seuils_mis_a_jour = False