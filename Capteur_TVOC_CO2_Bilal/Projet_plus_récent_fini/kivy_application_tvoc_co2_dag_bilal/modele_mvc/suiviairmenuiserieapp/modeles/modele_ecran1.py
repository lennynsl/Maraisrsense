# ==========================================================
# modele_ecran1.py
# Modèle pour la gestion des données de l'écran 1 (adresse MAC)
# ==========================================================
"""
Module : modele_ecran1.py

Ce module fournit le modèle pour la gestion de l'adresse MAC, séparant la logique système de l'affichage.
Permet une meilleure conformité à l'architecture MVC.
À utiliser dans le contrôleur pour fournir l'adresse MAC à la vue.

Robustesse :
    - Si la récupération de l'adresse MAC échoue, la valeur "Indisponible" est retournée et l'erreur est journalisée.

Utilisation :
    modele = ModeleEcran1(controleur)
    mac = modele.get_adresse_mac()
"""

from getmac import get_mac_address

class ModeleEcran1:
    """
    Modèle qui permet de gérer les données de l'écran1 (adresse MAC).
    Les données proviennent de MQTT ou du système.
    """

    def __init__(self, controleur):
        """
        Initialise le modèle pour l'écran 1.
        :param controleur: Référence au contrôleur principal
        """
        self.controleur = controleur

    def get_adresse_mac(self):
        """
        Retourne l'adresse MAC de la machine.
        Utilise la bibliothèque getmac pour obtenir l'adresse réseau.
        :return: str, adresse MAC ou "Indisponible" si non trouvée
        """
        try:
            mac = get_mac_address()
            return mac if mac else "Indisponible"
        except Exception as e:
            print(f"Erreur lors de la récupération de l'adresse MAC : {e}")
            return "Indisponible"