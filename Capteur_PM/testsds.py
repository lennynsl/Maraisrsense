import serial
import time
import sds011
import os

#installer les bibliothèques serial, pyserial, time, sds011 et os

class GestionPM:
    def __init__(self, port):
        self.port = port
        self.sensor = None
        self.init_sensor()

    def init_sensor(self):
        """ Initialise le capteur si le port est disponible. """
        try:
            if os.path.exists(self.port):
                if self.sensor is not None:
                    self.sensor.close()
                self.sensor = sds011.SDS011(self.port, use_query_mode=True)
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
        """ Gestion du capteur avec reconnexion automatique """
        if self.sensor is None:
            print("🔄 Tentative de reconnexion au capteur...")
            self.init_sensor()
            return

        try:
            self.sensor.sleep(sleep=False)
        except (serial.SerialException, OSError) as e:
            print(f"⚠️ Erreur lors du réveil du capteur : {e}")
            self.sensor = None  # Réinitialise le capteur pour forcer une reconnexion au prochain cycle
            time.sleep(self.intervalle)
            raise

    def __sommeil_capteur(self):
        """ Met le capteur en veille avec gestion des erreurs et reconnexion automatique """
        if self.sensor is None:
            print("🔄 Tentative de reconnexion au capteur avant mise en veille...")
            self.init_sensor()
            return

        try:
            print("💤 Mise en veille du capteur...")
            self.sensor.sleep(sleep=True)
            # time.sleep(2)  # Petite pause pour éviter une surcharge
        except (serial.SerialException, OSError) as e:
            print(f"⚠️ Erreur lors de la mise en veille du capteur : {e}")
            self.sensor = None  # Réinitialise le capteur pour forcer une reconnexion au prochain cycle
            raise


    def get_valeur(self):    
        # if self.sensor is None:
        #     return None, None
        
        try:
            self.__reveil_capteur()
            time.sleep(30)
            result = self.sensor.query()
            if result is not None:
                return result
            else:
                print("⚠️ Impossible de récupérer les données du capteur.")
                self.sensor.sleep(sleep=True)
                raise
            self.__sommeil_capteur()
        # return None, None
        except (serial.SerialException, OSError) as e:
            print(f"⚠️ Erreur de lecture du capteur : {e}")
            self.sensor = None
            raise
            # return None, None
            

if __name__ == "__main__":  
    while True:
        try :
            capteur = GestionPM(port="/dev/sds011")
            break
        except :
            time.sleep(5)
    while True:    
        try:
            # Test de récupération des valeurs
            print("📊 Récupération des valeurs du capteur...")
            pm25, pm10 = capteur.get_valeur()
            if pm25 is not None and pm10 is not None:
                print(f"✅ Données du capteur : PM2.5 = {pm25} µg/m³, PM10 = {pm10} µg/m³")
            else:
                print("❌ Aucune donnée reçue du capteur.")
            
        except Exception as e:
            print(f"🚨 Erreur lors des tests : {e}")
        time.sleep(5)