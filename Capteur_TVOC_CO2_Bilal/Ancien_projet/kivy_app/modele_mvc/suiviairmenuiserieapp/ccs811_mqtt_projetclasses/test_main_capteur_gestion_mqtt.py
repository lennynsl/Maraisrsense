from suiviairmenuiserieapp.ccs811_mqtt_projetclasses.ccs811 import CCS811
import time
from pinpong.board import Board
import paho.mqtt.client as mqtt

if __name__ == "__main__":
    # Initialise la carte UNIHIKER
    Board("UNIHIKER").begin()

    # Configuration des paramètres MQTT
    adresse_du_broker = "mqtt.marais2025.btssn.ovh"
    port_connexion = 8883
    client_identification = "root"
    mots_de_passe = "hyrome49#"

    # Initialisation du client MQTT
    client = mqtt.Client(client_identification)
    client.username_pw_set(username=client_identification, password=mots_de_passe)
    client.connect(adresse_du_broker, port_connexion, 60)
    client.loop_start()

    try:
        print("Initialisation du capteur CCS811...")
        capteur = CCS811()
        capteur.setup()
        print("Capteur CCS811 initialisé avec succès.")

        # Boucle principale pour lecture et envoi des mesures
        while True:
            try:
                if capteur.data_available():
                    capteur.read_logorithm_results()
                    co2 = capteur.CO2
                    tvoc = capteur.tVOC
                    print(f"CO2: {co2} ppm, TVOC: {tvoc} ppb")

                    # Publier les données sur le broker MQTT
                    client.publish("capteurs/co2", co2)
                    client.publish("capteurs/tvoc", tvoc)
                    print("Données publiées sur le broker MQTT.")
                else:
                    print("Pas de nouvelles données disponibles.")

                time.sleep(5)  # Pause entre les lectures
            except Exception as e:
                print(f"Erreur dans la boucle principale : {e}")
                time.sleep(5)  # Pause avant nouvelle tentative

    except Exception as e:
        print(f"Erreur critique lors de l'initialisation : {e}")