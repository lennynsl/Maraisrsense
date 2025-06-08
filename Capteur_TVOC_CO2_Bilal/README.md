# Capteur TVOC & CO₂ (CCS811) – UNIHIKER

**Version finale – Projet pédagogique et démonstrateur industriel 2024**

---

## Présentation

Ce dépôt propose une solution complète pour la surveillance de la qualité de l'air (CO₂ et TVOC) à l'aide d'un capteur CCS811 connecté à une carte UNIHIKER.  
Le projet couvre tous les usages : test matériel, interface graphique (Kivy), envoi automatique des mesures sur Internet (MQTT), gestion dynamique des seuils d'alerte, robustesse industrielle, et exemples pédagogiques.

---

## Public visé

- **Débutants** : prise en main rapide, test matériel simple.
- **Enseignants/Makers** : intégration facile dans des TP ou projets IoT.
- **Développeurs** : architecture MVC, scripts robustes, communication réseau.
- **Industriels** : supervision, alertes, traçabilité, gestion multi-capteurs.

---

## Organisation du dépôt

| Dossier / Script                | Description                                                                                   | Public cible                        |
|----------------------------------|----------------------------------------------------------------------------------------------|-------------------------------------|
| **Projet_plus_récent_fini/**     | Application la plus avancée : interface graphique (Kivy), MVC, gestion industrielle, logs.   | Utilisateur final, développeur      |
| **Script_Test_Fin_CCS_Gestion/** | Scripts de test et gestion du capteur, publication MQTT, vérification du matériel.           | Débutant, testeur, intégrateur      |
| **Test_MQTT_Simple/**            | Exemples pour tester la connexion et l'envoi de données à un serveur MQTT.                   | Développeur, test réseau            |
| **Adresse_MAC_Obtained/**        | Script pour récupérer l'adresse MAC de la carte (identification réseau).                     | Développeur, administrateur réseau  |
| **physique_CCS811/**             | Script minimal pour vérifier le capteur (console, pas de réseau).                            | Débutant, test matériel rapide      |
| **Ancien_projet/**               | Archives, prototypes, versions précédentes.                                                  | Développeur, rétrocompatibilité     |

---

## Fonctionnalités principales

- Lecture fiable des valeurs de CO₂ (ppm) et TVOC (ppb) via I2C.
- Affichage graphique moderne (Kivy) ou console.
- Publication automatique et sécurisée des mesures sur un broker MQTT.
- Gestion dynamique des seuils d’alerte via MQTT.
- Robustesse industrielle : gestion des erreurs, logs, reconnexion automatique.
- Scripts de test matériel et d’intégration réseau.

---

## Prise en main rapide

### 1. Tester le capteur (console)
```bash
cd physique_CCS811
python physique_co2_tvoc_ccs811.py
```
*Affiche les valeurs toutes les 10 secondes dans la console.*

### 2. Lancer l'application graphique complète
```bash
cd Projet_plus_récent_fini/kivy_application_tvoc_co2_dag_bilal/modele_mvc
python main.py
```
*Interface graphique, alertes, envoi automatique, navigation.*

### 3. Envoyer les mesures sur Internet (MQTT)
Configurer le serveur dans `Test_MQTT_Simple/Comunication_CCS811_V2.py` puis :
```bash
python Test_MQTT_Simple/Comunication_CCS811_V2.py
```

### 4. Écouter les messages MQTT (debug)
```bash
python Test_MQTT_Simple/MQTT\ broker\ connexion.py
```

### 5. Récupérer l'adresse MAC
```bash
python Script_Test_Fin_CCS_Gestion/Adresse_MAC_Obtained/obtained_MAC.py
```

---

## Installation & Dépendances

- **Matériel** : Carte UNIHIKER, capteur CCS811 (I2C).
- **Logiciel** : Python 3.8+, modules : `kivy`, `pinpong`, `paho-mqtt`, `getmac`.
- **Installation** :
  ```bash
  pip install kivy pinpong paho-mqtt getmac
  ```

---

## Architecture logicielle

- **MVC (Modèle-Vue-Contrôleur)** :  
  - **Modèle** : logique métier, gestion du capteur, communication MQTT, calculs, seuils.
  - **Vue** : interface graphique (Kivy), affichage des mesures, alertes, navigation.
  - **Contrôleur** : fait le lien entre modèle et vue, orchestre les actions, gère les interactions utilisateur.
- **Scripts de test** : Pour vérifier chaque brique séparément (matériel, réseau, etc.).
- **Gestion des erreurs** : try/except partout, logs, reconnexion automatique.
- **Extensible** : Ajoutez d'autres capteurs, adaptez l'interface, changez le serveur MQTT facilement.

---

## Pourquoi plusieurs dossiers ?

- **physique_CCS811/** : Diagnostic matériel rapide, sans dépendance réseau.
- **Script_Test_Fin_CCS_Gestion/** : Test capteur ↔ Python ↔ MQTT sans interface graphique.
- **Projet_plus_récent_fini/** : Application complète, robuste, prête à l'emploi ou à intégrer.
- **Test_MQTT_Simple/** : Apprentissage ou diagnostic de la communication réseau.
- **Adresse_MAC_Obtained/** : Identification réseau (multi-capteurs).
- **Ancien_projet/** : Historique, exemples, rétrocompatibilité.

---

## Conseils & Bonnes pratiques

- Respectez la séparation MVC pour la maintenance et l’évolutivité.
- Commentez vos ajouts pour faciliter la compréhension et la reprise du code.
- Testez chaque modification sur l’interface et la communication MQTT.
- Consultez les logs pour diagnostiquer les problèmes matériels ou réseau.
- Adaptez les seuils et la configuration MQTT selon votre environnement.

---

## Auteur & Contribution

- **Bilal DAG (Étudiant 2)** – auteur principal, conception, développement, documentation.
- Basé sur des travaux de Sasa Saftic, Sparkfun, Nathan Seidle, etc.

Pour toute question, suggestion ou contribution, ouvrez une issue ou contactez l’auteur.  
Les contributions sont les bienvenues : fork, pull request, documentation, tests, etc.

---

**Projet final validé – 2024**  
Merci à tous les contributeurs et utilisateurs !


