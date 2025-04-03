from pinpong.board import Board, I2C
from GestionTVOC_CO2 import GestionTVOC_CO2

def main():
    """
    Programme principal pour lire une seule mesure des niveaux de CO2 et TVOC
    depuis le capteur CCS811.
    """
    # Initialisation de la carte
    print("Initialisation de la carte UNIHIKER...")
    Board("UNIHIKER").begin() 

    # Initialisation de l'I2C et du capteur
    print("Initialisation du capteur CCS811...")
    i2c = I2C()  # Instanciation de l'I2C
    capteur = CapteurTVOC_CO2(i2c)  # Instanciation de la classe avec i2c

    # Lecture d'une mesure unique
    print("Lecture des données du capteur...")
    co2, tvoc = capteur.lire_mesure()

    # Affichage des résultats
    if co2 is not None and tvoc is not None:
        print(f"Mesure réussie ! CO2: {co2} ppm, TVOC: {tvoc} ppb")
    else:
        print("Erreur : Données non disponibles ou capteur non opérationnel.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")