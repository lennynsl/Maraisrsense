from pinpong.board import Board
from GestionTVOC_CO2 import GestionTVOC_CO2

def main():
    """
    Programme principal pour lire une seule mesure des niveaux de CO2 et TVOC
    depuis le capteur CCS811.
    """
    print("Initialisation de la carte UNIHIKER...")
    Board("UNIHIKER").begin()

    print("Initialisation du capteur CCS811...")
    capteur = GestionTVOC_CO2()

    print("Lecture des données du capteur...")
    co2, tvoc = capteur.get_mesure()

    if co2 is not None and tvoc is not None:
        print(f"Mesure réussie ! CO2: {co2} ppm, TVOC: {tvoc} ppb")
    else:
        print("Erreur : Données non disponibles ou capteur non opérationnel.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")