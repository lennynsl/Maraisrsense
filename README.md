#!/bin/bash

# Nom du fichier
README_FILE="README.md"

# Contenu du README.md
cat <<EOL > $README_FILE
# Maraisrsense

## 📌 Description
Maraisrsense est un projet de capteur **TVOC, CO₂, PM10 et PM2.5** conçu pour mesurer la qualité de l'air. Il permet de recueillir des données environnementales et de les analyser.  
Le projet intègre :
- **MQTT** pour la communication des données  
- **Kivy** pour l'interface utilisateur  
- **Alarme visuelle**, **gyrophare** et **relais** pour les alertes  

## 🚀 Installation
1. Clonez ce dépôt :
   \`\`\`bash
   git clone https://github.com/lennynsl/Maraisrsense.git
   cd Maraisrsense
   \`\`\`

2. Installez les dépendances requises :
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

## 🔧 Utilisation
Lancez le programme avec :
\`\`\`bash
python main.py
\`\`\`

## 📂 Structure du projet
\`\`\`
Maraisrsense/
│── Capteur_TVOC/
│   ├── capteur.py
│   ├── README.md
│── main.py
│── requirements.txt
│── README.md
│── LICENSE
\`\`\`

## 📖 Contributeurs
- **Bilal** - Développement du capteur TVOC  
- **Lenny** - Développement du capteur PM  
- **Mathieu** - Alarme et gyrophare (alarmes visuelles)  

## 📝 Technologies utilisées
- **MQTT** - Communication des données capteurs  
- **Kivy** - Interface utilisateur graphique  

## 📝 Licence
Ce projet est sous licence MIT. Voir [LICENSE](LICENSE) pour plus d'informations.

EOL

echo "README.md mis à jour avec succès ! 🚀"
