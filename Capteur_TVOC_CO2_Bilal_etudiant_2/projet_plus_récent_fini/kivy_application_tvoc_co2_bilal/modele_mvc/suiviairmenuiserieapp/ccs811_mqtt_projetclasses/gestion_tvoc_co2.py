# ==========================================================
# gestion_tvoc_co2.py
# Version : 1.0.1 (Ajout de documentation et commentaires structurants)
# Module pour la gestion du capteur CCS811 (CO2/TVOC)
# ==========================================================
"""
Module : gestion_tvoc_co2.py

Ce module fournit une interface simplifiée pour lire les mesures du capteur CCS811 (CO2 et TVOC).
Il encapsule la logique d'initialisation et de lecture du capteur pour une utilisation dans le modèle métier.

Robustesse :
    Si le capteur n'est pas disponible ou une erreur survient, la méthode `obtenir_mesure` retourne `(None, None)` et journalise l'erreur, évitant ainsi tout crash de l'application.

Note : Toutes les opérations matérielles doivent être réalisées dans le thread principal pour éviter des comportements inattendus sur certains systèmes embarqués.

Utilisation typique :
    gestion = GestionTVOC_CO2()
    co2, tvoc = gestion.obtenir_mesure()
"""

from suiviairmenuiserieapp.ccs811_mqtt_projetclasses.ccs811 import CCS811
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

class GestionTVOC_CO2:
    """
    Classe pour interagir avec le capteur CCS811 et lire les niveaux de CO2 et TVOC.
    Fournit une interface simple pour le modèle.
    À utiliser dans le modèle pour obtenir les mesures du capteur.
    """

    def __init__(self):
        """
        Initialise et configure le capteur CCS811.
        Lève une exception si l'initialisation échoue.
        """
        try:
            logger.info("Initialisation du capteur CCS811...")
            self.capteur = CCS811()
            self.capteur.setup()
            logger.info("Capteur CCS811 correctement initialisé.")
        except Exception as exception:
            logger.error(f"Échec de l'initialisation du capteur CCS811 : {exception}")
            self.capteur = None
            raise Exception("Impossible d'initialiser le capteur CCS811.")

    def obtenir_mesure(self):
        """
        Récupère les dernières mesures de CO2 et TVOC du capteur CCS811.
        :return: tuple (CO2, TVOC) ou (None, None) si indisponible
        """
        try:
            if self.capteur.data_available():
                self.capteur.read_logorithm_results()
                return self.capteur.CO2, self.capteur.tVOC
            else:
                return None, None
        except Exception as exception:
            logger.error(f"Erreur lors de la lecture du capteur CCS811 : {exception}")
            return None, None