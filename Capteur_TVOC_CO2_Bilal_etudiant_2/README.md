# Capteur TVOC & CO₂ (CCS811) – UNIHIKER

**Version finale – Projet pédagogique et démonstrateur industriel 2024**

---

## Présentation

Ce dossier propose une solution simple pour surveiller la qualité de l'air (CO₂ et TVOC) avec un capteur CCS811 branché sur une carte UNIHIKER.  
Vous pouvez tester le matériel, utiliser une application graphique, envoyer les mesures sur Internet (MQTT), gérer les alertes, et plus encore.

---

## Pour qui ?

- **Débutants** : prise en main rapide, test matériel simple.
- **Enseignants/Makers** : facile à intégrer dans un TP ou un projet.
- **Développeurs** : code structuré, communication réseau, scripts robustes.
- **Industriels** : supervision, alertes, gestion multi-capteurs.

---

## Organisation du dossier

| Dossier                        | À quoi ça sert ?                                                                 | Pour qui ?                    |
|--------------------------------|----------------------------------------------------------------------------------|-------------------------------|
| **projet_plus_récent_fini/**   | Application complète avec interface graphique (Kivy), gestion avancée, logs.      | Utilisateur final, développeur |
| **physique_CCS811/**           | Tester rapidement le capteur CCS811 (console, sans réseau).                      | Débutant, test matériel        |
| **test_mqtt_simple_basique/**  | Exemples très simples pour vérifier la connexion et l'envoi de données MQTT.     | Développeur, test réseau       |
| **Ancien_projet/**             | Archives, anciens essais, prototypes.                                            | Pour référence, rétrocompat.   |

---

## Fonctionnalités principales

- Lire les valeurs de CO₂ (ppm) et TVOC (ppb) simplement.
- Afficher les mesures sur écran ou dans la console.
- Envoyer automatiquement les mesures sur Internet (MQTT).
- Recevoir et gérer les seuils d’alerte à distance.
- Robuste : gestion des erreurs, reconnexion automatique, logs.
- Scripts pour tester le matériel ou le réseau facilement.

---

## Comment démarrer rapidement ?

### 1. Tester le capteur (console)
```bash
cd physique_CCS811
python physique_co2_tvoc_ccs811.py
```
*Affiche les valeurs toutes les 10 secondes dans la console.*

### 2. Lancer l'application graphique complète
```bash
cd projet_plus_récent_fini/kivy_application_tvoc_co2_bilal/modele_mvc
python main.py
```
*Interface graphique, alertes, envoi automatique, navigation.*

### 3. Tester l'envoi MQTT simple
```bash
cd test_mqtt_simple_basique
python Comunication_CCS811_V2.py
```
*Vérifie la connexion et l'envoi de données sur un serveur MQTT.*

---

## Installation & Dépendances

- **Matériel** : Carte UNIHIKER, capteur CCS811 (I2C).
- **Logiciel** : Python 3.8+, modules : `kivy`, `pinpong`, `paho-mqtt`, `getmac`.
- **Installer les dépendances** :
  ```bash
  pip install kivy pinpong paho-mqtt getmac
  ```

---

## Pourquoi plusieurs dossiers ?

- **physique_CCS811/** : Tester le matériel sans se compliquer, juste en console.
- **projet_plus_récent_fini/** : Application complète, interface graphique, gestion avancée.
- **test_mqtt_simple_basique/** : Tester ou apprendre la communication réseau MQTT.
- **Ancien_projet/** : Archives, exemples, prototypes (pour référence).

---

## Conseils & Bonnes pratiques

- Respectez la séparation des dossiers pour vous y retrouver facilement.
- Commentez vos ajouts pour aider les autres (et vous-même plus tard).
- Testez chaque modification sur l’interface ou la communication réseau.
- Consultez les logs si un problème survient.
- Adaptez les seuils et la configuration MQTT selon votre besoin.

---

## Auteur & Contribution

- **Bilal DAG (Étudiant 2)** – auteur principal, conception, développement, documentation.

Pour toute question ou suggestion, ouvrez une issue ou contactez l’auteur.  
Les contributions sont les bienvenues : fork, pull request, documentation, tests, etc.

---

**Projet final validé – 2024**  
Merci à tous les contributeurs et utilisateurs !


