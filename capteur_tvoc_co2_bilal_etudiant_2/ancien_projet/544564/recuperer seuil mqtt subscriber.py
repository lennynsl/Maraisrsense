import paho.mqtt.client as mqtt
import pymysql
import ssl
from datetime import datetime


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connexion au broker MQTT réussie")
        client.subscribe("#")  # Abonnement à tous les topics
        print("Abonné à tous les topics. En attente de messages...")
    else:
        print(f"Erreur de connexion MQTT, code: {rc}")


def on_message(client, userdata, msg):
    db = userdata["db"]
    cursor = db.cursor()

    topic = msg.topic
    print(f"\nMessage reçu sur le topic : {topic}")

    try:
        # Topic attendu : identifiant_sonde/nom_typemesure/nom_unite/valeur
        identifiant_sonde, nom_typemesure, nom_unite, valeur_topic = topic.split("/")
        valeur = float(valeur_topic)
    except Exception:
        print("Erreur : topic non conforme. Format attendu : identifiant_sonde/nom_typemesure/nom_unite/valeur")
        return

    try:
        # Chercher nom_emplacement de la sonde
        cursor.execute("""
            SELECT E.nom_emplacement
            FROM Sonde S
            JOIN Emplacement E ON S.id_emplacement = E.id_emplacement
            WHERE S.identifiant_sonde = %s
        """, (identifiant_sonde,))
        result = cursor.fetchone()

        if result is None:
            print("Erreur : sonde non trouvée dans la base de données.")
            return

        nom_emplacement = result["nom_emplacement"]
        print(f"Nom emplacement trouvé : {nom_emplacement}")

        # Insertion avec SELECT imbriqué
        cursor.execute("""
            INSERT INTO Mesure (horodatage_mesure, valeur_mesure, id_typemesure, id_emplacement)
            SELECT NOW(), %s, T.id_typemesure, E.id_emplacement
            FROM TypeMesure T, Emplacement E
            WHERE T.nom_typemesure = %s AND E.nom_emplacement = %s
        """, (valeur, nom_typemesure, nom_emplacement))

        db.commit()
        print("Insertion en BDD réussie.")

    except pymysql.MySQLError as e:
        print(f"Erreur lors de l'insertion en BDD : {e.args[0]} - {e.args[1]}")


def main():
    print("Début connexion")

    try:
        db = pymysql.connect(
            host="mqtt.marais2025.btssn.ovh",
            user="root",
            password="hyrome49#",
            database="MaraisRsite",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )
        print("Connexion à la base de données réussie", flush=True)
    except pymysql.MySQLError as e:
        print(f"Erreur de connexion à la base de données : {e.args[0]} - {e.args[1]}")
        return

    client = mqtt.Client(userdata={"db": db})
    client.username_pw_set("root", "hyrome49#")
    client.tls_set(cert_reqs=ssl.CERT_NONE)
    client.tls_insecure_set(True)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("mqtt.marais2025.btssn.ovh", 8883, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()
