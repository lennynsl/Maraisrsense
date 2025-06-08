# 🌈 Marais'R'Sense – Plateforme de Surveillance de la Qualité de l'Air

Bienvenue sur le dépôt **Marais'R'Sense** !  
Ce projet open source propose des outils simples pour mesurer, afficher et surveiller la qualité de l'air, que vous soyez débutant, enseignant, curieux ou professionnel.

---

## 🗂️ Structure des dossiers principaux

Voici comment le projet est organisé.  
Chaque dossier correspond à une partie du système : capteurs, affichage, alarmes…  
Vous pouvez cliquer sur chaque nom pour voir ce qu'il contient.

---

### 1. [Capteur_TVOC_CO2_Bilal_etudiant_2](./Capteur_TVOC_CO2_Bilal_etudiant_2)  
*Mesure du CO₂ et des composés organiques volatils (TVOC) dans l'air avec la carte Unihiker*

- **physique_CCS811/**  
  *Permet de vérifier que le capteur fonctionne sur la carte Unihiker, en affichant les mesures dans la console (texte).*  
  [Voir le dossier](./Capteur_TVOC_CO2_Bilal_etudiant_2/physique_CCS811)
- **projet_plus_récent_fini/**  
  *Application avec écran graphique (boutons, couleurs, alertes) sur Unihiker pour voir les mesures en direct et envoyer les données sur Internet.*  
  [Voir le dossier](./Capteur_TVOC_CO2_Bilal_etudiant_2/projet_plus_récent_fini)
    - `kivy_application_tvoc_co2_bilal/`
        - `modele_mvc/` : Le cœur du programme graphique
- **test_mqtt_simple_basique/**  
  *Pour tester si l'envoi des mesures sur Internet fonctionne bien depuis Unihiker.*  
  [Voir le dossier](./Capteur_TVOC_CO2_Bilal_etudiant_2/test_mqtt_simple_basique)
- **Ancien_projet/**  
  *Anciens essais, archives (pour les curieux ou pour garder l'historique).*  
  [Voir le dossier](./Capteur_TVOC_CO2_Bilal_etudiant_2/Ancien_projet)

---

### 2. [Capteur_PM_Lenny_etudiant_1](./Capteur_PM_Lenny_etudiant_1)  
*Mesure des poussières fines dans l'air (PM2.5 et PM10) avec la carte Unihiker*

- **TestFinal.py**  
  *Lance la mesure et affiche les résultats à l'écran de la carte Unihiker.*
- **GestionPM.py**  
  *Gère la communication avec le capteur de poussières SDS011 branché sur Unihiker.*
- **IHM.py**  
  *Affiche les résultats de façon simple sur Unihiker.*

---

### 3. [Mathieu_etudiant_3](./Mathieu_etudiant_3)  
*Gestion des alarmes et signaux visuels (lumières, gyrophare, etc.) sur Unihiker*

- **alarmes/**  
  *Fait clignoter une lumière ou déclenche une alarme si la qualité de l'air est mauvaise.*
- **gyrophare/**  
  *Contrôle un gyrophare (lumière tournante) pour signaler un problème.*
- **integration/**  
  *Exemples pour relier les alarmes aux mesures des capteurs.*

---

## 🏠 Présentation Générale

**Marais'R'Sense**, c'est :
- Des capteurs branchés sur la carte **Unihiker** qui mesurent la qualité de l'air (CO₂, TVOC, poussières PM2.5 et PM10)
- Un affichage simple sur l'écran tactile de la carte Unihiker (avec des couleurs, des alertes)
- Des alarmes visuelles (lumières, gyrophare) qui se déclenchent si l'air devient mauvais
- L'envoi automatique des mesures sur Internet pour suivre à distance
- Un projet adapté à tous : test rapide, démonstration, projet d'école, ou usage professionnel

---


## 🌟 Fonctionnalités Globales

- **Mesure précise** de CO₂ et TVOC (polluants de l'air)
- **Affichage graphique** (écran tactile ou ordinateur) ou simple texte
- **Envoi automatique** des mesures sur Internet (pour surveiller à distance)
- **Alertes dynamiques** : les seuils d'alerte peuvent être changés à distance
- **Alarmes visuelles** : lumières, gyrophare, messages d'alerte
- **Robustesse** : le système gère les coupures, les erreurs, et se reconnecte tout seul
- **Extensible** : on peut ajouter d'autres capteurs facilement

---

## 🚀 Démarrage Rapide

Même si vous n'êtes pas informaticien, voici comment tester :

### 1. Installer les programmes nécessaires

Ouvrez un terminal (ou invite de commandes) et tapez :
```bash
pip install -r requirements.txt
```
*Ou, pour installer seulement ce qu'il faut pour un module :*
```bash
pip install kivy pinpong paho-mqtt getmac
```

### 2. Lancer un module (exemple)

- **Pour voir les mesures sur un écran graphique** :
  ```bash
  cd Capteur_TVOC_CO2_Bilal_etudiant_2/projet_plus_récent_fini/kivy_application_tvoc_co2_bilal/modele_mvc
  python main.py
  ```
- **Pour tester le capteur simplement (texte)** :
  ```bash
  cd Capteur_TVOC_CO2_Bilal_etudiant_2/physique_CCS811
  python physique_co2_tvoc_ccs811.py
  ```
- **Pour tester l'envoi sur Internet** :
  ```bash
  cd Capteur_TVOC_CO2_Bilal_etudiant_2/test_mqtt_simple_basique
  python Comunication_CCS811_V2.py
  ```

---

## 🖼️ Schéma de Fonctionnement

Voici comment tout fonctionne ensemble :

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

**En résumé :**
- Les capteurs mesurent la qualité de l'air en continu
- Les résultats s'affichent sur un écran (avec des couleurs et des alertes)
- Si l'air devient mauvais, une lumière ou un gyrophare s'allume
- Les mesures sont envoyées sur Internet pour être consultées à distance

---

## 📚 Documentation détaillée

Chaque dossier contient un fichier `README.md` qui explique :
- Comment lancer les scripts
- Comment configurer les seuils d'alerte ou le serveur Internet
- Des conseils pour dépanner si besoin

---

## 👨‍💻 Contributeurs

- **Bilal** – Capteur TVOC/CO₂, interface graphique, documentation
- **Lenny** – Capteur de poussières PM, intégration particules fines
- **Mathieu** – Alarmes, gyrophare, alertes visuelles

---

## 🛠️ Technologies Utilisées

- **Python** (le langage principal)
- **Kivy** (pour l'affichage graphique)
- **MQTT** (pour envoyer les mesures sur Internet)
- **PinPong** (pour communiquer avec les capteurs)
- **Unihiker** (petit ordinateur avec écran tactile)
- **getmac** (pour identifier l'appareil sur le réseau)

---

## 🔒 Sécurité et bonnes pratiques

- Les échanges Internet ne sont pas chiffrés par défaut (pour les tests)
- Pour plus de sécurité, activez le chiffrement (TLS/SSL) et protégez vos mots de passe
- Mettez à jour régulièrement les programmes et la carte Unihiker
- Protégez l'accès physique aux capteurs

---

## 📝 Licence du Projet

Ce projet est sous licence MIT (libre et gratuit, voir détails plus bas).

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
