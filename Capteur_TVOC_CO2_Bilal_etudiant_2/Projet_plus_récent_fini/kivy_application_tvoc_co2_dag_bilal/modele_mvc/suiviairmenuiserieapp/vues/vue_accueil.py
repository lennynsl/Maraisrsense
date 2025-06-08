# ==========================================================
# vue_accueil.py
# Vue principale pour l'affichage des mesures sur l'écran d'accueil
# ==========================================================
"""
Module : vue_accueil.py

Vue principale Kivy pour l'affichage dynamique des mesures, alertes et navigation.
Responsable uniquement de l'affichage et des callbacks utilisateur.

Séparation stricte :
    - Cette vue ne contient aucune logique métier, uniquement des callbacks et de l'affichage.
    - Toute modification des valeurs affichées doit passer par le contrôleur.
"""

from kivy.uix.screenmanager import Screen
from kivy.clock import mainthread

class VueAccueil(Screen):
    """
    Vue Kivy pour l'écran d'accueil.
    Affiche dynamiquement les valeurs du capteur CCS811 (CO2/TVOC).
    Fournit les callbacks pour la navigation et la mise à jour des valeurs.
    """

    def __init__(self, controleur, **kwargs):
        """
        Constructeur de la vue d'accueil.
        :param controleur: Référence au contrôleur principal (MVC)
        :param kwargs: Arguments supplémentaires pour l'initialisation Kivy
        """
        super().__init__(**kwargs)
        self.controleur = controleur

    def on_change_valeur(self):
        """
        Callback appelé lors d'un changement de valeur (ex: bouton).
        Demande au contrôleur de gérer le changement de valeur.
        """
        self.controleur.change_valeur()

    def on_change_ecran(self):
        """
        Callback appelé lors d'un changement d'écran (ex: bouton Adresse MAC).
        Demande au contrôleur de basculer vers l'écran suivant (adresse MAC).
        """
        self.controleur.change_ecran()

    def changer_valeur(self, valeur):
        """
        Met à jour dynamiquement l'affichage d'un compteur ou d'une valeur.
        :param valeur: Nouvelle valeur à afficher dans le widget 'cpt'
        """
        if "cpt" in self.ids:
            self.ids.cpt.text = str(valeur)

    @mainthread
    def afficher_co2_tvoc(self, val1, val2, alertes, moyenne_jour=None, seuils_mis_a_jour=False):
        """
        Met à jour tous les labels et indicateurs de la vue d'accueil selon les valeurs reçues.
        Cette méthode est thread-safe grâce au décorateur @mainthread.

        :param val1: Valeur du CO2 (int ou float, en ppm)
        :param val2: Valeur du TVOC (int ou float, en ppb)
        :param alertes: Dictionnaire d'états d'alerte pour chaque mesure (ex: {"co2": "normal", ...})
        :param moyenne_jour: Dictionnaire des moyennes journalières (optionnel)
        :param seuils_mis_a_jour: Booléen, True si les seuils ont été mis à jour récemment
        """
        def couleur_alerte(etat):
            """
            Retourne la couleur RGBA selon l'état d'alerte.
            Vert si normal, orange si attention, rouge sinon.
            """
            if etat == "normal":
                return (0, 1, 0, 1)
            elif etat == "attention":
                return (1, 0.7, 0, 1)
            else:
                return (1, 0, 0, 1)

        co2_color = couleur_alerte(alertes["co2"])
        tvoc_color = couleur_alerte(alertes["tvoc"])

        # Bloc CO2
        if "titre_co2" in self.ids:
            self.ids.titre_co2.color = co2_color
        if "valeur1" in self.ids:
            self.ids.valeur1.text = f"{val1} ppm"
            self.ids.valeur1.color = co2_color
        if "indicateur_co2" in self.ids:
            self.ids.indicateur_co2.source = (
                "img/fleche_vert_haut.png" if alertes["co2"] == "normal" else "img/fleche_rouge_bas.png"
            )

        # Bloc TVOC
        if "titre_tvoc" in self.ids:
            self.ids.titre_tvoc.color = tvoc_color
        if "valeur2" in self.ids:
            self.ids.valeur2.text = f"{val2} ppb"
            self.ids.valeur2.color = tvoc_color
        if "indicateur_tvoc" in self.ids:
            self.ids.indicateur_tvoc.source = (
                "img/fleche_vert_haut.png" if alertes["tvoc"] == "normal" else "img/fleche_rouge_bas.png"
            )

        # Effacement des alertes additionnelles (si elles existent)
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

        # Affichage des moyennes journalières si disponibles
        if moyenne_jour:
            if "moyenne_co2" in self.ids:
                self.ids.moyenne_co2.text = moyenne_jour.get("co2", "moy : 0 ppm")
                self.ids.moyenne_co2.color = (0.1, 0.4, 1, 1)
            if "moyenne_tvoc" in self.ids:
                self.ids.moyenne_tvoc.text = moyenne_jour.get("tvoc", "moy : 0 ppb")
                self.ids.moyenne_tvoc.color = (0.1, 0.4, 1, 1)

    def on_update_co2_tvoc(self):
        """
        Callback pour demander la mise à jour des valeurs capteurs.
        Appelle la méthode correspondante du contrôleur.
        """
        self.controleur.mettre_a_jour_co2_tvoc()

    def on_afficher_capteurs(self):
        """
        Callback pour afficher les données des capteurs supplémentaires.
        Appelle la méthode correspondante du contrôleur.
        """
        self.controleur.afficher_donnees_capteurs()

    def on_afficher_adresse_mac(self):
        """
        Callback pour afficher l'adresse MAC de l'appareil.
        Appelle la méthode correspondante du contrôleur.
        """
        self.controleur.afficher_adresse_mac()