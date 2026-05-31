# F1 Telemetry Tracker

F1 Telemetry Tracker est une application Streamlit qui utilise FastF1 pour explorer la telemetrie d'un tour rapide en Formule 1.

L'application permet de selectionner une saison, un Grand Prix, une session et un pilote, puis affiche la vitesse du tour le plus rapide en fonction de la distance parcourue.

## Apercu

Fonctionnalites principales :

- selection des saisons 2022, 2023, 2024 et 2025
- selection de plusieurs Grands Prix du calendrier F1
- selection du type de session : course, qualifications, essais libres, sprint
- selection du pilote
- chargement des donnees via FastF1 avec cache local
- affichage du temps du tour le plus rapide
- graphique vitesse / distance avec Matplotlib
- export CSV des donnees de telemetrie
- gestion d'erreurs basique pour les sessions ou pilotes indisponibles

## Prerequis

- Python 3.10 ou plus recent
- Une connexion internet au premier chargement des donnees FastF1

## Installation

Clone le projet, puis installe les dependances dans un environnement virtuel :

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Lancement

```bash
streamlit run app.py
```

Streamlit ouvrira ensuite l'application dans le navigateur.

## Utilisation

Dans la barre laterale :

1. Choisis une annee.
2. Choisis un Grand Prix.
3. Choisis une session.
4. Choisis un pilote.

L'application charge alors la session FastF1, recupere le tour le plus rapide du pilote selectionne et affiche :

- le temps du tour
- le numero du tour
- la courbe de vitesse en fonction de la distance
- un bouton pour telecharger les donnees en CSV

## Cache FastF1

FastF1 stocke les donnees dans le dossier local :

```text
./cache
```

Ce dossier est ignore par Git, car il peut contenir beaucoup de fichiers generes automatiquement.

## Structure du projet

```text
.
├── app.py
├── README.md
├── ROADMAP.md
├── requirements.txt
└── .gitignore
```

## Roadmap

Les prochaines ameliorations possibles sont listees dans `ROADMAP.md`.

Exemples :

- comparer deux pilotes sur le meme graphique
- ajouter throttle / brake
- ajouter RPM / vitesse
- separer la logique FastF1 dans un module dedie
- ajouter un workflow GitHub Actions
