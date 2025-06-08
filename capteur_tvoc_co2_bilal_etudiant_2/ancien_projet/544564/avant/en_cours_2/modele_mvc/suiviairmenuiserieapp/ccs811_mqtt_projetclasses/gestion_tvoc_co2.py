# ==========================================================
# gestion_tvoc_co2.py
# Version : 1.0.1 (Ajout de documentation et commentaires structurants)
# Module pour la gestion du capteur CCS811 (CO2/TVOC)
# ==========================================================

from suiviairmenuiserieapp.ccs811_mqtt_projetclasses.ccs811 import CCS811  # Classe capteur CCS811
import time  # Pour temporisation
from pinpong.board import Board  # Pour initialiser la carte Unihiker

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
        Récupère les dernières mesures de CO2 et TVOC du capteur.
        
        Returns:
            tuple: Une paire de valeurs (CO2, TVOC) en ppm et ppb respectivement,
                   ou (None, None) si les données ne sont pas disponibles.
        """
        try:
            if self.capteur.data_available():
                self.capteur.read_logorithm_results()
                return self.capteur.CO2, self.capteur.tVOC
            else:
                return None, None
        except Exception as e:
            print(f"Erreur lors de la lecture : {e}")
            return None, None

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