from CCS811 import CCS811
import time
from pinpong.board import  Board
class GestionTVOC_CO2:
    """
    Classe pour interagir avec le capteur CCS811 et lire les niveaux de CO2 et TVOC.
    """

    def __init__(self):
        """Initialise et configure le capteur."""
        try:
            print("🔄 Initialisation du capteur CCS811...")
            self.capteur = CCS811() # Instancie le capteur
            self.capteur.setup() # Configure le capteur
            print("✅ Capteur CCS811 correctement initialisé.")
        except Exception as e:
            print(f"❌ Échec de l'initialisation : {e}")
            self.capteur = None
            raise Exception("Impossible d'initialiser le capteur CCS811.")

    def get_mesure(self):
        """
        Effectue une mesure unique et retourne les niveaux de CO2 et TVOC.
        """
        try:
            if self.capteur.data_available():
                print("✅ Données disponibles, lecture en cours...")
                self.capteur.read_logorithm_results()  # Lecture des données
                return self.capteur.CO2, self.capteur.tVOC
            elif self.capteur.check_for_error():
                print("⚠️ Erreur détectée par le capteur.")
                self.capteur.print_error()
                # return None, None
                raise Exception("Erreur détectée lors de la lecture des données.")
            else:
                print("⚠️ Pas de nouvelles données disponibles.")
                return None, None
        except Exception as e:
            print(f"❌ Erreur lors de la lecture des mesures : {e}")
            # return None, None
            raise Exception("Erreur détectée lors de la lecture des données.")

# Programme principal
if __name__ == "__main__":
    Board("UNIHIKER").begin()  # Initialise la carte UNIHIKER

    while True:
        try:
            # Initialisation de l'objet GestionTVOC_CO2
            capteur = GestionTVOC_CO2()

            # Lecture des mesures en boucle
            while True:
                try:
                    print("📊 Récupération des valeurs du capteur...")
                    co2, tvoc = capteur.get_mesure()
                    if co2 is not None and tvoc is not None:
                        print(f"✅ Données du capteur : CO2 = {co2} ppm, TVOC = {tvoc} ppb")
                    else:
                        print("❌ Aucune donnée reçue.")
                    time.sleep(5)  # Pause entre les lectures
                except Exception as e:
                    print(f"🚨 Erreur lors des mesures : {e}")
                    time.sleep(5) # Pause avant de réessayer
                    break
        except Exception as e:
            print(f"🚨 Erreur critique : {e}")
            time.sleep(5) # Pause avant une tentative de redémarrage