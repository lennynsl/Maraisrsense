# ==========================================================
# vue_ecran1.py
# Version : 1.0.1 (Ajout de documentation et commentaires structurants)
# Vue pour l'affichage de l'adresse MAC et des capteurs supplémentaires
# ==========================================================

from kivy.uix.screenmanager import Screen  # Gestion des écrans Kivy
from kivy.clock import mainthread         # Pour exécuter sur le thread principal
from kivy.uix.label import Label          # Pour créer dynamiquement des labels

class Ecran1(Screen):
    """
    Vue Kivy pour l'écran d'affichage de l'adresse MAC et des capteurs additionnels.
    """
    def __init__(self, controleur, **kwargs):
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
        Affiche l'adresse MAC sur l'écran.
        :param mac: Adresse MAC à afficher
        """
        if "MAC" in self.ids:
            self.ids.MAC.text = mac if mac else "Adresse MAC indisponible"