# ==========================================================
# vue_ecran1.py
# Vue pour l'affichage de l'adresse MAC et navigation retour.
# ==========================================================
"""
Module : vue_ecran1.py

Vue Kivy dédiée à l'affichage de l'adresse MAC et à la navigation retour.
Responsable uniquement de l'affichage et des callbacks associés.

Robustesse :
    - Si l'adresse MAC n'est pas disponible, un message explicite est affiché à l'utilisateur.

Utilisation :
    vue = Ecran1(controleur)
    vue.afficher_adresse_mac(mac)
"""

from kivy.uix.screenmanager import Screen
from kivy.clock import mainthread

class Ecran1(Screen):
    """
    Vue Kivy pour l'écran d'affichage de l'adresse MAC et des capteurs additionnels.
    Fournit les callbacks pour la navigation et l'affichage dynamique de l'adresse MAC.
    """
    def __init__(self, controleur, **kwargs):
        """
        Constructeur de la vue Ecran1.
        :param controleur: Référence au contrôleur principal
        :param kwargs: Arguments supplémentaires pour l'initialisation Kivy
        """
        super().__init__(**kwargs)
        self.controleur = controleur

    def on_retour(self):
        """
        Action pour revenir à l'écran d'accueil.
        """
        self.controleur.retour_accueil()

    @mainthread
    def afficher_adresse_mac(self, mac):
        """
        Affiche l'adresse MAC sur l'écran (exécuté sur le thread principal).
        :param mac: Adresse MAC à afficher
        """
        if "MAC" in self.ids:
            self.ids.MAC.text = mac if mac else "Adresse MAC indisponible"