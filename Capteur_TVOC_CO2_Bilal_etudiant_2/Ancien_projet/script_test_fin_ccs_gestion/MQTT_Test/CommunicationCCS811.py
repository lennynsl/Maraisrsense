import paho.mqtt.client as mqtt


class CommunicationCCS811:
    """
    Classe pour gérer la communication MQTT avec le capteur CCS811.
    """

    def __init__(self, broker, port, topic):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = mqtt.Client()

    def connect(self):
        self.client.connect(self.broker, self.port)

    def publish(self, message):
        self.client.publish(self.topic, message)
        print(f"Message envoyé: {message}")


if __name__ == "__main__":
    mqtt_client = CommunicationCCS811(
        broker="127.0.0.1",
        port=1883,
        topic="d2e09263c6cc/test_topic",
    )
    mqtt_client.connect()
    mqtt_client.publish("Test données publication")
