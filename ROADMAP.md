# Roadmap

Cette roadmap decoupe le projet en petites evolutions faciles a developper, tester et pousser separement.

## Ameliorations fonctionnelles

- [x] Ajouter un menu deroulant pour choisir le pilote
- [x] Ajouter plus de Grands Prix disponibles
- [x] Ajouter les saisons 2024 et 2025
- [x] Afficher le temps du tour le plus rapide
- Comparer deux pilotes sur le meme graphique
- Ajouter un graphique throttle/brake
- Ajouter un graphique RPM/vitesse
- Ajouter une vue des secteurs du tour
- Afficher un tableau recapitulatif des meilleurs tours
- Ajouter une gestion plus fine des sessions sprint

## Qualite projet

- Ajouter des tests unitaires sur les fonctions de preparation des donnees
- [x] Separer la logique FastF1 dans un module `telemetry.py`
- Ajouter une configuration Streamlit dans `.streamlit/config.toml`
- Ajouter un workflow GitHub Actions de verification syntaxique
- Ajouter un formatage automatique avec Ruff
- Ajouter un type checking leger avec mypy

## Experience utilisateur

- [x] Ajouter un message clair quand FastF1 ne trouve pas une session
- Ajouter des explications courtes sur les abreviations de session
- [x] Ajouter une option pour telecharger les donnees du tour en CSV
- Ajouter un theme visuel coherent avec la F1
- [x] Ajouter des indicateurs de chargement plus precis
