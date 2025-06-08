# ==========================================================
# main.py
# Version : 1.0.1 (Ajout de documentation et commentaires structurants)
# Point d'entrée principal de l'application Modèle_MVC
# Initialise l'application Kivy, les modèles, vues et contrôleurs
# ==========================================================

import os
import sys
import kivy
from kivy.config import Config
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, FadeTransition

kivy.require("2.3.0")
Config.set("graphics", "fullscreen", "auto")  # S'assurer que l'application s'affiche en plein écran
Config.set("kivy", "log_level", "debug") # Définir le niveau de log sur debug pour plus de détails

# Définir explicitement le répertoire courant
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
print(f"Répertoire courant défini sur : {current_dir}")

# Ajoutez le dossier parent Modele_MVC au PYTHONPATH
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
print(f"PYTHONPATH mis à jour avec : {parent_dir}")

# Import des modules nécessaires
try:
    from suiviairmenuiserieapp.controleurs.controleur_principal import Controleur
    from suiviairmenuiserieapp.vues.vue_accueil import VueAccueil
    from suiviairmenuiserieapp.vues.vue_ecran1 import Ecran1
    print("Modules importés avec succès.")
except ModuleNotFoundError as e:
    print(f"Erreur d'importation : {e}")
    sys.exit(1)

class SuiviAirMenuiserie(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager = None
        self.controleur = None

    def build(self):
        """
        Configure et construit l'application.
        """
        # Vérifiez si le fichier demo3.kv existe
        kv_file = os.path.join(current_dir, "demo3.kv")
        if not os.path.exists(kv_file):
            print(f"Fichier KV introuvable : {kv_file}")
            sys.exit(1)
        print(f"Fichier KV trouvé : {kv_file}")

        # Charger explicitement le fichier demo3.kv
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
        print("🔄 Lancement de l'application SuiviAirMenuiserie...")
        SuiviAirMenuiserie().run()
        print("Application terminée avec succès.")
    except Exception as e:
        print(f"Erreur critique lors de l'exécution de l'application : {e}")
        sys.exit(1)

