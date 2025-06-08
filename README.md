# 🌈 Marais'R'Sense – Plateforme de Surveillance de la Qualité de l'Air

Bienvenue sur le dépôt **Marais'R'Sense** !  
Ce projet open source propose des outils simples pour mesurer, afficher et surveiller la qualité de l'air, adaptés à l'enseignement, la découverte, ou l'industrie.

---

## 🗂️ Structure des dossiers principaux

| Dossier | À quoi ça sert ? | Pour qui ? |
|---------|------------------|------------|
| [projet_plus_récent_fini](./Capteur_TVOC_CO2_Bilal_etudiant_2/projet_plus_récent_fini) | Application complète avec interface graphique (Kivy), gestion avancée, envoi automatique des mesures | Utilisateur final, développeur |
| [physique_CCS811](./Capteur_TVOC_CO2_Bilal_etudiant_2/physique_CCS811) | Tester rapidement le capteur CCS811 (CO₂/TVOC) sans réseau, juste en console | Débutant, test matériel |
| [test_mqtt_simple_basique](./Capteur_TVOC_CO2_Bilal_etudiant_2/test_mqtt_simple_basique) | Exemples très simples pour vérifier la connexion et l'envoi de données MQTT | Développeur, test réseau |
| [Ancien_projet](./Capteur_TVOC_CO2_Bilal_etudiant_2/Ancien_projet) | Archives, anciens essais, prototypes | Pour référence, rétrocompatibilité |

---

### 📁 Détail des dossiers (cliquez pour en savoir plus)

<details>
<summary><strong>projet_plus_récent_fini</strong> – Application complète</summary>

- Application graphique moderne (Kivy)
- Architecture claire (MVC)
- Mesure automatique et envoi sur Internet (MQTT)
- Gestion des alertes et seuils dynamiques
- Plusieurs écrans (accueil, adresse MAC, alertes)
- **Pour lancer :**
  ```bash
  cd Capteur_TVOC_CO2_Bilal_etudiant_2/projet_plus_récent_fini/kivy_application_tvoc_co2_bilal/modele_mvc
  python main.py
  ```
- Voir le README du dossier pour plus d'explications.
</details>

<details>
<summary><strong>physique_CCS811</strong> – Test matériel rapide</summary>

- Vérifie que le capteur CCS811 fonctionne bien (CO₂, TVOC)
- Affiche les mesures toutes les 10 secondes dans la console
- Idéal pour vérifier le câblage ou le matériel sans se compliquer
- **Pour lancer :**
  ```bash
  cd Capteur_TVOC_CO2_Bilal_etudiant_2/physique_CCS811
  python physique_co2_tvoc_ccs811.py
  ```
</details>

<details>
<summary><strong>test_mqtt_simple_basique</strong> – Exemples MQTT simples</summary>

- Scripts pour tester l'envoi de données sur un serveur MQTT
- Permet de vérifier la connexion réseau et la configuration MQTT
- Très utile pour apprendre ou diagnostiquer un problème réseau
- **Pour lancer :**
  ```bash
  cd Capteur_TVOC_CO2_Bilal_etudiant_2/test_mqtt_simple_basique
  python Comunication_CCS811_V2.py
  ```
</details>

<details>
<summary><strong>Ancien_projet</strong> – Archives et prototypes</summary>

- Versions précédentes, prototypes, exemples historiques
- Sert de référence ou d'inspiration
- À ne pas utiliser pour un projet neuf
</details>

---

## 🏠 Présentation Générale

**Marais'R'Sense** permet de :
- Mesurer la qualité de l'air (CO₂, TVOC, PM2.5, PM10)
- Afficher les résultats sur écran ou ordinateur
- Déclencher des alertes (visuelles, relais, gyrophare)
- Envoyer automatiquement les données sur Internet (cloud, serveur, smartphone)
- S'adapter à tous les niveaux : test rapide, démonstration, projet industriel, ou usage pédagogique

---


## 🌟 Fonctionnalités Globales

- **Mesure précise** de CO₂ (ppm) et TVOC (ppb) via capteur CCS811 (I2C)
- **Affichage graphique moderne** (Kivy) ou console
- **Envoi automatique** des mesures sur serveur MQTT (cloud/local)
- **Gestion dynamique des seuils** d’alerte via MQTT
- **Alarmes visuelles** (gyrophare, relais, alertes écran)
- **Robustesse industrielle** : gestion des erreurs, logs, reconnexion auto
- **Extensible** : multi-capteurs, adaptation facile à d'autres environnements

