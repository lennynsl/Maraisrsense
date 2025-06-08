# ==========================================================
# controleur_principal.py
# Contrôleur principal de l'application (orchestration MVC)
# ==========================================================
"""
Module : controleur_principal.py

Contrôleur principal de l'application.
- Orchestration entre modèles (logique métier) et vues (affichage).
- Toutes les interactions utilisateur passent par ce module.
- Navigation entre écrans, synchronisation des données, gestion des erreurs.

Fréquence d'échantillonnage : lecture du capteur toutes les 5 secondes (modifiable).
Envoi MQTT : toutes les 10 minutes (modifiable).
"""

from suiviairmenuiserieapp.modeles.modele_accueil import ModeleAccueil
from suiviairmenuiserieapp.modeles.modele_ecran1 import ModeleEcran1
from suiviairmenuiserieapp.vues.vue_accueil import VueAccueil
from suiviairmenuiserieapp.vues.vue_ecran1 import Ecran1
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.clock import Clock
import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

class Controleur:
    """
    Contrôleur principal qui fait le lien entre les modèles et les vues.
    Gère la navigation, les callbacks, la synchronisation des données et l'orchestration MVC.
    Assure la robustesse applicative et la conformité aux exigences industrielles.
    """

    def __init__(self, manager):
        """
        Initialise le contrôleur principal.
        :param manager: ScreenManager Kivy

        Fréquence d'échantillonnage et d'affichage :
        Les sondes mesurent et affichent les valeurs toutes les 5 secondes (modifiable).
        """
        self.manager = manager
        self.gestion_accueil = ModeleAccueil()
        self.gestion_ecran1 = ModeleEcran1(self)
        self.ihm_accueil = None
        self.ihm_ecran1 = None
        # Planification des mises à jour périodiques
        Clock.schedule_interval(self.mettre_a_jour_co2_tvoc, 5)
        Clock.schedule_interval(self.envoyer_mesures_mqtt_periodique, 600)

    def set_ihm_accueil(self, ihm_accueil):
        """
        Définit la référence à la vue accueil.
        :param ihm_accueil: instance de VueAccueil
        """
        try:
            self.ihm_accueil = ihm_accueil
            logger.info("ihm_accueil défini avec succès.")
        except Exception as exception:
            logger.error(f"Erreur lors de la définition de ihm_accueil : {exception}")

    def set_ihm_ecran1(self, ihm_ecran1):
        """
        Définit la référence à la vue écran 1 (adresse MAC).
        :param ihm_ecran1: instance de Ecran1
        """
        try:
            self.ihm_ecran1 = ihm_ecran1
            logger.info("ihm_ecran1 défini avec succès.")
        except Exception as exception:
            logger.error(f"Erreur lors de la définition de ihm_ecran1 : {exception}")

    def change_valeur(self):
        """
        Demande au modèle de changer la valeur et met à jour la vue.
        """
        new_valeur = self.gestion_accueil.change_valeur()
        self.ihm_accueil.changer_valeur(new_valeur)

    def change_ecran(self):
        """
        Passe à l'écran 1 (adresse MAC) et affiche l'adresse MAC.
        """
        try:
            self.manager.current = "ecran1"
            if self.ihm_ecran1:
                mac = self.gestion_ecran1.get_adresse_mac()
                self.ihm_ecran1.afficher_adresse_mac(mac)
                logger.info("Adresse MAC affichée sur l'écran 1.")
        except Exception as exception:
            logger.error(f"Erreur lors du changement d'écran : {exception}")

    def retour_accueil(self):
        """
        Revient à l'écran d'accueil.
        """
        self.manager.current = "accueil"

    def nouvelle_temperature(self, temp):
        """
        (Fonctionnalité non utilisée actuellement)
        Affiche la température sur l'écran 1.
        """
        self.ihm_ecran1.afficher_temperature(temp)

    def _mettre_a_jour_vue_accueil(self, seuils_mis_a_jour=False):
        """
        Met à jour la vue accueil avec les dernières valeurs, alertes et moyennes.
        :param seuils_mis_a_jour: booléen, True si les seuils ont été mis à jour récemment
        """
        co2, tvoc = self.gestion_accueil.get_co2_tvoc()
        alertes = self.gestion_accueil.verifier_seuils()
        moyenne_journaliere = self.gestion_accueil.get_moyenne_journaliere()
        if self.ihm_accueil is not None:
            self.ihm_accueil.afficher_co2_tvoc(
                co2, tvoc, alertes, moyenne_journaliere, seuils_mis_a_jour=seuils_mis_a_jour
            )
        else:
            logger.warning("ihm_accueil n'est pas défini. Assurez-vous que set_ihm_accueil a été appelé.")

    def mettre_a_jour_co2_tvoc(self, *args):
        """
        Met à jour les valeurs CO2/TVOC en lisant le capteur et rafraîchit la vue.
        """
        try:
            self.gestion_accueil.lire_donnees_capteur()
            self._mettre_a_jour_vue_accueil()
        except Exception as exception:
            logger.error(f"Erreur lors de la mise à jour CO2/TVOC : {exception}")

    def mettre_a_jour_affichage_seuils(self, *args):
        """
        Met à jour la vue avec les seuils courants et la dernière valeur lue (sans relire le capteur).
        """
        try:
            seuils_mis_a_jour = self.gestion_accueil.seuils_mis_a_jour
            self._mettre_a_jour_vue_accueil(seuils_mis_a_jour=seuils_mis_a_jour)
            if seuils_mis_a_jour:
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: self._reinitialiser_seuils_mis_a_jour(), 4)
        except Exception as exception:
            logger.error(f"Erreur lors de la mise à jour de l'affichage des seuils : {exception}")

    def _reinitialiser_seuils_mis_a_jour(self):
        """
        Réinitialise le flag de seuils mis à jour et rafraîchit l'affichage.
        """
        try:
            self.gestion_accueil.reset_seuils_mis_a_jour()
            self._mettre_a_jour_vue_accueil()
        except Exception as exception:
            logger.error(f"Erreur lors de la réinitialisation des seuils mis à jour : {exception}")

    def envoyer_mesures_mqtt_periodique(self, *args):
        """
        Envoie explicitement les dernières valeurs lues au broker MQTT toutes les 10 minutes.
        """
        try:
            self.gestion_accueil.envoyer_mesures_mqtt()
            logger.info("Envoi périodique des mesures au broker MQTT (toutes les 10 minutes).")
        except Exception as exception:
            logger.error(f"Erreur lors de l'envoi périodique MQTT : {exception}")

    def afficher_donnees_capteurs(self):
        """
        (Fonctionnalité désactivée) Affiche les données des capteurs supplémentaires.
        """
        pass

    def afficher_adresse_mac(self):
        """
        Récupère et affiche l'adresse MAC via la vue Ecran1.
        """
        try:
            mac = self.gestion_ecran1.get_adresse_mac()
            self.ihm_ecran1.afficher_adresse_mac(mac)
        except Exception as exception:
            logger.error(f"Erreur lors de l'affichage de l'adresse MAC : {exception}")