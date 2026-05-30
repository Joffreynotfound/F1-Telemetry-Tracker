# F1 Telemetry Tracker

Application Streamlit permettant d'afficher la telemetrie FastF1 du tour le plus rapide d'un pilote sur un Grand Prix et une session donnes.

## Installation

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Lancement

```bash
streamlit run app.py
```

FastF1 stocke son cache local dans le dossier `./cache`, ignore par Git.

## Fonctionnalites actuelles

- Selection de l'annee 2022 ou 2023
- Selection du Grand Prix entre Monza et Silverstone
- Selection de la session entre course (`R`) et qualification (`Q`)
- Chargement FastF1 mis en cache via Streamlit
- Graphique vitesse/distance du tour le plus rapide de Verstappen
