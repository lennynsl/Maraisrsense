from Class_CCS811 import CCS811
from pinpong.board import I2C

class CapteurTVOC_CO2:
    """
    Classe pour interagir avec le capteur CCS811 et lire les niveaux de CO2 et TVOC.
    """

    def __init__(self, i2c, address=0x5A):
        """
        Initialise le capteur avec l'adresse I2C spécifiée.
        """
        self.capteur = CCS811()
        self.capteur.setup()

    def lire_mesure(self):
        """
        Effectue une mesure unique et retourne les niveaux de CO2 et TVOC.
        """
        if self.capteur.data_available():
            self.capteur.read_logorithm_results()
            return self.capteur.CO2, self.capteur.tVOC
        elif self.capteur.check_for_error():
            self.capteur.print_error()
            return None, None
        else:
            return None, None


if __name__ == "__main__":
    # Exemple d'utilisation
    i2c = I2C()
    capteur = CapteurTVOC_CO2(i2c)
    co2, tvoc = capteur.lire_mesure()
    if co2 is not None and tvoc is not None:
        print(f"CO2: {co2} ppm, TVOC: {tvoc} ppb")
    else:
        print("Erreur ou données non disponibles.")