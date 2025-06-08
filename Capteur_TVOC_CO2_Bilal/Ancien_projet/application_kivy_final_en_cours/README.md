# SuiviAirMenuiserieApp

Application Python pour surveiller la qualité de l’air (CO₂ et TVOC) avec un capteur CCS811 et envoi automatique des mesures à un broker MQTT.

---

## Présentation

Ce projet permet de :
- Lire les mesures de CO₂ (en ppm) et TVOC (en ppb) via un capteur CCS811 connecté à une carte Unihiker.
- Afficher ces mesures en temps réel dans une interface graphique Kivy.
- Envoyer automatiquement les mesures au broker MQTT toutes les 10 minutes.
- Afficher l’adresse MAC de l’appareil.
- Gérer dynamiquement les seuils d’alerte reçus par MQTT.
- Alerter l’utilisateur en cas de problème capteur ou de connexion.

---

## Fonctionnalités principales

- Affichage en temps réel des mesures de CO₂ et TVOC.
- Affichage de l’adresse MAC de l’appareil.
- Envoi automatique des mesures toutes les 10 minutes au broker MQTT.
- Alertes si le capteur est déconnecté ou en défaut.
- Interface graphique simple avec Kivy.
- Gestion dynamique des seuils via MQTT.

---

## Installation

1. **Prérequis** : Python 3.10 ou supérieur, carte Unihiker, capteur CCS811.
2. **Dépendances** :
   ```bash
   pip install kivy getmac paho-mqtt pinpong
   ```
3. **Lancement** :
   ```bash
   python modele_mvc\suiviairmenuiserieapp\main.py
   ```

---

## Structure du projet et explication des scripts

- `modele_mvc/suiviairmenuiserieapp/main.py`  
  Point d’entrée de l’application. Initialise Kivy, les vues, les modèles et le contrôleur principal.

- `modele_mvc/suiviairmenuiserieapp/vues/vue_accueil.py`  
  Vue principale affichant les mesures CO₂/TVOC, les alertes, la moyenne journalière, et les boutons d’action.

- `modele_mvc/suiviairmenuiserieapp/vues/vue_ecran1.py`  
  Vue secondaire affichant l’adresse MAC de l’appareil.

- `modele_mvc/suiviairmenuiserieapp/modeles/modele_accueil.py`  
  Modèle principal : gère la lecture des mesures, la logique de seuils, l’envoi MQTT, la gestion du capteur.

- `modele_mvc/suiviairmenuiserieapp/modeles/modele_ecran1.py`  
  Modèle pour la gestion de l’adresse MAC.

- `modele_mvc/suiviairmenuiserieapp/controleurs/controleur_principal.py`  
  Contrôleur principal : fait le lien entre les modèles et les vues, gère la logique d’application, les changements d’écran, les mises à jour périodiques, etc.

- `modele_mvc/suiviairmenuiserieapp/ccs811_mqtt_projetclasses/ccs811.py`  
  Module bas niveau pour la gestion du capteur CCS811 (I2C) : lecture brute des valeurs, configuration, gestion des erreurs matérielles.

- `modele_mvc/suiviairmenuiserieapp/ccs811_mqtt_projetclasses/gestion_tvoc_co2.py`  
  Classe d’abstraction pour lire les valeurs CO₂/TVOC du capteur CCS811 de façon simple.

- `modele_mvc/suiviairmenuiserieapp/ccs811_mqtt_projetclasses/communication_mqtt_ccs811.py`  
  Classe pour la communication MQTT : connexion, publication des mesures, gestion de l’adresse MAC comme identifiant.

- `modele_mvc/suiviairmenuiserieapp/ccs811_mqtt_projetclasses/test_main_capteur_gestion_mqtt.py`  
  Script de test pour lire les valeurs du capteur CCS811 et les publier sur le broker MQTT en ligne de commande (sans interface graphique).

- `modele_mvc/suiviairmenuiserieapp/ccs811_mqtt_projetclasses/mqtt_broker_connexion.py`  
  Script pour se connecter au broker MQTT et afficher tous les messages reçus (outil de debug).

- `modele_mvc/suiviairmenuiserieapp/demo3.kv`  
  Fichier de layout Kivy : définit l’interface graphique (placement des boutons, labels, couleurs, etc.).

---

## Utilisation

- Lancer l’application pour afficher les mesures.
- Cliquer sur "Adresse MAC" pour voir l’adresse réseau.
- Les mesures sont envoyées automatiquement au serveur MQTT toutes les 10 minutes.
- Les seuils d’alerte peuvent être mis à jour dynamiquement via MQTT.

---

## Conseils pour bien démarrer

- Utilisez les boutons à l’écran pour naviguer entre les vues.
- Un message d’accueil s’affiche en haut de l’application.
- Un message d’erreur s’affiche en rouge si le capteur n’est pas détecté.
- Fermez la fenêtre pour quitter l’application.
- Les valeurs sont mises à jour toutes les 8 secondes.
- Les données sont envoyées automatiquement toutes les 10 minutes.

---

## Dépendances principales

- [Kivy](https://kivy.org/) : interface graphique
- [pinpong](https://github.com/DFRobot/pinpong) : gestion du matériel Unihiker/CCS811
- [paho-mqtt](https://pypi.org/project/paho-mqtt/) : communication MQTT
- [getmac](https://pypi.org/project/getmac/) : récupération de l’adresse MAC

---

## Historique des versions

- **v1.0.0** : Première version (affichage CO₂/TVOC, envoi MQTT, interface simple).
- **v1.1.0** : Gestion dynamique du capteur, documentation améliorée.
- **v1.2.0** : Nettoyage du code, simplification pour l’utilisateur.
- **v1.3.0** : Ajout d’un guide utilisateur, labels d’aide, README enrichi.
- **v1.4.0** : README simplifié, explications détaillées, vocabulaire accessible.

---

## Auteurs

- Bilal DAG

---

## Licence

Ce projet est fourni à des fins pédagogiques.  
Ajoutez ici votre licence si besoin.

---

## Besoin d’aide ?

Si vous avez une question ou un souci, relisez ce fichier ou consultez les commentaires dans le code.  
Bonne utilisation !
