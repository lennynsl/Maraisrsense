from unihiker import GUI
import time

# Classe pour gérer l'affichage des valeurs PM2.5 et PM10 sur l'interface Unihiker
class IHM:
    def __init__(self):
        """Initialise l'interface graphique en nettoyant l'écran."""
        self.unihiker = GUI()  # Création de l'instance GUI pour gérer l'affichage
        self.unihiker.clear()  # Efface l'écran au démarrage
    
    def afficher_valeurs(self, pm25, pm10):
        """Affiche les valeurs PM2.5 et PM10 sur l'écran de l'Unihiker."""
        self.unihiker.clear()  # Efface l'écran avant d'afficher les nouvelles valeurs
        texte = f"PM2.5: {pm25} µg/m³\nPM10: {pm10} µg/m³"
        self.unihiker.draw_text(text=texte, x=10, y=50, color="black", font_size=12)  # Affiche le texte

    def afficher_erreur(self, message):
        """Affiche un message d'erreur sur l'écran sans effacer les valeurs précédentes."""
        texte = "Le capteur n'est pas connecté"
        self.unihiker.draw_text(text=texte, x=10, y=150, color="red", font_size=12)  # Affichage du message d'erreur en rouge

# Programme principal
if __name__ == "__main__":
    # Initialisation de l'IHM
    ihm = IHM()
    print("🖥️ Test de l'interface graphique Unihiker...\n")

    # Liste de valeurs simulées pour les tests
    valeurs_test = [(12.5, 25.8), (5.2, 15.4), (0.0, 0.0)]  # Valeurs normales
    valeur_erreur_test = (None, None)  # Simule une erreur de capteur

    # Vérification d'une erreur et affichage du message correspondant
    if valeur_erreur_test == (None, None): 
        ihm.afficher_erreur("Erreur de connexion au capteur")
    
    # Affichage des valeurs simulées sur l'écran Unihiker
    for pm25, pm10 in valeurs_test:
        print(f"📊 Affichage des valeurs : PM2.5 = {pm25} µg/m³, PM10 = {pm10} µg/m³")
        ihm.afficher_valeurs(pm25, pm10)
        time.sleep(2)  # Pause pour voir les valeurs affichées

    print("✅ Test terminé.")