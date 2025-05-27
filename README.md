
```bash
#!/bin/bash

# Noms des fichiers
README_FILE="README.md"
LICENSE_FILE="LICENSE" # Tu peux aussi l'appeler LICENSE.txt ou LICENSE.md si tu préfères

# --- Contenu du README.md ---
cat <<EOL_README > $README_FILE
# Maraisrsense

Bienvenue dans **Maraisrsense** !
Ce projet permet de surveiller la qualité de l'air à l'aide de capteurs connectés et intègre des fonctionnalités avancées.

---

## 🌍 À quoi sert ce projet ?

- **Mesure de la qualité de l'air** : Capteurs **TVOC, CO₂, PM10 et PM2.5**.
- **Affichage et interface utilisateur** : Utilisation de **Kivy** pour une présentation intuitive.
- **Communication des données** : Envoi des mesures via **MQTT** pour une transmission efficace.
- **Alarmes et alertes** : **Gyrophare, relai et alarmes visuelles** pour signaler des niveaux critiques.

---

## 🚀 Comment utiliser Maraisrsense ?

1. **Installez Python 3.10 ou plus récent** sur votre ordinateur.
2. **Installez les dépendances** :
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`
3. **Lancez l'application** :
   \`\`\`bash
   python main.py
   \`\`\`
4. **Surveillez les mesures en temps réel** et recevez des alertes en cas de seuil critique.

---

## 🔧 Fonctionnalités principales

- **Affichage des niveaux de TVOC, CO₂ et PM 2,5 et 10**.
- **Interface utilisateur** simplifiée grâce à **Kivy**.
- **Alarmes automatiques** via gyrophare et relai.
- **Envoi automatique des données** au serveur MQTT.
- **Mise à jour des valeurs** en temps réel.

---

## 📂 Structure du projet

\`\`\`
Maraisrsense/
│── Capteur_TVOC/
│   ├── capteur.py
│   ├── README.md
│── main.py
│── requirements.txt
│── README.md
│── LICENSE  <-- Ce fichier sera lié
\`\`\`

---

## 📖 Contributeurs

- **Bilal** - Développement du capteur TVOC
- **Lenny** - Développement du capteur PM
- **Mathieu** - Alarme et gyrophare (alarmes visuelles)

---

## 🛠 Technologies utilisées

- **Python** - Langage principal du projet
- **MQTT** - Communication des données capteurs
- **Kivy** - Interface utilisateur graphique
- **PinPong** - Contrôle des capteurs et interaction
- **Unihiker** - Intégration matérielle micro controleur tactile avec ecran.

---

## 📝 Licence

Ce projet est sous licence MIT. Voir [LICENSE]($LICENSE_FILE) pour plus d'informations.

EOL_README

# --- Contenu du LICENSE (MIT) ---
# IMPORTANT : Vérifiez et adaptez [nom complet des détenteurs du copyright]
# ci-dessous par les informations correctes pour votre projet !
YEAR="2025" # Année fixée à 2025
COPYRIGHT_HOLDERS="Bilal, Lenny, Mathieu" # À adapter si besoin !

cat <<EOL_LICENSE > $LICENSE_FILE
MIT License

Copyright (c) $YEAR $COPYRIGHT_HOLDERS

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
EOL_LICENSE

```
