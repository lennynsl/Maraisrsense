from testihm import *
from testsds import *

#installer les bibliothèques serial, pyserial, time, sds011, os et unihiker
#Pour les tests avec la classe unihiker, ensuite, nous utiliserons plutôt kivy



if __name__ == "__main__":  
    afficher = IHM()
    while True:
        try:
            capteur1 = GestionPM(port="/dev/sds011")
            break
        except:
            afficher.afficher_erreur()
        

    while True:    
        pm25, pm10 = capteur1.get_valeur()
        if pm25 is not None and pm10 is not None:
            afficher.afficher_valeurs(pm25, pm10)
        time.sleep(30)