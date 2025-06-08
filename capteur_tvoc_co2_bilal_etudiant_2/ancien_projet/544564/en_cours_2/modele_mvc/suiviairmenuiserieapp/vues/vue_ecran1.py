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

    @mainthread
    def afficher_donnees_capteur(self, capteur_id, co2, tvoc):
        """
        Affiche les données d'un capteur supplémentaire.
        """
        layout = self.ids.capteurs_layout
        label_co2 = self.ids.get(f"capteur_{capteur_id}_co2")
        label_tvoc = self.ids.get(f"capteur_{capteur_id}_tvoc")

        if not label_co2:
            label_co2 = Label(id=f"capteur_{capteur_id}_co2", font_size='16sp')
            layout.add_widget(label_co2)

        if not label_tvoc:
            label_tvoc = Label(id=f"capteur_{capteur_id}_tvoc", font_size='16sp')
            layout.add_widget(label_tvoc)

        label_co2.text = f"Capteur {capteur_id} - CO2 : {co2} ppm"
        label_tvoc.text = f"Capteur {capteur_id} - TVOC : {tvoc} ppb"