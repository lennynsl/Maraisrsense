from Capteur_TVOC_CO2 import CapteurTVOC_CO2
from pinpong.board import I2C

def main():
    """
    Programme principal pour lire les données du capteur CCS811.
    """
    # Initialisation de l'I2C et du capteur
    capteur = CapteurTVOC_CO2(I2C())

    # Lecture d'une mesure unique
    co2, tvoc = capteur.lire_mesure()

    # Affichage des résultats
    if co2 is not None and tvoc is not None:
        print(f"CO2: {co2} ppm, TVOC: {tvoc} ppb")
    else:
        print("Erreur ou données non disponibles.")

if __name__ == "__main__":
    main()