import time
from pinpong.board import I2C, Board

# Adresse et registres du capteur CCS811
CCS811_ADDR = 0x5A # Adresse I2C par défaut
CSS811_STATUS = 0x00
CSS811_MEAS_MODE = 0x01
CSS811_ALG_RESULT_DATA = 0x02
CSS811_BASELINE = 0x11
CSS811_HW_ID = 0x20
CSS811_ERROR_ID = 0xE0
CSS811_APP_START = 0xF4

class CCS811:
    """
    Classe pour interagir avec le capteur CCS811.
    Permet de mesurer les niveaux de CO2 et de TVOC.
    """

    def __init__(self):
        """
        Initialise la carte et l'objet I2C.
        """
        self.i2c = I2C() # Initialise l'objet I2C
        self.tVOC = 0 # Niveau de TVOC (en ppb)
        self.CO2 = 0 # Niveau de CO2 (en ppm)

    def print_error(self):
        """
        Affiche les erreurs détectées par le capteur.
        """
        error = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_ERROR_ID, 1)[0]
        message = "Erreur détectée : "

        if error & (1 << 5):
            message += "Problème d'alimentation du chauffage. "
        if error & (1 << 4):
            message += "Défaut du chauffage. "
        if error & (1 << 3):
            message += "Résistance maximale atteinte. "
        if error & (1 << 2):
            message += "Mode de mesure invalide. "
        if error & (1 << 1):
            message += "Lecture de registre invalide. "
        if error & (1 << 0):
            message += "Message invalide. "

        print(message)

    def check_for_error(self):
        """
        Vérifie si une erreur est présente.
        Retourne True si une erreur est détectée.
        """
        status = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_STATUS, 1)[0]
        return bool(status & (1 << 0))

    def app_valid(self):
        """
        Vérifie si l'application du capteur est valide.
        Retourne True si valide.
        """
        status = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_STATUS, 1)[0]
        return bool(status & (1 << 4))

    def set_drive_mode(self, mode):
        """
        Configure le mode de fonctionnement du capteur.
        mode : entier (0 à 4) représentant le mode de mesure.
        """
        if mode > 4:
            mode = 4 # Limite le mode à 4 maximum

        setting = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_MEAS_MODE, 1)[0]
        setting &= ~(0b00000111 << 4)  # Réinitialise les bits de mode
        setting |= (mode << 4) # Définit le nouveau mode
        self.i2c.writeto_mem(CCS811_ADDR, CSS811_MEAS_MODE, setting)

    def configure_ccs811(self):
        """
        Configure le capteur CCS811 pour le rendre opérationnel.
        Vérifie les erreurs et initialise le mode de fonctionnement.
        """
        hardware_id = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_HW_ID, 1)[0]
        if hardware_id != 0x81:
            raise ValueError("CCS811 non détecté. Vérifiez le câblage.")

        if self.check_for_error():
            self.print_error()
            raise ValueError("Erreur au démarrage.")

        if not self.app_valid():
            raise ValueError("Application du capteur invalide.")

        self.i2c.writeto(CCS811_ADDR, bytes([CSS811_APP_START]))

        if self.check_for_error():
            self.print_error()
            raise ValueError("Erreur lors du démarrage de l'application.")

        self.set_drive_mode(1) # Définit le mode de mesure par défaut

        if self.check_for_error():
            self.print_error()
            raise ValueError("Erreur lors de la configuration du mode.")

    def setup(self):
        """
        Initialise le capteur et affiche la valeur de référence (baseline).
        """
        print("Initialisation du capteur CCS811...")
        self.configure_ccs811()

        baseline = self.get_base_line()
        print(f"Baseline du capteur : 0x{baseline:04X}")

    def get_base_line(self):
        """
        Lit la valeur de référence (baseline) du capteur.
        Retourne un entier représentant la baseline.
        """
        data = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_BASELINE, 2)
        return (data[0] << 8) | data[1]

    def data_available(self):
        """
        Vérifie si de nouvelles données sont disponibles.
        Retourne True si des données sont prêtes.
        """
        status = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_STATUS, 1)[0]
        return bool(status & (1 << 3))

    def read_logorithm_results(self):
        """
        Lit les résultats de mesure (CO2 et TVOC) du capteur.
        Met à jour les attributs CO2 et tVOC.
        """
        data = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_ALG_RESULT_DATA, 4)
        self.CO2 = (data[0] << 8) | data[1]
        self.tVOC = (data[2] << 8) | data[3]

    def run(self):
        """
        Boucle principale pour lire les données en continu.
        Affiche les niveaux de CO2 et de TVOC.
        """
        self.setup()
        while True:
            if self.data_available():
                self.read_logorithm_results()
                print(f"CO2: {self.CO2} ppm, TVOC: {self.tVOC} ppb")
            elif self.check_for_error():
                self.print_error()
            time.sleep(1)


#if __name__ == "__main__":
    # Exemple d'utilisation de la classe CCS811
    #Board("UNIHIKER").begin() # Initialise la carte UNIHIKER

    #capteur = CCS811()
    #capteur.run()