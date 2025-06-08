# ==========================================================
# modele_accueil.py
# Version : 1.3.0 (Ajout du support dynamique CCS811, adaptation automatique du topic MQTT, documentation améliorée)
# Modèle principal pour la gestion des données capteurs (CCS811)
# dans le projet Modèle_MVC (architecture MVC)
# ==========================================================

from suiviairmenuiserieapp.ccs811_mqtt_projetclasses.gestion_tvoc_co2 import GestionTVOC_CO2  # Gestion capteur I2C CCS811
from suiviairmenuiserieapp.ccs811_mqtt_projetclasses.communication_mqtt_ccs811 import CommunicationCCS811  # Communication MQTT
import datetime  # Pour la gestion des dates et heures
import warnings  # Pour la gestion des avertissements
import json  # Pour décoder le message MQTT des seuils
import threading  # Pour lancer le client MQTT secondaire en thread

class ModeleAccueil:
    """
    Modèle qui permet de gérer les données de l'Accueil.
    Fonctionne uniquement avec un capteur CCS811 (CO2/TVOC).
    Gère la publication MQTT.
    """
    def __init__(self, controleur=None):
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
        self.seuils = {
            "co2": {"correct_seuil": 1000, "limite_seuil": 2000},
            "tvoc": {"correct_seuil": 500, "limite_seuil": 1000}
        }
        self.controleur = controleur  # Ajout d'une référence au contrôleur

        # Initialisation du capteur CCS811 (I2C)
        try:
            self.capteur_ccs811 = GestionTVOC_CO2()
            print("Capteur CCS811 initialisé dans ModeleAccueil.")
        except Exception as e:
            print(f"Erreur d'initialisation du capteur CCS811 dans ModeleAccueil : {e}")
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
                print(f"Réseau injoignable ou port MQTT fermé : {net_exc}")
                reseau_ok = False

            if reseau_ok:
                default_timeout = socket.getdefaulttimeout()
                socket.setdefaulttimeout(7)
                self.mqtt_sender = CommunicationCCS811(
                    broker_host, 8883, "root", "hyrome49#"
                )
                socket.setdefaulttimeout(default_timeout)
            else:
                print("MQTT non initialisé car le réseau n'est pas disponible.")
                self.mqtt_sender = None
        except Exception as e:
            print(f"Erreur d'initialisation MQTT : {e}")
            self.mqtt_sender = None

        # Ajout : lancement du client MQTT secondaire pour écouter les seuils
        threading.Thread(target=self._init_mqtt_seuils, daemon=True).start()

    def _init_mqtt_seuils(self):
        import paho.mqtt.client as mqtt
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                client.subscribe("seuil/CO2")
                client.subscribe("seuil/TVOC")
                print("Souscrit aux topics seuil/CO2 et seuil/TVOC")
        def on_message(client, userdata, msg):
            try:
                data = json.loads(msg.payload.decode())
                maj = False
                if msg.topic == "seuil/CO2":
                    if "correct_seuil" in data and "limite_seuil" in data:
                        self.seuils["co2"] = {
                            "correct_seuil": data["correct_seuil"],
                            "limite_seuil": data["limite_seuil"]
                        }
                        print(f"[MQTT] Seuils CO2 reçus (démarrage ou update) : {self.seuils['co2']}")
                        maj = True
                elif msg.topic == "seuil/TVOC":
                    if "correct_seuil" in data and "limite_seuil" in data:
                        self.seuils["tvoc"] = {
                            "correct_seuil": data["correct_seuil"],
                            "limite_seuil": data["limite_seuil"]
                        }
                        print(f"[MQTT] Seuils TVOC reçus (démarrage ou update) : {self.seuils['tvoc']}")
                        maj = True
                # Mise à jour immédiate de l'affichage si le contrôleur est disponible
                if maj and self.controleur is not None:
                    from kivy.clock import Clock
                    Clock.schedule_once(lambda dt: self.controleur.mettre_a_jour_co2_tvoc(), 0)
            except Exception as e:
                print(f"Erreur décodage seuils MQTT : {e}")
        client = mqtt.Client()
        client.username_pw_set("root", "hyrome49#")
        client.tls_set()
        client.tls_insecure_set(True)
        client.on_connect = on_connect
        client.on_message = on_message
        try:
            client.connect("mqtt.marais2025.btssn.ovh", 8883)
            client.loop_forever()
        except Exception as e:
            print(f"Erreur connexion MQTT seuils : {e}")

    def set_type_capteur(self, type_capteur):
        """
        Permet de changer dynamiquement le type de capteur utilisé.
        (Désormais, seul CCS811 est supporté)
        """
        if type_capteur == "CCS811":
            self.type_capteur = type_capteur
            print(f"Type de capteur changé pour : {type_capteur}")
        else:
            print(f"Type de capteur non supporté : {type_capteur}")

    def lire_donnees_capteur(self):
        """
        Lit les données du capteur CCS811.
        Met à jour les valeurs.
        """
        capteur = self.capteur_ccs811
        if not capteur:
            try:
                self.capteur_ccs811 = GestionTVOC_CO2()
                capteur = self.capteur_ccs811
                print("Capteur CCS811 reconnecté et initialisé.")
                self.capteur_disponible = True
            except Exception as e:
                print("Capteur CCS811 non initialisé, lecture impossible.")
                self.co2, self.tvoc = 0, 0
                self.capteur_disponible = False
                return
        try:
            co2, tvoc = capteur.get_mesure()
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
        except Exception as e:
            self.capteur_ccs811 = None
            self.co2, self.tvoc = 0, 0
            self.capteur_disponible = False

    def get_co2_tvoc(self):
        """
        Retourne les valeurs actuelles du capteur CCS811.
        """
        return self.co2, self.tvoc

    def verifier_seuils(self):
        """
        Vérifie les seuils pour le capteur CCS811 selon les seuils reçus par MQTT.
        Retourne un dictionnaire d'alertes pour l'affichage.
        Utilise en priorité les seuils reçus du broker, sinon les valeurs par défaut.
        """
        seuils_co2 = self.seuils.get("co2", {})
        if not ("correct_seuil" in seuils_co2 and "limite_seuil" in seuils_co2):
            seuil_co2 = {"correct_seuil": 1000, "limite_seuil": 2000}
        else:
            seuil_co2 = seuils_co2

        seuils_tvoc = self.seuils.get("tvoc", {})
        if not ("correct_seuil" in seuils_tvoc and "limite_seuil" in seuils_tvoc):
            seuil_tvoc = {"correct_seuil": 500, "limite_seuil": 1000}
        else:
            seuil_tvoc = seuils_tvoc

        alertes = {
            "co2": "indisponible" if self.co2 is None else
                "normal" if self.co2 < seuil_co2["correct_seuil"] else
                "danger",
            "tvoc": "indisponible" if self.tvoc is None else
                "normal" if self.tvoc < seuil_tvoc["correct_seuil"] else
                "danger",
            "capteur": "connecte" if self.capteur_disponible else "deconnecte"
        }
        return alertes

    def get_moyenne_journaliere(self):
        """
        Retourne les textes formatés pour affichage de la moyenne
        sous la forme : "moy : .... ppm ou ppb "
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
        """
        print(f"[MQTT] Envoi des mesures au broker : type_capteur={self.type_capteur}, valeurs={self.get_co2_tvoc()}")
        if self.mqtt_sender:
            try:
                self.mqtt_sender.envoyer("co2", self.co2, "ppm")
                self.mqtt_sender.envoyer("tvoc", self.tvoc, "ppb")
            except Exception as e:
                print(f"Erreur lors de l'envoi périodique MQTT : {e}")
                self.mqtt_sender = None