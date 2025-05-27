# Marais'R'Sense

Bienvenue dans **Marais'R'Sense** !  
Ce projet permet de surveiller la qualité de l'air à l'aide de capteurs connectés et intègre des fonctionnalités avancées.

---

## 🌍 À quoi sert ce projet ?

- **Mesure de la qualité de l'air** : Capteurs **TVOC, CO₂, PM10 et PM2.5**.
- **Affichage et interface utilisateur** : Utilisation de **Kivy** pour une présentation intuitive.
- **Communication des données** : Envoi des mesures via **MQTT** pour une transmission efficace.
- **Alarmes et alertes** : **Gyrophare, relais et alarmes visuelles** pour signaler des niveaux critiques.

---

## 🚀 Comment utiliser Marais'R'Sense ?

1. **Installez Python 3.10 ou plus récent** sur votre ordinateur.
2. **Installez les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
   > Cette commande utilise l'outil **pip** pour installer automatiquement toutes les bibliothèques Python listées dans le fichier `requirements.txt` nécessaires au bon fonctionnement du projet.
   > Ouvre un terminal (ou l'invite de commandes), place-toi dans le dossier du projet avec `cd chemin/vers/Maraisrsense`, puis copie-colle cette commande et appuie sur Entrée.
3. **Lancez l'application** :
   ```bash
   python main.py
   ```
4. **Surveillez les mesures en temps réel** et recevez des alertes en cas de seuil critique.

---

## 🔧 Fonctionnalités principales

- **Affichage des niveaux de TVOC, CO₂, PM2.5 et PM10**.
- **Interface utilisateur** simplifiée grâce à **Kivy**.
- **Alarmes automatiques** via gyrophare et relais.
- **Envoi automatique des données** au serveur MQTT.
- **Mise à jour des valeurs** en temps réel.

---

## 🖼️ Schéma de fonctionnement

```
+-------------------+         +-------------------+         +-------------------+
|   Capteurs TVOC   |         |    Interface      |         |    Serveur MQTT   |
|   CO₂, PM2.5,     | ----->  |    Utilisateur    | ----->  |   (Cloud/local)   |
|   PM10            |         |    (Kivy)         |         |                   |
+-------------------+         +-------------------+         +-------------------+
         |                            |                              |
         |                            v                              |
         |                  +-------------------+                   |
         |                  |   Alarmes &       | <-----------------+
         +----------------> |   Gyrophare       |
                            +-------------------+
```

- **Les capteurs** mesurent la qualité de l'air (TVOC, CO₂, PM2.5, PM10).
- **L'interface utilisateur** affiche les mesures en temps réel.
- **Les alarmes** (gyrophare, relais) se déclenchent en cas de seuil critique.
- **Les données** sont envoyées automatiquement au serveur MQTT.

---

## 📖 Contributeurs

- **Bilal** - Développement du capteur TVOC
- **Lenny** - Développement du capteur PM
- **Mathieu** - Alarmes et gyrophare (alarmes visuelles)

---

## 🛠 Technologies utilisées

- **Python** - Langage principal du projet
- **MQTT** - Communication des données capteurs
- **Kivy** - Interface utilisateur graphique
- **PinPong** - Contrôle des capteurs et interaction
- **Unihiker** - Intégration matérielle microcontrôleur tactile avec écran

---

## 📝 Licence

Ce projet est sous licence MIT. Voir la [licence ci-dessous](#licence-mit) pour plus d'informations.

---

## Licence MIT

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

---

_Readme créé par Bilal._
