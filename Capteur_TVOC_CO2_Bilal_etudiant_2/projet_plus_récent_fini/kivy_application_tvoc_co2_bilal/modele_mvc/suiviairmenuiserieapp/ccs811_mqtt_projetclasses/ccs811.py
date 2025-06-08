# ==========================================================
# ccs811.py
# Module bas niveau pour la gestion du capteur CCS811 (I2C)
# Fournit une interface directe pour initialiser et lire les mesures du capteur CCS811.
# ==========================================================
"""
Module : ccs811.py

Ce module fournit une classe pour interagir avec le capteur CCS811 via I2C.
Il permet d'initialiser le capteur, de configurer les modes de mesure, de lire les valeurs de CO2 et TVOC,
et de diagnostiquer les erreurs matérielles. Ce module est destiné à être utilisé par des couches supérieures
pour la gestion de la qualité de l'air.

Utilisation typique :
    capteur = CCS811()
    capteur.setup()
    if capteur.data_available():
        capteur.read_logorithm_results()
        print(capteur.CO2, capteur.tVOC)

Références :
- Datasheet CCS811 : https://www.sciosense.com/wp-content/uploads/documents/CCS811_Datasheet.pdf
- Registres principaux :
    - 0x00 : STATUS
    - 0x01 : MEAS_MODE
    - 0x02 : ALG_RESULT_DATA
    - 0x11 : BASELINE
    - 0x20 : HW_ID
    - 0xE0 : ERROR_ID
    - 0xF4 : APP_START
"""

import time
from pinpong.board import I2C, Board

# Adresse I2C et registres du capteur CCS811
CCS811_ADDR = 0x5A  # Adresse I2C par défaut du capteur CCS811
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
    Fournit des méthodes pour initialiser, configurer et lire les données du capteur.
    """

    def __init__(self):
        """
        Initialise la carte Unihiker et l'objet I2C.
        Prépare les attributs pour stocker les mesures de CO2 et TVOC.
        Lève une exception si l'initialisation échoue.
        """
        try:
            print("Initialisation de la carte Unihiker...")
            Board("UNIHIKER").begin()
            self.i2c = I2C()
            self.tVOC = 0  # Niveau de TVOC (en ppb)
            self.CO2 = 0   # Niveau de CO2 (en ppm)
            print("I2C initialisé avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'initialisation de l'I2C : {e}")
            self.i2c = None

    def print_error(self):
        """
        Affiche les erreurs détectées par le capteur CCS811.
        Décrypte les bits du registre d'erreur pour fournir un diagnostic détaillé.
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
        Vérifie si une erreur est présente dans le capteur.
        :return: True si une erreur est détectée, False sinon.
        """
        status = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_STATUS, 1)[0]
        return bool(status & (1 << 0))

    def app_valid(self):
        """
        Vérifie si l'application du capteur CCS811 est valide.
        :return: True si l'application est valide, False sinon.
        """
        status = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_STATUS, 1)[0]
        return bool(status & (1 << 4))

    def set_drive_mode(self, mode):
        """
        Configure le mode de fonctionnement du capteur CCS811.
        :param mode: entier (0 à 4) représentant le mode de mesure.
        Modes disponibles :
            0 : Mesure arrêtée
            1 : 1 mesure/seconde
            2 : 10 mesures/seconde
            3 : 60 mesures/seconde
            4 : Mesure à la demande
        """
        if mode > 4:
            mode = 4  # Limite le mode à 4 maximum

        setting = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_MEAS_MODE, 1)[0]
        setting &= ~(0b00000111 << 4)  # Réinitialise les bits de mode
        setting |= (mode << 4)  # Définit le nouveau mode
        self.i2c.writeto_mem(CCS811_ADDR, CSS811_MEAS_MODE, setting)

    def configure_ccs811(self):
        """
        Configure le capteur CCS811 pour le rendre opérationnel.
        Vérifie les erreurs et initialise le mode de fonctionnement.
        Lève une exception si le capteur n'est pas détecté ou si une erreur est présente.
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

        self.set_drive_mode(1)  # Définit le mode de mesure par défaut (1 mesure/seconde)

        if self.check_for_error():
            self.print_error()
            raise ValueError("Erreur lors de la configuration du mode.")

    def setup(self):
        """
        Initialise le capteur CCS811 et affiche la valeur de référence (baseline) en hexadécimal.
        Lève une exception si l'I2C n'est pas initialisé.
        """
        if self.i2c is None:
            raise ValueError("I2C non initialisé. Impossible de configurer le capteur.")
        print("Initialisation du capteur CCS811...")
        self.configure_ccs811()
        print("Capteur CCS811 configuré avec succès.")

        baseline = self.get_base_line()
        print(f"Baseline du capteur : 0x{baseline:04X}")

    def get_base_line(self):
        """
        Lit la valeur de référence (baseline) du capteur CCS811.
        :return: entier représentant la baseline.
        """
        data = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_BASELINE, 2)
        return (data[0] << 8) | data[1]

    def data_available(self):
        """
        Vérifie si de nouvelles données sont disponibles sur le capteur CCS811.
        :return: True si des données sont prêtes à être lues, False sinon.
        """
        status = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_STATUS, 1)[0]
        return bool(status & (1 << 3))

    def read_logorithm_results(self):
        """
        Lit les résultats de mesure (CO2 et TVOC) du capteur CCS811.
        Met à jour les attributs CO2 et tVOC avec les valeurs lues.
        """
        data = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_ALG_RESULT_DATA, 4)
        self.CO2 = (data[0] << 8) | data[1]
        self.tVOC = (data[2] << 8) | data[3]

    def run(self):
        """
        Boucle principale pour lire les données en continu.
        Affiche les niveaux de CO2 et de TVOC toutes les secondes.
        Utilisé pour des tests ou des diagnostics.
        """
        self.setup()
        while True:
            if self.data_available():
                self.read_logorithm_results()
                print(f"CO2: {self.CO2} ppm, TVOC: {self.tVOC} ppb")
            elif self.check_for_error():
                self.print_error()
            time.sleep(1)