---

## 🚀 Démarrage Rapide

### 1. Installation des dépendances

```bash
pip install -r requirements.txt
```
*ou, pour un module spécifique :*
```bash
pip install kivy pinpong paho-mqtt getmac
```

### 2. Lancer un module

- **Application graphique complète** (interface Kivy, MQTT, seuils dynamiques) :
  ```bash
  cd Capteur_TVOC_CO2_Bilal_etudiant_2/projet_plus_récent_fini/kivy_application_tvoc_co2_bilal/modele_mvc
  python main.py
  ```
- **Test matériel rapide** (console, sans réseau) :
  ```bash
  cd Capteur_TVOC_CO2_Bilal_etudiant_2/physique_CCS811
  python physique_co2_tvoc_ccs811.py
  ```
- **Test MQTT simple** :
  ```bash
  cd Capteur_TVOC_CO2_Bilal_etudiant_2/test_mqtt_simple_basique
  python Comunication_CCS811_V2.py
  ```

---

## 🖼️ Schéma de Fonctionnement

Voici comment s'articule l'ensemble du système Marais'R'Sense, de la mesure à l'alerte et à la supervision à distance :

```
╔════════════════════╗        ╔════════════════════╗        ╔════════════════════╗
║   Capteurs        ║        ║   Interface        ║        ║    Serveur MQTT    ║
║  (TVOC, CO₂,      ║        ║   Utilisateur      ║        ║   (Cloud/Local)    ║
║   PM2.5, PM10)    ║ ──────▶║   (Kivy, écran)    ║ ──────▶║   Stockage,        ║
╚════════════════════╝        ╚════════════════════╝        ║   supervision      ║
        │                           │                       ╚════════════════════╝
        │                           ▼
        │                 ╔════════════════════╗
        │                 ║   Alarmes &       ║
        └───────────────▶ ║   Actionneurs     ║
                          ║ (Gyrophare,       ║
                          ║  relais, alertes) ║
                          ╚════════════════════╝
```

**Explications :**
- **Capteurs** : Mesurent en continu la qualité de l'air (CO₂, TVOC, PM2.5, PM10).
- **Interface Utilisateur (Kivy)** : Affiche les mesures en temps réel, permet la navigation, montre les alertes et l'état du système.
- **Alarmes & Actionneurs** : Déclenchent des signaux visuels ou physiques (gyrophare, relais, etc.) en cas de dépassement de seuils.
- **Serveur MQTT** : Centralise les données, permet la supervision à distance, l'archivage et la gestion des seuils dynamiques.

---

## 🎨 Suggestions d'Animations & Couleurs (pour interface web)

