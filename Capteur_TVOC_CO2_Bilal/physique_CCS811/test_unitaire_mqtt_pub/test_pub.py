import unittest
import sys
import os

# Ajoute le dossier parent au path pour l'import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Mosquitto_pub_marais import ClientMQTT

class TestMQTTPublish(unittest.TestCase):
    def setUp(self):
        self.adresse_broker = "mqtt.marais2025.btssn.ovh"
        self.port = 8883
        self.identifiant = "root"
        self.mot_de_passe = "hyrome49#"
        self.client = ClientMQTT(self.adresse_broker, self.port, self.identifiant, self.mot_de_passe)

    def test_envoyer_tvoc(self):
        try:
            self.client.envoyer("test_unitaire/tvoc", "10 ppb")
        except Exception as e:
            self.fail(f"envoyer a levé une exception : {e}")

    def test_envoyer_co2(self):
        try:
            self.client.envoyer("test_unitaire/co2", "640 ppm")
        except Exception as e:
            self.fail(f"envoyer a levé une exception : {e}")

if __name__ == "__main__":
    unittest.main()
