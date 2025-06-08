# ==========================================================
# controleur_principal.py
# Version : 1.0.1 (Ajout de documentation et commentaires structurants)
# Contrôleur principal du projet Modèle_MVC (architecture MVC)
# Gère la logique entre modèles et vues
# ==========================================================

from suiviairmenuiserieapp.modeles.modele_accueil import ModeleAccueil
from suiviairmenuiserieapp.modeles.modele_ecran1 import ModeleEcran1
from suiviairmenuiserieapp.vues.vue_accueil import VueAccueil
from suiviairmenuiserieapp.vues.vue_ecran1 import Ecran1
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.clock import Clock
import datetime

class Controleur:
    """
    Contrôleur principal qui fait le lien entre les modèles et les vues.
    """

    def __init__(self,manager):
        # Sauvegarde du manager d'écran
        self.manager=manager
        #Création des modèles
        self.gestion_accueil=ModeleAccueil()
        self.gestion_ecran1=ModeleEcran1(self)
        # Références aux vues
        self.ihm_accueil = None  # Initialisation par défaut
        self.ihm_ecran1 = None  # Initialisation par défaut
        # Mise à jour automatique des données CO2 et TVOC toutes les 8 secondes
        Clock.schedule_interval(self.mettre_a_jour_co2_tvoc, 8)

    #permet d'avoir des références sur les vues
    def set_ihm_accueil(self, ihm_accueil):
        self.ihm_accueil = ihm_accueil
        print("ihm_accueil défini avec succès.")

    def set_ihm_ecran1(self, ihm_ecran1):
        self.ihm_ecran1 = ihm_ecran1
        print("ihm_ecran1 défini avec succès.")


    def change_valeur(self):
        #on demande au modele ce qu'il faut faire
        new_valeur=self.gestion_accueil.change_valeur()
        self.ihm_accueil.changer_valeur(new_valeur)

    def change_ecran(self):
        """
        Changement d'écran vers l'écran 1.
        """
        self.manager.current = "ecran1"
        if self.ihm_ecran1:
            mac = self.gestion_ecran1.get_adresse_mac()
            self.ihm_ecran1.afficher_adresse_mac(mac)
            print("Adresse MAC")

    def retour_accueil(self):
        self.manager.current="accueil"
    
    def nouvelle_temperature(self,temp):
        self.ihm_ecran1.afficher_temperature(temp)

    def mettre_a_jour_co2_tvoc(self, *args):
        """
        Lit les données du capteur via le modèle et met à jour la vue.
        """
        self.gestion_accueil.lire_donnees_capteur()
        co2, tvoc = self.gestion_accueil.get_co2_tvoc()
        alertes = self.gestion_accueil.verifier_seuils()
        moyenne_jour = self.gestion_accueil.get_moyenne_journaliere()
        print(f"Alertes : {alertes}")  # Affiche les alertes dans la console

        if self.ihm_accueil is not None:
            self.ihm_accueil.afficher_co2_tvoc(co2, tvoc, alertes, moyenne_jour)
        else:
            print("ihm_accueil n'est pas défini. Assurez-vous que set_ihm_accueil a été appelé.")

    def afficher_donnees_capteurs(self):
        """
        Affiche les données des capteurs supplémentaires.
        """
        capteurs = self.gestion_accueil.get_tous_les_capteurs()
        for capteur_id, donnees in capteurs.items():
            co2, tvoc = donnees["co2"], donnees["tvoc"]
            if self.ihm_ecran1:
                self.ihm_ecran1.afficher_donnees_capteur(capteur_id, co2, tvoc)

    def afficher_adresse_mac(self):
        """
        Récupère et affiche l'adresse MAC via la vue Ecran1.
        """
        mac = self.gestion_ecran1.get_adresse_mac()
        self.ihm_ecran1.afficher_adresse_mac(mac)