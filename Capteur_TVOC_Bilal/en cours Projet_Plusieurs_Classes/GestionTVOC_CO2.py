from pinpong.board import Board
from CCS811 import CCS811
import time

# Initialisation et interaction avec le capteur CCS811
class GestionCO2_TVOC:
    def __init__(self):
        try:
            self.capteur = CCS811()  # Initialise le capteur
            print("✅ Capteur CCS811 initialisé.")
        except Exception as e:
            print(f"❌ Erreur d'initialisation : {e}")
            self.capteur = None

    def get_mesures(self):
        # Vérifie si le capteur est prêt et récupère les mesures
        if self.capteur and self.capteur.data_available():
            self.capteur.read_logorithm_results()
            return self.capteur.CO2, self.capteur.tVOC
        else:
            print("⚠️ Données indisponibles ou capteur non prêt.")
            return None, None

# Programme principal
if __name__ == "__main__":
    Board("UNIHIKER").begin()  # Initialise la carte
    capteur = GestionCO2_TVOC()  # Crée un objet pour gérer le capteur

    while True:
        try:
            co2, tvoc = capteur.get_mesures()
            if co2 is not None and tvoc is not None:
                print(f"📊 CO2 : {co2} ppm, TVOC : {tvoc} ppb")
            else:
                print("⚠️ Lecture échouée.")
            time.sleep(5)  # Pause entre les lectures
        except KeyboardInterrupt:
            print("🛑 Programme arrêté par l'utilisateur.")
            break