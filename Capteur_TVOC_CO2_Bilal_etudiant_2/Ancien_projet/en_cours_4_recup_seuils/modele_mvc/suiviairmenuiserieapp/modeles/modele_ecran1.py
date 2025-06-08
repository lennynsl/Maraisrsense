# ==========================================================
# modele_ecran1.py
# Version : 1.0.1 (Ajout de documentation et commentaires structurants)
# Modèle pour la gestion des données de l'écran 1 (adresse MAC)
# ==========================================================

from getmac import get_mac_address

class ModeleEcran1:
    """
    Modèle qui permet de gérer les données de l'écran1.
    Les données proviennent de MQTT ou du système.
    """
    def __init__(self, controleur):
        self.controleur = controleur

    def get_adresse_mac(self):
        """
        Retourne l'adresse MAC de la machine.
        """
        try:
            mac = get_mac_address()
            return mac if mac else "Indisponible"
        except Exception as e:
            print(f"Erreur lors de la récupération de l'adresse MAC : {e}")
            return "Indisponible"