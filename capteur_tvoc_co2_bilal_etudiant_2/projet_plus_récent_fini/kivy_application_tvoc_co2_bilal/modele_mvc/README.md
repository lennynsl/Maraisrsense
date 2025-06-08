# SuiviAirMenuiserieApp

Application de surveillance de la qualité de l'air (CO2 et TVOC) basée sur un capteur CCS811 et une carte Unihiker, suivant l'architecture **MVC** (Modèle-Vue-Contrôleur).

---

## Sommaire

- [Présentation](#présentation)
- [Installation & Dépendances](#installation--dépendances)
- [Exemple de lancement](#exemple-de-lancement)
- [Configuration](#configuration)
- [Architecture du projet](#architecture-du-projet)
- [Structure détaillée](#structure-détaillée)
- [Fonctionnement général](#fonctionnement-général)
- [Personnalisation & Conseils](#personnalisation--conseils)
- [Détail des principaux scripts](#détail-des-principaux-scripts)
- [Précision des capteurs](#précision-des-capteurs)
- [Fréquence d'échantillonnage](#fréquence-déchantillonnage)
- [Bonnes pratiques de développement](#bonnes-pratiques-de-développement)
- [Flux de données](#flux-de-données)
- [Pour les développeurs](#pour-les-développeurs)
- [Historique des versions](#historique-des-versions)
- [Conseils](#conseils)
- [Support](#support)

---

## Présentation

Cette application permet de surveiller la qualité de l'air (CO2 et TVOC) à l'aide d'un capteur CCS811 connecté à une carte Unihiker.  
Elle suit l'architecture **MVC** pour une séparation claire des responsabilités.

---

## Installation & Dépendances

**Prérequis :**
- Python 3.8+
- Matériel : Unihiker + capteur CCS811

**Dépendances Python :**
- `kivy`
- `getmac`
- `paho-mqtt`
- `pinpong`
- `logging`

Installez-les avec :
```bash
pip install kivy getmac paho-mqtt pinpong
```

---

## Exemple de lancement

Dans le dossier du projet, exécutez :
```bash
python main.py
```
Assurez-vous que le matériel est connecté et que les dépendances sont installées.

---

## Configuration

- **Adresse du broker MQTT** : modifiable dans `modele_accueil.py` et `communication_mqtt_ccs811.py`
- **Fréquence d'échantillonnage** : modifiable dans `controleur_principal.py` (paramètre de `Clock.schedule_interval`)
- **Seuils dynamiques** : reçus via MQTT, modifiables côté serveur

---

## Architecture du projet

- **Modèles (`modeles/`)** : logique métier, gestion des données, communication capteur/MQTT
- **Vues (`vues/` + `demo3.kv`)** : affichage, interactions utilisateur, callbacks
- **Contrôleur (`controleurs/`)** : lien modèles/vues, navigation, orchestration, mises à jour

---

## Structure détaillée

```
suiviairmenuiserieapp/
│
├── modeles/
│     ├── modele_accueil.py        # Modèle principal : logique métier, gestion capteur, MQTT, seuils
│     └── modele_ecran1.py         # Modèle secondaire : gestion de l'adresse MAC
│
├── vues/
│     ├── vue_accueil.py           # Vue principale : affichage mesures, alertes, boutons
│     └── vue_ecran1.py            # Vue secondaire : affichage adresse MAC
│
├── controleurs/
│     └── controleur_principal.py  # Contrôleur principal : navigation, callbacks, orchestration MVC
│
├── ccs811_mqtt_projetclasses/
│     ├── ccs811.py                        # Accès bas niveau au capteur CCS811 (I2C)
│     ├── gestion_tvoc_co2.py              # Interface simple pour lire les mesures du capteur
│     ├── communication_mqtt_ccs811.py     # Gestion de la communication MQTT (envoi mesures)
│     └── ... (autres scripts techniques)
│
├── demo3.kv                      # Layout graphique Kivy (définit l'interface utilisateur)
├── main.py                       # Point d'entrée de l'application (initialisation MVC/Kivy)
└── __init__.py
```

---

## Fonctionnement général

- **Lecture des mesures** :  
  Le modèle lit les valeurs du capteur CCS811 (CO2, TVOC) et calcule les moyennes.
  - *Remarque :* Au premier démarrage, le capteur retourne souvent 400 ppm pour le CO2 et 0 ppb pour le TVOC. Une logique de filtrage de la première valeur est prévue dans le modèle.
- **Affichage** :  
  Les vues affichent dynamiquement les mesures, alertes, adresse MAC, etc.
- **Envoi automatique** :  
  Les mesures sont envoyées toutes les 10 minutes au serveur MQTT.
- **Seuils dynamiques** :  
  Les seuils (correct/limite pour CO2 et TVOC) sont reçus en temps réel via MQTT.
- **Navigation** :  
  Le contrôleur gère le passage entre les écrans (accueil, adresse MAC).
- **Fréquence d'échantillonnage** :  
  Mesure et affichage toutes les 5 secondes (modifiable).

---

## Personnalisation & Conseils

- **Valeurs initiales** :  
  CO2 et TVOC sont initialisés à 0. Pour ignorer la première valeur par défaut du capteur, activez la logique de filtrage dans `modele_accueil.py`.
- **Changer la fréquence d'échantillonnage** :  
  Modifiez la valeur dans le contrôleur (`controleur_principal.py`).
- **Robustesse** :  
  L'application gère les erreurs de capteur et de réseau pour éviter les plantages. Consultez les logs pour diagnostiquer les problèmes.

---

## Détail des principaux scripts

### Modèles

- **`modele_accueil.py`** :  
  Lecture capteur, calcul moyennes, gestion seuils, envoi MQTT, robustesse.
- **`modele_ecran1.py`** :  
  Fournit l'adresse MAC.

### Vues

- **`vue_accueil.py`** :  
  Affichage CO2/TVOC, alertes, moyennes, navigation.
- **`vue_ecran1.py`** :  
  Affichage adresse MAC, bouton retour.
- **`demo3.kv`** :  
  Layout graphique.

### Contrôleur

- **`controleur_principal.py`** :  
  Lien modèles/vues, navigation, planification, gestion des erreurs.

### Techniques

- **`ccs811.py`** :  
  Accès bas niveau au capteur CCS811.
- **`gestion_tvoc_co2.py`** :  
  Interface simplifiée pour obtenir les mesures.
- **`communication_mqtt_ccs811.py`** :  
  Connexion et envoi des mesures au broker MQTT.

---

## Précision des capteurs

Les capteurs doivent respecter les normes de précision applicables aux risques industriels.

- **CO2** : conforme **EN 50543** (ou équivalent)
- **TVOC** : conforme **EN 14662** (ou équivalent)
- Précision typique : ±15% près des seuils d’exposition professionnelle

> *Le capteur CCS811 est destiné à un usage pédagogique. Pour un usage industriel critique, utiliser des capteurs certifiés.*

---

## Fréquence d'échantillonnage

- **Par défaut** : 5 secondes (modifiable)
- **Envoi MQTT** : toutes les 10 minutes

---

## Bonnes pratiques de développement

- **Conventions de nommage** : noms explicites, en français, respectant PEP8.
- **Documentation** : chaque classe/fonction est documentée.
- **Logger** : suivi des événements et erreurs via `logging`.
- **Gestion des exceptions** : blocs try/except pour la robustesse.

---

## Flux de données

1. **Lecture** : Le modèle lit les valeurs du capteur CCS811.
2. **Traitement** : Stockage, calcul des moyennes, vérification des seuils.
3. **Affichage** : Le contrôleur transmet les valeurs à la vue.
4. **Envoi** : Toutes les 10 minutes, envoi au broker MQTT.
5. **Seuils** : Si un seuil est modifié via MQTT, il est appliqué immédiatement.

---

## Pour les développeurs

- **Ajouter un capteur** : nouvelle classe dans `modeles/`, adapter la logique métier, modifier la vue si besoin.
- **Modifier l'affichage** : modifier `vue_accueil.py` ou `demo3.kv`.
- **Changer de broker MQTT** : modifier l'adresse dans `modele_accueil.py` et `communication_mqtt_ccs811.py`.
- **Ajouter une fonctionnalité** : ajouter la logique dans le modèle, les callbacks dans le contrôleur, l'affichage dans la vue.

---

## Historique des versions

- **v1.0.0** : Première version (affichage CO2/TVOC, envoi MQTT, interface simple).
- **v1.1.0** : Gestion dynamique du capteur, documentation améliorée.
- **v1.2.0** : Nettoyage du code, simplification pour l'utilisateur.
- **v1.3.0** : Ajout de commentaires détaillés, documentation enrichie, versionning amélioré.
- **v1.4.0** : Documentation structurante pour développeurs, explications détaillées, conformité MVC vérifiée.
- **v1.5.0** : Ajout des exigences industrielles (précision, fréquence), robustesse, conventions de nommage, gestion des erreurs, loggers.
- **v1.6.0** : Fréquence d'échantillonnage configurable, documentation mise à jour, robustesse accrue pour la gestion du capteur.

---

## Conseils

- **Respectez la séparation MVC** : ne mélangez pas logique métier, affichage et contrôle.
- **Commentez vos ajouts** pour faciliter la maintenance.
- **Testez chaque modification** sur l'interface et la communication MQTT.
- **Consultez ce README** et les commentaires dans chaque fichier pour comprendre la structure.

---

## Support

Pour toute question, contactez le responsable du projet ou ouvrez une issue sur le dépôt.

---

**Auteur : DAG Bilal (Etudiant 2)**

Bonne contribution !
