from CCS811 import CCS811
import time


class GestionTVOC_CO2:
    """
    Classe pour interagir avec le capteur CCS811 et lire les niveaux de CO2 et TVOC.
    """

    def __init__(self):
        try:
            self.capteur = CCS811()
            print("Capteur CCS811 initialisé.")
        except Exception as e:
            print(f"Erreur d'initialisation : {e}")
            self.capteur = None

    def get_mesure(self):
        """
        Vérifie si le capteur est prêt et récupère les mesures.
        """
        if self.capteur and self.capteur.data_available():
            self.capteur.read_logorithm_results()
            return self.capteur.CO2, self.capteur.tVOC
        else:
            print("Données indisponibles ou capteur non prêt.")
            return None, None


if __name__ == "__main__":
    from pinpong.board import Board

    Board("UNIHIKER").begin()
    capteur = GestionTVOC_CO2()

    while True:
        try:
            co2, tvoc = capteur.get_mesure()
            if co2 is not None and tvoc is not None:
                print(f"CO2 : {co2} ppm, TVOC : {tvoc} ppb")
            else:
                print("Lecture échouée.")
            time.sleep(5)
        except KeyboardInterrupt:
            print("Programme arrêté par l'utilisateur.")
            break