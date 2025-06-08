# physique_CCS811

Ce dossier contient des scripts pour tester, valider et exploiter physiquement le capteur CCS811 (lecture directe des valeurs CO₂ et TVOC via I2C sur la carte Unihiker).

---

## Table des matières

- [Présentation](#présentation)
- [Structure du dossier](#structure-du-dossier)
- [Fichiers présents](#fichiers-présents)
- [Fonctionnement détaillé](#fonctionnement-détaillé)
- [Utilisation pas à pas](#utilisation-pas-à-pas)
- [Conseils, dépannage et bonnes pratiques](#conseils-dépannage-et-bonnes-pratiques)
- [Auteurs](#auteurs)

---

## Présentation

Ce dossier est dédié à la validation matérielle et logicielle du capteur CCS811, utilisé pour mesurer la concentration de CO₂ (en ppm) et de composés organiques volatils totaux (TVOC, en ppb).  
L'objectif est de permettre une vérification rapide du câblage, de la communication I2C et de la fiabilité des mesures, sans dépendre d'une interface graphique ou d'une connexion réseau.

---

## Structure du dossier

```
physique_CCS811/
│
├── physique_co2_tvoc_ccs811.py      # Script principal de lecture du capteur CCS811
├── test_unitaire_mqtt_pub/          # Dossier de tests unitaires pour la publication MQTT
│   └── test_pub.py
├── README.md                        # Ce fichier de documentation
```

---

## Fichiers présents

- **physique_co2_tvoc_ccs811.py**  
  Script principal permettant de lire et d'afficher les valeurs de CO₂ et TVOC du capteur CCS811 via le bus I2C de la carte Unihiker.
  - Initialise la carte Unihiker et le bus I2C.
  - Effectue une lecture toutes les 10 secondes.
  - Affiche les résultats dans la console sous la forme :  
    `CO₂: <valeur> ppm | TVOC: <valeur> ppb`
  - Structure modulaire pour faciliter l'extension (ex : ajout d'envoi MQTT).

- **test_unitaire_mqtt_pub/test_pub.py**  
  Script de test unitaire pour vérifier la capacité à publier des données sur un broker MQTT.
  - Utilise la classe `ClientMQTT` pour envoyer des valeurs de test sur des topics dédiés.
  - Permet de valider la configuration réseau et la connexion au broker.

- **README.md**  
  Documentation complète du dossier, des scripts et des bonnes pratiques d'utilisation.

---

## Fonctionnement détaillé

### 1. Initialisation

- La carte Unihiker est initialisée via la bibliothèque `pinpong`.
- Le bus I2C est configuré pour communiquer avec le capteur CCS811 (adresse 0x5A).

### 2. Lecture des données

- Le script lit toutes les 10 secondes les registres du capteur pour obtenir :
  - La concentration de CO₂ (en ppm)
  - La concentration de TVOC (en ppb)
- Les valeurs sont affichées dans la console pour permettre une vérification immédiate.

### 3. Extensibilité

- La structure du code permet d'ajouter facilement d'autres fonctionnalités, comme l'envoi automatique des mesures vers un serveur MQTT ou l'enregistrement dans un fichier.

---

## Utilisation pas à pas

### Prérequis

- **Matériel** :
  - Carte Unihiker
  - Capteur CCS811 connecté sur le bus I2C
- **Logiciel** :
  - Python 3.10 ou supérieur
  - Bibliothèque `pinpong` installée

### Installation des dépendances

```bash
pip install pinpong
```

### Lancement du script principal

```bash
python physique_co2_tvoc_ccs811.py
```

### Résultat attendu

- À chaque intervalle de 10 secondes, la console affiche :
  ```
  CO₂: <valeur mesurée> ppm | TVOC: <valeur mesurée> ppb
  ```

### Lancement des tests unitaires MQTT

- Rendez-vous dans le dossier `test_unitaire_mqtt_pub` et lancez :
  ```bash
  python test_pub.py
  ```
- Vérifiez que les messages sont bien publiés sur le broker MQTT configuré.

---

## Conseils, dépannage et bonnes pratiques

- **Aucune valeur affichée ou valeurs incohérentes** :  
  - Vérifiez le câblage I2C (SDA/SCL, alimentation).
  - Assurez-vous que le capteur est bien alimenté et reconnu par la carte.
- **Erreur d'import** :  
  - Vérifiez que la bibliothèque `pinpong` est bien installée.
  - Utilisez la bonne version de Python.
- **Problèmes de connexion MQTT** :  
  - Vérifiez l'adresse, le port, l'identifiant et le mot de passe du broker.
  - Testez la connexion réseau de la carte Unihiker.
- **Bonnes pratiques** :  
  - Ne modifiez pas le script principal pour ajouter des fonctionnalités avancées : créez un nouveau module ou script dédié.
  - Documentez toute modification ou extension pour faciliter la maintenance.

---

## Auteurs

- Réalisé par l'étudiant 2 : **Bilal DAG**

---


