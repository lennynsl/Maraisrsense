<!--
Améliorations visuelles : titres plus grands, encadrés, couleurs (Markdown), icônes, séparation nette.
-->

# 🌈 **Marais'R'Sense** – *Plateforme de Surveillance de la Qualité de l'Air*

Bienvenue sur le dépôt **Marais'R'Sense** !  
Ce projet open source met à votre disposition des outils accessibles et fiables pour mesurer, visualiser et surveiller la qualité de l'air, que vous soyez débutant, enseignant, passionné ou professionnel.

---

## 🗂️ **Structure des dossiers principaux**

> **Chaque dossier correspond à une partie du système : capteurs, affichage, alarmes…**  
> *Cliquez sur chaque nom pour voir ce qu'il contient.*

---

### <span style="font-size:1.2em; color:#1e90ff;">1. [Capteur_TVOC_CO2_Bilal_etudiant_2](./Capteur_TVOC_CO2_Bilal_etudiant_2)</span>  
*<span style="color:#555;">Mesure du CO₂ et des composés organiques volatils (TVOC) dans l'air avec la carte UniHiker</span>*

- <span style="color:#228B22;">**physique_CCS811/**</span>  
  <span style="color:#555;">Test matériel simple du capteur CCS811 sur UniHiker, affichage des mesures dans la console (texte).</span>  
  [Voir le dossier](./Capteur_TVOC_CO2_Bilal_etudiant_2/physique_CCS811)
- <span style="color:#228B22;">**projet_plus_récent_fini/**</span>  
  <span style="color:#555;">Application graphique complète (Kivy, MVC, gestion MQTT, alertes) sur UniHiker. Permet de visualiser les mesures, recevoir des alertes, envoyer les données sur Internet.</span>  
  [Voir le dossier](./Capteur_TVOC_CO2_Bilal_etudiant_2/projet_plus_récent_fini)
    - `kivy_application_tvoc_co2_bilal/`
        - `modele_mvc/` : Le cœur du programme graphique (lancement principal)
- <span style="color:#228B22;">**test_mqtt_simple_basique/**</span>  
  <span style="color:#555;">Scripts pour tester l'envoi et la réception MQTT depuis UniHiker (vérification réseau).</span>  
  [Voir le dossier](./Capteur_TVOC_CO2_Bilal_etudiant_2/test_mqtt_simple_basique)
- <span style="color:#228B22;">**Ancien_projet/**</span>  
  <span style="color:#555;">Archives, prototypes, anciens essais (pour référence ou historique).</span>  
  [Voir le dossier](./Capteur_TVOC_CO2_Bilal_etudiant_2/Ancien_projet)

> Chaque sous-dossier contient un `README.md` qui explique comment utiliser les scripts, les prérequis et les conseils de dépannage.

---

### <span style="font-size:1.2em; color:#ff8c00;">2. [Capteur_PM_Lenny_etudiant_1](./Capteur_PM_Lenny_etudiant_1)</span>  
*<span style="color:#555;">Mesure des poussières fines dans l'air (PM2.5 et PM10) avec la carte UniHiker</span>*

- **TestFinal.py**  
  <span style="color:#555;">Script principal pour lancer la mesure et afficher les résultats sur l'écran de la carte UniHiker.</span>
- **GestionPM.py**  
  <span style="color:#555;">Classe pour gérer la communication avec le capteur de poussières SDS011.</span>
- **IHM.py**  
  <span style="color:#555;">Interface graphique simple pour afficher les résultats sur UniHiker.</span>

---

### <span style="font-size:1.2em; color:#e74c3c;">3. [Mathieu_etudiant_3](./Mathieu_etudiant_3)</span>  
*<span style="color:#555;">Gestion des alarmes et signaux visuels (lumières, gyrophare, etc.) sur UniHiker</span>*

- **alarmes/**  
  <span style="color:#555;">Scripts pour déclencher des alarmes visuelles ou sonores si la qualité de l'air est mauvaise.</span>
- **gyrophare/**  
  <span style="color:#555;">Contrôle d'un gyrophare (lumière tournante) pour signaler un problème.</span>
- **integration/**  
  <span style="color:#555;">Exemples pour relier les alarmes aux mesures des capteurs (intégration avec les autres modules).</span>

---

## 🏠 **Présentation Générale**

**Marais'R'Sense**, c'est :
- 🟢 **Des capteurs branchés sur la carte UniHiker** qui mesurent la qualité de l'air (CO₂, TVOC, poussières PM2.5 et PM10)
- 🟡 **Un affichage simple sur l'écran tactile** de la carte UniHiker (avec des couleurs, des alertes)
- 🔴 **Des alarmes visuelles** (lumières, gyrophare) qui se déclenchent si l'air devient mauvais
- 🌐 **L'envoi automatique des mesures sur Internet** pour suivre à distance
- 👨‍🎓 **Un projet adapté à tous** : test rapide, démonstration, projet d'école, ou usage professionnel

---

## 🌟 **Fonctionnalités Globales**

- 🎯 **Mesure précise** de CO₂ et TVOC (polluants de l'air)
- 🖥️ **Affichage graphique** (écran tactile UniHiker) ou simple texte
- 📡 **Envoi automatique** des mesures sur Internet (pour surveiller à distance)
- 🚨 **Alertes dynamiques** : les seuils d'alerte peuvent être changés à distance
- 💡 **Alarmes visuelles** : lumières, gyrophare, messages d'alerte
- 🔄 **Robustesse** : le système gère les coupures, les erreurs, et se reconnecte tout seul
- ➕ **Extensible** : on peut ajouter d'autres capteurs facilement

---

## 🚀 **Démarrage Rapide**

Même si vous n'êtes pas informaticien, voici comment tester :

### 1. Installer les programmes nécessaires

```bash
pip install -r requirements.txt
```
*Ou, pour installer seulement ce qu'il faut pour un module :*
```bash
pip install kivy pinpong paho-mqtt getmac
```

### 2. Lancer un module (exemple)

- **Pour voir les mesures sur un écran graphique UniHiker** :
  ```bash
  cd Capteur_TVOC_CO2_Bilal_etudiant_2/projet_plus_récent_fini/kivy_application_tvoc_co2_bilal/modele_mvc
  python main.py
  ```
- **Pour tester le capteur simplement (texte, UniHiker)** :
  ```bash
  cd Capteur_TVOC_CO2_Bilal_etudiant_2/physique_CCS811
  python physique_co2_tvoc_ccs811.py
  ```
- **Pour tester l'envoi sur Internet (UniHiker)** :
  ```bash
  cd Capteur_TVOC_CO2_Bilal_etudiant_2/test_mqtt_simple_basique
  python Comunication_CCS811_V2.py
  ```

---

## 🖼️ **Schéma de Fonctionnement**

```text
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
- Les résultats s'affichent sur l'écran UniHiker (avec des couleurs et des alertes)
- Si l'air devient mauvais, une lumière ou un gyrophare s'allume
- Les mesures sont envoyées sur Internet pour être consultées à distance

---

## 👨‍💻 **Contributeurs**

- **Bilal** – Capteur TVOC/CO₂, interface graphique, documentation
- **Lenny** – Capteur de poussières PM, intégration particules fines
- **Mathieu** – Alarmes, gyrophare, alertes visuelles

---

## 🛠️ **Technologies Utilisées**

- **Python** (le langage principal)
- **Kivy** (pour l'affichage graphique)
- **MQTT** (pour envoyer les mesures sur Internet)
- **PinPong** (pour communiquer avec les capteurs)
- **UniHiker** (petit ordinateur avec écran tactile)
- **getmac** (pour identifier l'appareil sur le réseau)

---

## 🔒 **Sécurité et bonnes pratiques**

- Les échanges Internet ne sont pas chiffrés par défaut (pour les tests)
- Pour plus de sécurité, activez le chiffrement (TLS/SSL) et protégez vos mots de passe
- Mettez à jour régulièrement les programmes et la carte UniHiker
- Protégez l'accès physique aux capteurs

---

## 📝 **Licence du Projet**

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

## 📄 **Licences des Outils Utilisés**

- **Python** : PSF License ([voir](https://docs.python.org/3/license.html))
- **Kivy** : MIT ([voir](https://github.com/kivy/kivy/blob/master/LICENSE))
- **paho-mqtt** : Eclipse Public License v2.0 ([voir](https://www.eclipse.org/legal/epl-2.0/))
- **PinPong** : MIT ([voir](https://github.com/DFRobot/pinpong/blob/master/LICENSE))
- **getmac** : MIT ([voir](https://github.com/ghostofgoes/getmac))
