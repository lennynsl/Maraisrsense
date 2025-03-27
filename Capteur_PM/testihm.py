from unihiker import GUI
import time

#installer la classe unihiker

class IHM:
    def __init__(self):
        self.unihiker = GUI()
        self.unihiker.clear()
    
    def afficher_valeurs(self, pm25, pm10):
        self.unihiker.clear()
        texte = f"PM2.5: {pm25} µg/m³\nPM10: {pm10} µg/m³"
        self.unihiker.draw_text(text=texte, x=10, y=50, color="black", font_size=12)

    def afficher_erreur(self,message):
        # self.unihiker.clear()
        texte = f"Le capteur n'est pas connecté"
        self.unihiker.draw_text(text=texte, x=10, y=150, color="black", font_size=12)

if __name__ == "__main__":
    # Initialisation de l'IHM
    ihm = IHM()
    #Faire en sorte que ca affiche sur l'IHM un message d'erreur sans supprimer les valeurs d'avant
    print("🖥️ Test de l'interface graphique Unihiker...\n")

    # Affichage de valeurs de test
    valeurs_test = [(12.5, 25.8), (5.2, 15.4), (0.0, 0.0)]  # Liste de valeurs simulées
    valeur_erreur_test = [(None,None)]

    if valeur_erreur_test == None: 
        ihm.afficher_erreur()
    
    for pm25, pm10 in valeurs_test:
        print(f"📊 Affichage des valeurs : PM2.5 = {pm25} µg/m³, PM10 = {pm10} µg/m³")
        ihm.afficher_valeurs(pm25, pm10)
        time.sleep(2)  # Pause pour voir les valeurs à l'écran

    print("✅ Test terminé.")
