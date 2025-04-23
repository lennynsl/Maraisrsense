import time
import paho.mqtt.client as mqtt
from pinpong.board import Board
from CCS811 import CCS811 

class CCS811MQTT:
    """
    Une classe pour transmettre les données collectés dans la zone concernée du capteur CCS811 via MQTT en utilisant une instance de CCS811. 
    Donc sans créer la globalité du script de base du Capteur CCS811.
    """

    def __init__(self, ccs811_instance, broker="localhost", port=1883, topic="capteur/CCS811_data"):
        """
        Initialise la classe CCS811MQTT.
        - ccs811_instance: instance de la classe CCS811.
        - broker: adresse du serveur MQTT.
        - port: port du serveur MQTT.
        - topic: sujet MQTT pour publier les données.
        """
        self.ccs811 = ccs811_instance
        self.topic = topic

        # Configuration du service client MQTT.
        self.client = mqtt.Client()
        self.client.connect(broker, port)
        self.client.loop_start()

    def publish_data(self):
        """
        Publie les données du capteur sur le serveur MQTT.
        """
        message = {"CO2": self.ccs811.CO2, "TVOC": self.ccs811.tVOC}
        self.client.publish(self.topic, str(message))

    def run(self):
        """
        Boucle principale pour lire les données depuis l'instance CCS811 et les publier via MQTT.
        """
        self.ccs811.setup()  # Initialise le capteur CCS811.
        while True:
            if self.ccs811.data_available():
                self.ccs811.read_logorithm_results()
                self.publish_data()
                print(f"CO2: {self.ccs811.CO2} ppm, TVOC: {self.ccs811.tVOC} ppb")
            elif self.ccs811.check_for_error():
                self.ccs811.print_error()
            time.sleep(1)

# Exemple d'utilisation.
if __name__ == "__main__":
    Board("UNIHIKER").begin()  # Initialise la carte UniHiker.
    capteur = CCS811()  # Crée une instance de la classe CCS811.
    capteur_mqtt = CCS811MQTT(capteur)  # Passe l'instance à CCS811MQTT.
    capteur_mqtt.run()