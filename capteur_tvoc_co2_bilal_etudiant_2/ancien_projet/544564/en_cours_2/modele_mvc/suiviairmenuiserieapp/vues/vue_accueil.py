# ==========================================================
# vue_accueil.py
# Version : 1.2.0 (Affichage dynamique selon capteur, adaptation multi-capteur, documentation détaillée)
# Vue principale pour l'affichage des mesures sur l'écran d'accueil
# du projet Modèle_MVC (architecture MVC)
# ==========================================================

from kivy.uix.screenmanager import Screen  # Pour la gestion des écrans Kivy
from kivy.clock import mainthread         # Pour exécuter sur le thread principal Kivy

class VueAccueil(Screen):
    """
    Vue Kivy pour l'écran d'accueil.
    Affiche dynamiquement les valeurs selon le capteur branché (CCS811 ou SDS011).
    """
    def __init__(self, controleur, **kwargs):
        super().__init__(**kwargs)
        self.controleur = controleur

    def on_change_valeur(self):
        """
        Action lors du changement de valeur (bouton ou événement).
        """
        self.controleur.change_valeur()

    def on_change_ecran(self):
        """
        Action pour changer d'écran (ex : bouton Adresse MAC).
        """
        self.controleur.change_ecran()

    def changer_valeur(self, valeur):
        """
        Met à jour l'affichage d'un compteur ou d'une valeur.
        """
        if "cpt" in self.ids:
            self.ids.cpt.text = str(valeur)

    @mainthread
    def afficher_co2_tvoc(self, val1, val2, alertes, moyenne_jour=None):
        """
        Met à jour dynamiquement les labels pour afficher les valeurs selon le capteur.
        :param val1: Valeur 1 (CO2 ou PM2.5)
        :param val2: Valeur 2 (TVOC ou PM10)
        :param alertes: Dictionnaire contenant les alertes
        :param moyenne_jour: Dictionnaire {"co2": float, "tvoc": float, ...}
        """
        # Détection du type de capteur par les clés d'alertes
        if "co2" in alertes:
            # CO2 et TVOC
            co2_color = (0, 1, 0, 1) if alertes["co2"] == "normal" else (1, 0, 0, 1)
            tvoc_color = (0, 1, 0, 1) if alertes["tvoc"] == "normal" else (1, 0, 0, 1)

            # Mettre à jour le titre et la valeur CO2
            if "titre_co2" in self.ids:
                self.ids.titre_co2.color = co2_color
            if "valeur1" in self.ids:
                self.ids.valeur1.text = f"{val1} ppm"
                self.ids.valeur1.color = co2_color
            if "indicateur_co2" in self.ids:
                if alertes["co2"] == "normal":
                    self.ids.indicateur_co2.source = "img/fleche_vert_haut.png"
                else:
                    self.ids.indicateur_co2.source = "img/fleche_rouge_bas.png"

            # Mettre à jour le titre et la valeur TVOC
            if "titre_tvoc" in self.ids:
                self.ids.titre_tvoc.color = tvoc_color
            if "valeur2" in self.ids:
                self.ids.valeur2.text = f"{val2} ppb"
                self.ids.valeur2.color = tvoc_color
            if "indicateur_tvoc" in self.ids:
                if alertes["tvoc"] == "normal":
                    self.ids.indicateur_tvoc.source = "img/fleche_vert_haut.png"
                else:
                    self.ids.indicateur_tvoc.source = "img/fleche_rouge_bas.png"

                # Masquer le texte d'état
                if "alerte1" in self.ids:
                    self.ids.alerte1.text = ""
                if "alerte2" in self.ids:
                    self.ids.alerte2.text = ""

            # Affichage d'une alerte si le capteur est déconnecté
            if "alerte_capteur" in self.ids:
                if alertes.get("capteur") == "deconnecte":
                    self.ids.alerte_capteur.text = "Capteur CCS811 déconnecté !"
                    self.ids.alerte_capteur.color = (1, 0, 0, 1)
                else:
                    self.ids.alerte_capteur.text = ""

            # Affichage des moyennes journalières avec nombre de mesures
            if moyenne_jour:
                if "moyenne_co2" in self.ids:
                    self.ids.moyenne_co2.text = moyenne_jour.get("co2", "moy : 0 ppm")
                    self.ids.moyenne_co2.color = (0.1, 0.4, 1, 1)  # Bleu vif
                if "moyenne_tvoc" in self.ids:
                    self.ids.moyenne_tvoc.text = moyenne_jour.get("tvoc", "moy : 0 ppb")
                    self.ids.moyenne_tvoc.color = (0.1, 0.4, 1, 1)  # Bleu vif
        elif "pm25" in alertes:
            # PM2.5 et PM10
            pm25_color = (0, 1, 0, 1) if alertes["pm25"] == "normal" else (1, 0, 0, 1)
            pm10_color = (0, 1, 0, 1) if alertes["pm10"] == "normal" else (1, 0, 0, 1)
            if "titre_co2" in self.ids:
                self.ids.titre_co2.text = "PM2.5"
                self.ids.titre_co2.color = pm25_color
            if "valeur1" in self.ids:
                self.ids.valeur1.text = f"{val1} µg/m³"
                self.ids.valeur1.color = pm25_color
            if "indicateur_co2" in self.ids:
                self.ids.indicateur_co2.source = "img/fleche_vert_haut.png" if alertes["pm25"] == "normal" else "img/fleche_rouge_bas.png"
            if "titre_tvoc" in self.ids:
                self.ids.titre_tvoc.text = "PM10"
                self.ids.titre_tvoc.color = pm10_color
            if "valeur2" in self.ids:
                self.ids.valeur2.text = f"{val2} µg/m³"
                self.ids.valeur2.color = pm10_color
            if "indicateur_tvoc" in self.ids:
                self.ids.indicateur_tvoc.source = "img/fleche_vert_haut.png" if alertes["pm10"] == "normal" else "img/fleche_rouge_bas.png"

                # Masquer le texte d'état
                if "alerte1" in self.ids:
                    self.ids.alerte1.text = ""
                if "alerte2" in self.ids:
                    self.ids.alerte2.text = ""

            # Affichage d'une alerte si le capteur est déconnecté
            if "alerte_capteur" in self.ids:
                if alertes.get("capteur") == "deconnecte":
                    self.ids.alerte_capteur.text = "Capteur CCS811 déconnecté !"
                    self.ids.alerte_capteur.color = (1, 0, 0, 1)
                else:
                    self.ids.alerte_capteur.text = ""

            # Affichage des moyennes journalières avec nombre de mesures
            if moyenne_jour:
                if "moyenne_co2" in self.ids:
                    self.ids.moyenne_co2.text = moyenne_jour.get("co2", "moy : 0 ppm")
                    self.ids.moyenne_co2.color = (0.1, 0.4, 1, 1)  # Bleu vif
                if "moyenne_tvoc" in self.ids:
                    self.ids.moyenne_tvoc.text = moyenne_jour.get("tvoc", "moy : 0 ppb")
                    self.ids.moyenne_tvoc.color = (0.1, 0.4, 1, 1)  # Bleu vif

    def on_update_co2_tvoc(self):
        """
        Action pour demander la mise à jour des valeurs capteurs.
        """
        self.controleur.mettre_a_jour_co2_tvoc()

    def on_afficher_capteurs(self):
        """
        Affiche les données des capteurs supplémentaires.
        """
        self.controleur.afficher_donnees_capteurs()

    def on_afficher_adresse_mac(self):
        """
        Affiche l'adresse MAC de l'appareil.
        """
        self.controleur.afficher_adresse_mac()