import serial  # Bibliothèque pour la communication série
import time    # Bibliothèque pour gérer les temporisations
import sds011  # Bibliothèque pour interagir avec le capteur SDS011
import os      # Bibliothèque pour vérifier la présence du port série

#il faut installer ces bibliothèques au préalable sur le unihiker

# Classe pour gérer la connexion et l'interaction avec le capteur SDS011
class GestionPM:
    def __init__(self, port):
        """Initialise la gestion du capteur SDS011 sur un port donné."""
        self.port = port  # Stocke le port du capteur
        self.sensor = None  # Initialise le capteur comme non connecté
        self.init_sensor()  # Tente d'initialiser le capteur

    def init_sensor(self):
        """Initialise le capteur si le port est disponible."""
        try:
            if os.path.exists(self.port):  # Vérifie si le port existe
                if self.sensor is not None:
                    self.sensor.close()  # Ferme la connexion précédente si elle existe
                self.sensor = sds011.SDS011(self.port, use_query_mode=True)  # Initialise le capteur en mode requête
                print(f"✅ Capteur connecté sur {self.port}")
            else:
                print(f"⚠️ Port {self.port} non trouvé. Attente de reconnexion...")
                self.sensor = None
                raise
        except serial.SerialException as e:
            print(f"❌ Erreur lors de l'initialisation : {e}")
            self.sensor = None
            raise

    def __reveil_capteur(self):
        """Réveille le capteur en cas de mise en veille ou tente une reconnexion."""
        if self.sensor is None:
            print("🔄 Tentative de reconnexion au capteur...")
            self.init_sensor()
            return

        try:
            self.sensor.sleep(sleep=False)  # Réveille le capteur
        except (serial.SerialException, OSError) as e:
            print(f"⚠️ Erreur lors du réveil du capteur : {e}")
            self.sensor = None  # Réinitialise le capteur pour forcer une reconnexion
            time.sleep(5)  # Pause avant une nouvelle tentative
            raise

    def __sommeil_capteur(self):
        """Met le capteur en veille avec gestion des erreurs."""
        if self.sensor is None:
            print("🔄 Tentative de reconnexion au capteur avant mise en veille...")
            self.init_sensor()
            return
        try:
            print("💤 Mise en veille du capteur...")
            self.sensor.sleep(sleep=True)  # Met le capteur en veille
        except (serial.SerialException, OSError) as e:
            print(f"⚠️ Erreur lors de la mise en veille du capteur : {e}")
            self.sensor = None  # Réinitialise le capteur pour forcer une reconnexion
            raise

    def get_valeur(self):
        """Récupère les valeurs de particules fines PM2.5 et PM10 mesurées par le capteur."""
        try:
            self.__reveil_capteur()  # Réveille le capteur avant la mesure
            time.sleep(30)  # Attente pour stabilisation des mesures
            result = self.sensor.query()  # Requête pour obtenir les valeurs PM2.5 et PM10
            if result is not None:
                return result  # Retourne les valeurs si elles sont valides
            else:
                print("⚠️ Impossible de récupérer les données du capteur.")
                self.sensor.sleep(sleep=True)
                raise
            self.__sommeil_capteur()  # Met le capteur en veille après la mesure
        except (serial.SerialException, OSError) as e:
            print(f"⚠️ Erreur de lecture du capteur : {e}")
            self.sensor = None  # Réinitialise le capteur
            raise

# Exécution principale du programme
if __name__ == "__main__":
    while True:
        try:
            capteur = GestionPM(port="/dev/sds011")  # Initialise l'objet de gestion du capteur
            break
        except:
            time.sleep(5)  # Réessaie après 5 secondes en cas d'erreur
    
    while True:
        try:
            # Tentative de récupération des valeurs du capteur
            print("📊 Récupération des valeurs du capteur...")
            pm25, pm10 = capteur.get_valeur()
            if pm25 is not None and pm10 is not None:
                print(f"✅ Données du capteur : PM2.5 = {pm25} µg/m³, PM10 = {pm10} µg/m³")
            else:
                print("❌ Aucune donnée reçue du capteur.")
        except Exception as e:
            print(f"🚨 Erreur lors des tests : {e}")
        time.sleep(5)  # Pause de 5 secondes avant la prochaine lecture
