from paramètres_connexion import  MQTTClient 

# Choisir le message à envoyer
def choose_message(message):
    if message == "on":
        return "on"
    elif message == "off":
        return "off"
    elif message == "toggle":
        return "toggle"
    else:
        return None

# Paramètres de connexion au broker MQTT
mqtt_client = MQTTClient(
    broker="mqtt.marais2025.btssn.ovh",
    port=8883,
    username="root",
    password="hyrome49#"
)

mqtt_client.connect()

# Boucle de commande utilisateur
try:
    while True:
        message = input("Entrez une commande (on, off, toggle, quit): ").strip().lower()
        if message == "quit":
            break

        message = choose_message(message)
        if message:
            mqtt_client.publish("shellyplus1-80646fdb37f8/command/switch:0", message)
            print(f"Message envoyé: {message}")
        else:
            print("message invalide. Veuillez entrer un message valide.")
except KeyboardInterrupt:
    print("\nArrêt du programme.")
finally:
    mqtt_client.disconnect()
