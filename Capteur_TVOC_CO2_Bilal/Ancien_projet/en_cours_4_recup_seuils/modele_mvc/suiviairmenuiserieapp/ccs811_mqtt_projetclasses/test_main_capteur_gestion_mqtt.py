from suiviairmenuiserieapp.ccs811_mqtt_projetclasses.ccs811 import CCS811
import time
from pinpong.board import Board
import paho.mqtt.client as mqtt

BROKER = "mqtt.marais2025.btssn.ovh"
PORT = 8883
CLIENT_ID = "root"
PASSWORD = "hyrome49#"


def main():
    """
    Lecture du capteur CCS811 et envoi périodique des mesures au broker MQTT.
    """
    Board("UNIHIKER").begin()

    client = mqtt.Client(CLIENT_ID)
    client.username_pw_set(username=CLIENT_ID, password=PASSWORD)
    client.connect(BROKER, PORT, 60)
    client.loop_start()

    try:
        print("Initialisation du capteur CCS811...")
        capteur = CCS811()
        capteur.setup()
        print("Capteur CCS811 initialisé avec succès.")

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

                time.sleep(5)
            except Exception as e:
                print(f"Erreur dans la boucle principale : {e}")
                time.sleep(5)
    except Exception as e:
        print(f"Erreur critique lors de l'initialisation : {e}")


if __name__ == "__main__":
    main()