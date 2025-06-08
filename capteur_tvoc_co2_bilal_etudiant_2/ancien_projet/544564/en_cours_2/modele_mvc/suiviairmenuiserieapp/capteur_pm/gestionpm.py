# ==========================================================
# gestionpm.py
# Créé par l'étudiant 1 : Lenny NASLIN (Mr NASLIN)
# Utilisé et adapté pour la carte Unihiker par l'étudiant 2 : DAG Bilal (Mr DAG)
# Version : 1.2.0 (Ajout de la détection automatique du port, gestion d'erreurs améliorée, documentation détaillée)
# Module de gestion du capteur SDS011 (particules fines) UART
# Utilisé dans le projet Modèle_MVC pour l'acquisition PM2.5/PM10
# ==========================================================

import serial
import time
import os
try:
    from suiviairmenuiserieapp.capteur_pm import sds011
except ImportError:
    import sds011         # Import global si installé via pip

class GestionPM:
    """
    Classe de gestion du capteur SDS011 (particules fines) pour Unihiker.
    Permet d'initialiser, réveiller, mettre en veille et lire les mesures PM2.5/PM10.
    """
    def __init__(self, port=None):
        """
        Initialise la gestion du capteur SDS011 sur un port donné.
        Si aucun port n'est fourni, essaie automatiquement les ports courants.
        """
        if port is None:
            # Détection automatique du port selon la plateforme
            if os.path.exists("/dev/ttyUSB0"):
                port = "/dev/ttyUSB0"
            elif os.path.exists("/dev/sds011"):
                port = "/dev/sds011"
            else:
                raise FileNotFoundError("Aucun port série SDS011 détecté (/dev/ttyUSB0 ou /dev/sds011)")
        self.port = port
        self.sensor = None  # Instance du capteur SDS011
        self.init_sensor()  # Tente d'initialiser le capteur

    def init_sensor(self):
        """
        Initialise le capteur SDS011 si le port est disponible.
        """
        try:
            if os.path.exists(self.port):  # Vérifie si le port existe physiquement
                if self.sensor is not None:
                    self.sensor.close()  # Ferme la connexion précédente si elle existe
                # Initialise le capteur en mode requête (query)
                self.sensor = sds011.SDS011(self.port, use_query_mode=True)
                print(f"✅ Capteur SDS011 connecté sur {self.port}")
            else:
                print(f"⚠️ Port {self.port} non trouvé. Attente de reconnexion...")
                self.sensor = None
                raise FileNotFoundError(f"Port {self.port} non trouvé")
        except serial.SerialException as e:
            print(f"❌ Erreur lors de l'initialisation du capteur SDS011 : {e}")
            self.sensor = None
            raise

    def __reveil_capteur(self):
        """
        Réveille le capteur SDS011 (sortie de veille) ou tente une reconnexion si besoin.
        """
        if self.sensor is None:
            print("🔄 Tentative de reconnexion au capteur SDS011...")
            self.init_sensor()
            return
        try:
            self.sensor.sleep(sleep=False)  # Réveille le capteur
        except (serial.SerialException, OSError) as e:
            print(f"⚠️ Erreur lors du réveil du capteur SDS011 : {e}")
            self.sensor = None  # Réinitialise le capteur pour forcer une reconnexion
            time.sleep(5)      # Pause avant une nouvelle tentative
            raise

    def __sommeil_capteur(self):
        """
        Met le capteur SDS011 en veille (mode basse consommation).
        """
        if self.sensor is None:
            print("🔄 Tentative de reconnexion au capteur SDS011 avant mise en veille...")
            self.init_sensor()
            return
        try:
            print("💤 Mise en veille du capteur SDS011...")
            self.sensor.sleep(sleep=True)  # Met le capteur en veille
        except (serial.SerialException, OSError) as e:
            print(f"⚠️ Erreur lors de la mise en veille du capteur SDS011 : {e}")
            self.sensor = None
            raise

    def get_valeur(self):
        """
        Récupère les valeurs de particules fines PM2.5 et PM10 mesurées par le capteur SDS011.
        Retourne un tuple (pm25, pm10) en µg/m³.
        """
        try:
            self.__reveil_capteur()  # Réveille le capteur avant la mesure
            time.sleep(30)           # Attente pour stabilisation des mesures (important pour SDS011)
            result = self.sensor.query()  # Requête pour obtenir les valeurs PM2.5 et PM10
            if result is not None:
                return result        # Retourne les valeurs si elles sont valides
            else:
                print("⚠️ Impossible de récupérer les données du capteur SDS011.")
                self.sensor.sleep(sleep=True)
                raise Exception("Aucune donnée reçue du capteur SDS011")
        except (serial.SerialException, OSError) as e:
            print(f"⚠️ Erreur de lecture du capteur SDS011 : {e}")
            self.sensor = None
            raise

# ==========================================================
# Exemple d'utilisation autonome (test direct)
# ==========================================================
if __name__ == "__main__":
    # Boucle d'initialisation du capteur
    while True:
        try:
            capteur = GestionPM()  # Initialise l'objet de gestion du capteur (port auto)
            break
        except Exception as e:
            print(f"Erreur d'init capteur : {e}")
            time.sleep(5)  # Réessaie après 5 secondes en cas d'erreur

    # Boucle principale de lecture des valeurs
    while True:
        try:
            print("📊 Récupération des valeurs du capteur SDS011...")
            pm25, pm10 = capteur.get_valeur()
            if pm25 is not None and pm10 is not None:
                print(f"✅ Données du capteur : PM2.5 = {pm25} µg/m³, PM10 = {pm10} µg/m³")
            else:
                print("❌ Aucune donnée reçue du capteur SDS011.")
        except Exception as e:
            print(f"🚨 Erreur lors des tests SDS011 : {e}")
        time.sleep(5)  # Pause de 5 secondes avant la prochaine lecture
