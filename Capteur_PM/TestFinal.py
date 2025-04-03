from IHM import *  # Importation de la classe d'affichage IHM
from GestionPM import *  # Importation de la gestion du capteur SDS011

# Nécessite l'installation des bibliothèques : serial, pyserial, time, sds011, os et unihiker
# À terme, les tests avec la classe Unihiker seront remplacés par Kivy

if __name__ == "__main__":  
    afficher = IHM()  # Création d'une instance de l'interface graphique
    
    # Tentative d'initialisation du capteur SDS011 avec gestion des erreurs
    while True:
        try:
            capteur1 = GestionPM(port="/dev/sds011")  # Connexion au capteur
            break  # Sortie de la boucle si la connexion réussit
        except:
            afficher.afficher_erreur()  # Affichage d'un message d'erreur si le capteur n'est pas détecté
    
    # Boucle principale pour récupérer et afficher les valeurs du capteur
    while True:    
        pm25, pm10 = capteur1.get_valeur()  # Lecture des valeurs PM2.5 et PM10
        if pm25 is not None and pm10 is not None:
            afficher.afficher_valeurs(pm25, pm10)  # Affichage des valeurs sur l'interface graphique
        time.sleep(30)  # Pause de 30 secondes avant la prochaine mesure
