# ==========================================================
# main.py
# Point d'entrée principal de l'application Kivy (MVC)
# ==========================================================
"""
Module : main.py

Point d'entrée principal de l'application Kivy.
- Configure l'environnement et le répertoire courant pour garantir le bon chargement des ressources.
- Modifie le PYTHONPATH pour permettre l'import des modules internes.
- Initialise le contrôleur principal, les vues et le gestionnaire d'écrans.
- Respecte l'architecture MVC pour une séparation claire des responsabilités.

Ce script assure l'initialisation complète de l'application et la robustesse du démarrage.
"""

import os
import sys
import kivy
from kivy.config import Config
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, FadeTransition
import logging

kivy.require("2.3.0")
Config.set("graphics", "fullscreen", "auto")  # Application en plein écran
Config.set("kivy", "log_level", "debug")       # Niveau de log détaillé

# Définir explicitement le répertoire courant pour le chargement des ressources
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
logging.info(f"Répertoire courant défini sur : {current_dir}")

# Ajout du dossier parent au PYTHONPATH pour l'import des modules internes
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
logging.info(f"PYTHONPATH mis à jour avec : {parent_dir}")

# === IMPORTS MVC ===
from suiviairmenuiserieapp.controleurs.controleur_principal import Controleur
from suiviairmenuiserieapp.vues.vue_accueil import VueAccueil
from suiviairmenuiserieapp.vues.vue_ecran1 import Ecran1

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

class SuiviAirMenuiserie(App):
    """
    Application principale Kivy pour le suivi de la qualité de l'air.
    Initialise le gestionnaire d'écrans, le contrôleur principal et les vues.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager = None
        self.controleur = None

    def build(self):
        """
        Configure et construit l'application.
        Charge le fichier KV, crée les écrans et configure le contrôleur.
        """
        kv_file = os.path.join(current_dir, "demo3.kv")
        if not os.path.exists(kv_file):
            logger.error(f"Fichier KV introuvable : {kv_file}")
            sys.exit(1)
        logger.info(f"Fichier KV trouvé : {kv_file}")

        Builder.load_file(kv_file)

        # Création du gestionnaire d'écrans avec une transition fluide
        self.manager = ScreenManager(transition=FadeTransition())

        # Création du contrôleur principal
        self.controleur = Controleur(self.manager)

        # Création et ajout des écrans
        ihm_accueil = VueAccueil(self.controleur, name='accueil')
        ihm_ecran1 = Ecran1(self.controleur, name='ecran1')
        self.manager.add_widget(ihm_accueil)
        self.manager.add_widget(ihm_ecran1)

        # Configuration des références dans le contrôleur
        self.controleur.set_ihm_accueil(ihm_accueil)
        self.controleur.set_ihm_ecran1(ihm_ecran1)

        return self.manager

if __name__ == "__main__":
    try:
        logger.info("Lancement de l'application SuiviAirMenuiserie...")
        SuiviAirMenuiserie().run()
        logger.info("Application terminée avec succès.")
    except Exception as e:
        logger.critical(f"Erreur critique lors de l'exécution de l'application : {e}")
        sys.exit(1)

