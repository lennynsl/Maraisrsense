# SuiviAirMenuiserieApp

Bienvenue !  
Cette application vous permet de surveiller facilement la qualité de l'air autour de vous grâce à un capteur connecté.

---

## À quoi sert cette application ?

- **Afficher la qualité de l'air** : Vous voyez en temps réel le taux de CO2 (en ppm) et de TVOC (en ppb).
- **Voir l'adresse MAC** : Un bouton vous permet d'afficher l'adresse MAC de votre appareil.
- **Envoi automatique** : Les mesures sont envoyées toutes les 10 minutes à un serveur (broker MQTT).
- **Aide intégrée** : Un message d'accueil et des alertes vous guident si un problème survient (capteur non détecté, etc.).

---

## Comment utiliser l'application ?

1. **Installez Python 3.10 ou plus récent** sur votre ordinateur.
2. **Installez les dépendances** :
   - Ouvrez un terminal dans ce dossier.
   - Tapez : `pip install kivy getmac paho-mqtt`
3. **Lancez l'application** :
   - Dans le terminal, tapez :  
     `python suiviairmenuiserieapp/main.py`
4. **Utilisez l'application** :
   - L'écran principal affiche les mesures de CO2 et TVOC.
   - Cliquez sur "Adresse MAC" pour voir l'adresse MAC de votre appareil.
   - Les valeurs sont mises à jour toutes les 8 secondes automatiquement.

---

## Fonctionnalités principales

- **Affichage en temps réel** des mesures de CO2 et TVOC.
- **Bouton "Adresse MAC"** pour afficher l'adresse réseau de votre appareil.
- **Alertes** si le capteur n'est pas détecté ou si un problème survient.
- **Envoi automatique** des données au serveur MQTT.
- **Interface simple** et adaptée aux débutants.

---

## Structure du projet

- `suiviairmenuiserieapp/main.py` : Point d'entrée de l'application.
- `suiviairmenuiserieapp/vues/` : Gère l'affichage (écrans, boutons, messages).
- `suiviairmenuiserieapp/modeles/` : Logique métier (gestion des mesures, capteur, etc.).
- `suiviairmenuiserieapp/ccs811_mqtt_projetclasses/communication_mqtt_ccs811.py` : Communication avec le serveur MQTT.

---

## Méthodes, fonctions et attributs principaux

### Exemple (à adapter selon votre code) :

- **Classe `MainApp`** (dans `main.py`)
  - `build()` : Lance l'application et affiche l'écran principal.
- **Classe `CapteurCCS811`** (dans `modeles/capteur_ccs811.py`)
  - `lire_co2()` : Retourne la valeur actuelle de CO2.
  - `lire_tvoc()` : Retourne la valeur actuelle de TVOC.
  - Attributs : `co2`, `tvoc`, `etat_capteur`.
- **Classe `CommunicationMQTT`** (dans `communication_mqtt_ccs811.py`)
  - `envoyer_mesures(co2, tvoc)` : Envoie les mesures au serveur.
  - Attributs : `client`, `topic`.

*Pour plus de détails, consultez les commentaires dans chaque fichier source.*

---

## Conseils pour bien démarrer

- **Navigation** : Utilisez les boutons à l'écran pour accéder aux fonctions.
- **Aide** : Un message d'accueil s'affiche en haut de l'application.
- **Problème de capteur** : Un message d'erreur s'affiche en rouge si le capteur n'est pas détecté.
- **Arrêt** : Fermez la fenêtre pour quitter l'application.
- **Affichage** : Les valeurs sont mises à jour toutes les 8 secondes.
- **Envoi des données** : Automatique toutes les 10 minutes.

---

## Historique des versions

- **v1.0.0** : Première version (affichage CO2/TVOC, envoi MQTT, interface simple).
- **v1.1.0** : Gestion dynamique du capteur, documentation améliorée.
- **v1.2.0** : Nettoyage du code, simplification pour l'utilisateur.
- **v1.3.0** : Ajout d'un guide utilisateur, labels d'aide, README enrichi.
- **v1.4.0** : README simplifié, explications détaillées, vocabulaire accessible.

---

## Besoin d'aide ?

Si vous avez une question ou un souci, relisez ce fichier ou consultez les commentaires dans le code.  
Bonne utilisation !
