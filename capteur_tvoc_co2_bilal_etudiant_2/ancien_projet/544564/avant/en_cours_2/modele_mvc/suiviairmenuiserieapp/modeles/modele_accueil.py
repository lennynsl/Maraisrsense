# ==========================================================
# modele_accueil.py
# Version : 1.3.0 (Ajout du support dynamique CCS811/SDS011, adaptation automatique du topic MQTT, documentation améliorée)
# Modèle principal pour la gestion des données capteurs (CCS811 ou SDS011)
# dans le projet Modèle_MVC (architecture MVC)
# ==========================================================

from suiviairmenuiserieapp.ccs811_mqtt_projetclasses.gestion_tvoc_co2 import GestionTVOC_CO2  # Gestion capteur I2C CCS811
from suiviairmenuiserieapp.ccs811_mqtt_projetclasses.communication_mqtt_ccs811 import CommunicationCCS811  # Communication MQTT
import datetime  # Pour la gestion des dates et heures
import warnings  # Pour la gestion des avertissements

class ModeleAccueil:
    """
    Modèle qui permet de gérer les données de l'Accueil.
    Peut fonctionner avec un capteur CCS811 (CO2/TVOC) ou SDS011 (PM2.5/PM10).
    Gère la publication MQTT et l'adaptation dynamique selon le capteur branché.
    """
    def __init__(self):
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
        self.type_capteur = "CCS811"  # "CCS811" ou "SDS011"
        self.capteur_ccs811 = None
        self.capteur_sds011 = None

        # Initialisation du capteur CCS811 (I2C)
        try:
            self.capteur_ccs811 = GestionTVOC_CO2()
            print("✅ Capteur CCS811 initialisé dans ModeleAccueil.")
        except Exception as e:
            print(f"❌ Erreur d'initialisation du capteur CCS811 dans ModeleAccueil : {e}")
            self.capteur_ccs811 = None
            self.capteur_disponible = False
        # Initialisation du capteur SDS011 (UART) via capteur_pm
        try:
            from suiviairmenuiserieapp.capteur_pm.gestionpm import GestionPM
            self.capteur_sds011 = GestionPM()
            print("✅ Capteur SDS011 initialisé dans ModeleAccueil.")
        except Exception as e:
            print(f"❌ Erreur d'initialisation du capteur SDS011 : {e}")
            self.capteur_sds011 = None

        # Initialisation de l'objet MQTT pour publier les mesures
        try:
            import socket
            broker_host = "mqtt.marais2025.btssn.ovh"
            try:
                socket.create_connection((broker_host, 8883), timeout=5)
                reseau_ok = True
            except Exception as net_exc:
                print(f"❌ Réseau injoignable ou port MQTT fermé : {net_exc}")
                reseau_ok = False

            if reseau_ok:
                default_timeout = socket.getdefaulttimeout()
                socket.setdefaulttimeout(10)
                self.mqtt_sender = CommunicationCCS811(
                    broker_host, 8883, "root", "hyrome49#"
                )
                socket.setdefaulttimeout(default_timeout)
            else:
                print("❌ MQTT non initialisé car le réseau n'est pas disponible.")
                self.mqtt_sender = None
        except Exception as e:
            print(f"❌ Erreur d'initialisation MQTT : {e}")
            self.mqtt_sender = None

    def set_type_capteur(self, type_capteur):
        """
        Permet de changer dynamiquement le type de capteur utilisé.
        """
        if type_capteur in ["CCS811", "SDS011"]:
            self.type_capteur = type_capteur
            print(f"🔄 Type de capteur changé pour : {type_capteur}")
        else:
            print(f"❌ Type de capteur inconnu : {type_capteur}")

    def lire_donnees_capteur(self):
        """
        Lit les données du capteur sélectionné (CCS811 ou SDS011).
        Met à jour les valeurs et publie sur MQTT.
        """
        if self.type_capteur == "CCS811":
            capteur = self.capteur_ccs811
            if not capteur:
                try:
                    self.capteur_ccs811 = GestionTVOC_CO2()
                    capteur = self.capteur_ccs811
                    print("✅ Capteur CCS811 reconnecté et initialisé.")
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
                    # Publication MQTT
                    if self.mqtt_sender:
                        try:
                            self.mqtt_sender.envoyer("co2", co2, "ppm")
                            self.mqtt_sender.envoyer("tvoc", tvoc, "ppb")
                        except Exception as e:
                            self.mqtt_sender = None
                else:
                    self.capteur_ccs811 = None
                    self.co2, self.tvoc = 0, 0
                    self.capteur_disponible = False
            except Exception as e:
                self.capteur_ccs811 = None
                self.co2, self.tvoc = 0, 0
                self.capteur_disponible = False
        elif self.type_capteur == "SDS011":
            capteur = self.capteur_sds011
            if not capteur:
                try:
                    from suiviairmenuiserieapp.capteur_pm.gestionpm import GestionPM
                    self.capteur_sds011 = GestionPM()
                    capteur = self.capteur_sds011
                    print("✅ Capteur SDS011 reconnecté et initialisé.")
                    self.capteur_disponible = True
                except Exception as e:
                    print("Capteur SDS011 non initialisé, lecture impossible.")
                    self.pm25, self.pm10 = 0, 0
                    self.capteur_disponible = False
                    return
            try:
                pm25, pm10 = capteur.get_valeur()
                self.pm25 = pm25
                self.pm10 = pm10
                self.capteur_disponible = True
                # Publication MQTT
                if self.mqtt_sender:
                    try:
                        self.mqtt_sender.envoyer("pm25", pm25, "ugm3")
                        self.mqtt_sender.envoyer("pm10", pm10, "ugm3")
                    except Exception as e:
                        self.mqtt_sender = None
            except Exception as e:
                self.capteur_sds011 = None
                self.pm25, self.pm10 = 0, 0
                self.capteur_disponible = False

    def get_co2_tvoc(self):
        """
        Retourne les valeurs actuelles selon le capteur sélectionné.
        """
        if self.type_capteur == "CCS811":
            return self.co2, self.tvoc
        elif self.type_capteur == "SDS011":
            return self.pm25, self.pm10

    def verifier_seuils(self):
        """
        Vérifie les seuils selon le capteur sélectionné.
        Retourne un dictionnaire d'alertes pour l'affichage.
        """
        if self.type_capteur == "CCS811":
            alertes = {
                "co2": "indisponible" if self.co2 is None else "normal" if self.co2 < 1000 else "attention" if self.co2 < 2000 else "danger",
                "tvoc": "indisponible" if self.tvoc is None else "normal" if self.tvoc < 500 else "attention" if self.tvoc < 1000 else "danger",
                "capteur": "connecte" if self.capteur_disponible else "deconnecte"
            }
        elif self.type_capteur == "SDS011":
            alertes = {
                "pm25": "normal" if self.pm25 < 25 else "attention" if self.pm25 < 50 else "danger",
                "pm10": "normal" if self.pm10 < 50 else "attention" if self.pm10 < 100 else "danger",
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