- **Badges colorés** pour chaque projet/répertoire (ex : ![Kivy](https://img.shields.io/badge/Kivy-UI-green), ![MQTT](https://img.shields.io/badge/MQTT-Cloud-blue))
- **Transitions animées** entre les sections (CSS fade-in, slide, etc.)
- **Icônes dynamiques** pour les alertes (rouge/orange/vert selon l'état)
- **Graphiques animés** pour l'évolution des mesures (si web)
- **Boutons interactifs** pour naviguer entre les modules

---

## 📚 Documentation détaillée

Chaque dossier contient son propre `README.md` pour une prise en main rapide et des explications détaillées.  
Consultez-les pour :
- Les scripts principaux à lancer
- Les options de configuration (broker MQTT, seuils, etc.)
- Les conseils de dépannage et bonnes pratiques

---

## 👨‍💻 Contributeurs

- **Bilal** – Développement capteur TVOC, architecture MVC, documentation
- **Lenny** – Développement capteur PM, intégration capteurs particules
- **Mathieu** – Alarmes, gyrophare, alertes visuelles

---

## 🛠️ Technologies Utilisées

- **Python** (3.8+)  
  Licence : [PSF License](https://docs.python.org/3/license.html)
- **Kivy** – Interface graphique  
  Licence : [MIT](https://github.com/kivy/kivy/blob/master/LICENSE)
- **MQTT** – Communication cloud/serveur (via [paho-mqtt](https://www.eclipse.org/paho/))  
  Licence : [Eclipse Public License v2.0](https://www.eclipse.org/legal/epl-2.0/)
- **PinPong** – Contrôle matériel Unihiker/capteurs  
  Licence : [MIT](https://github.com/DFRobot/pinpong/blob/master/LICENSE)
- **Unihiker** – Microcontrôleur tactile avec écran  
  ⚠️ **Important : la carte UniHiker doit être mise à jour en version V0.4.0 minimum** pour garantir la compatibilité et la stabilité.  
  Cette version apporte :
  - Mise à niveau de la bibliothèque Pinpong vers la dernière version V0.6.1 (stabilité, vitesse et compatibilité des threads considérablement améliorées)
  - Fonction de commutation du point d'accès sans fil avec gestion du protocole de sécurité
  - Bibliothèque Unihiker mise à jour (V0.0.27)
  - Intégration de nouvelles librairies Python : `torch`, `tensorflowjs`, `tf2onnx`, `xedu-hub`
  - Liens de la page Web locale mis à jour et ajout de la commutation entre siot V1 et V2
  - Connexion WiFi compatible avec les noms contenant des symboles spéciaux
  - Amélioration des invites de mise à jour de la version de Block pip
- **getmac** – Identification réseau  
  Licence : [MIT](https://github.com/ghostofgoes/getmac/blob/master/LICENSE)

---

## 🔒 Cybersécurité

- Les communications MQTT **ne sont pas chiffrées par défaut** dans les exemples fournis.
- Pour sécuriser les échanges, activez TLS/SSL dans les scripts MQTT et utilisez des ports sécurisés.
- Les identifiants/mots de passe doivent être stockés dans des fichiers séparés ou des variables d'environnement (jamais en clair dans le code).
- Mettez à jour régulièrement vos dépendances et la carte UniHiker pour bénéficier des derniers correctifs de sécurité.
- Pour un usage professionnel/sensible, adaptez la configuration réseau et la gestion des accès selon vos exigences de sécurité.

---

## 🛡️ Cybersécurité et Bonnes Pratiques

La sécurité des données et des équipements est un enjeu important, même pour les projets de mesure environnementale :

- **Sensibilisation** : Les données de qualité de l'air peuvent être sensibles dans certains contextes (industrie, santé, école). Protégez l'accès à vos interfaces et à vos serveurs.
- **Réseau local** : Privilégiez l'utilisation sur un réseau local sécurisé pour éviter toute interception ou modification des mesures.
- **Mises à jour** : Maintenez à jour la carte UniHiker, les bibliothèques Python et vos dépendances pour bénéficier des derniers correctifs de sécurité.
- **Accès physique** : Protégez l'accès physique aux capteurs et à la carte pour éviter toute manipulation non autorisée.
- **Authentification** : Si vous ouvrez l'accès à distance (serveur MQTT, interface web), mettez en place une authentification forte et limitez les droits d'accès.
- **Logs et traçabilité** : Activez la journalisation (logging) pour détecter toute activité anormale ou intrusion.
- **Confidentialité** : Si vous partagez les données, veillez à anonymiser les informations personnelles ou sensibles.

> Pour les usages professionnels ou en milieu sensible, consultez un expert cybersécurité pour adapter la configuration à vos besoins.

---

## 📝 Licence du Projet

Ce projet est sous licence MIT.

<details>
<summary>Cliquez pour afficher la licence complète du projet</summary>

```text
MIT License

Copyright (c) 2025 Bilal, Lenny, Mathieu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Additional permissions and limitations:
- You are encouraged to cite the authors when reusing or modifying this code.
- This software is provided for educational and research purposes. Commercial use is permitted under the MIT license, but the authors disclaim any responsibility for misuse.
- If you redistribute or modify the software, please indicate the changes made.
```
</details>

---

## 📄 Licences des Outils Utilisés

- **Python** : PSF License ([voir](https://docs.python.org/3/license.html))
- **Kivy** : MIT ([voir](https://github.com/kivy/kivy/blob/master/LICENSE))
- **paho-mqtt** : Eclipse Public License v2.0 ([voir](https://www.eclipse.org/legal/epl-2.0/))
- **PinPong** : MIT ([voir](https://github.com/DFRobot/pinpong/blob/master/LICENSE))
- **getmac** : MIT ([voir](https://github.com/ghostofgoes/getmac/blob/master/LICENSE))
- **Unihiker** : [Consulter la documentation officielle pour les conditions d'utilisation](https://www.unihiker.com/)

---

> _Page d'accueil structurée et maintenue par Bilal.  
> Pour toute suggestion, ouvrez une issue ou contactez un des contributeurs._
