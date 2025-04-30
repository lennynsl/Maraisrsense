from CCS811 import CCS811
from GestionTVOC_CO2 import GestionTVOC_CO2
from Communication_MQTT_CCS811 import CommunicationCCS811
import time
from pinpong.board import Board

if __name__ == "__main__":
    # Initialise la carte UNIHIKER
    Board("UNIHIKER").begin()

    # Configuration des paramètres MQTT
    adresse_du_broker = "mqtt.marais2025.btssn.ovh"
    port_connexion = 8883
    client_identification = "root"
    mots_de_passe = "hyrome49#"

    try:
        print("🔄 Initialisation des composants...")

        # Initialisation du capteur CCS811
        gestion_capteur = GestionTVOC_CO2()

        # Initialisation du client MQTT
        communication = CommunicationCCS811(
            adresse_du_broker,
            port_connexion,
            client_identification,
            mots_de_passe
        )
        print("✅ Composants correctement initialisés.")

        # Boucle principale pour lecture et envoi des mesures
        while True:
            try:
                print("📊 Récupération des valeurs du capteur...")
                co2, tvoc = gestion_capteur.get_mesure()
                if co2 is not None and tvoc is not None:
                    print(f"✅ Données du capteur : CO2 = {co2} ppm, TVOC = {tvoc} ppb")

                    # Envoi des données via MQTT
                    communication.envoyer("CO2", co2)
                    communication.envoyer("TVOC", tvoc)
                    print("📤 Données envoyées au broker MQTT.")

                else:
                    print("⚠️ Aucune donnée disponible pour l'envoi.")

                # Pause entre les lectures
                time.sleep(5)
            except Exception as e:
                print(f"🚨 Erreur dans la boucle principale : {e}")
                time.sleep(5)  # Pause avant nouvelle tentative

    except Exception as e:
        print(f"🚨 Erreur critique lors de l'initialisation : {e}")