# Changelog

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
et ce projet adhère au [Versionnage Sémantique](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-04-03

### Ajouté
- Initialisation du module **paygate-africa**.
- Implémentation du provider **CinetPay** (Redirection).
- Implémentation du provider **Kkiapay** (Widget JS).
- Système de **Factory** pour le chargement dynamique et asynchrone des clients.
- Utilisation des **Protocols Python** (Duck Typing) pour l'interface `Transaction`.
- Validation de la configuration via des classes `Settings` autonomes.
- Documentation complète générée avec **MkDocs** (Material theme).
- Suite de tests unitaires avec **Pytest** et mocks pour les appels réseau.
- Configuration de linting et formatage avec **Ruff**.
- Workflows **GitHub Actions** pour la CI/CD (Tests + Publication PyPI + Déploiement Docs).
- Philosophie "**Zero Dependency**" (Utilisation exclusive de la librairie standard).

---
[0.1.0]: https://github.com/flavien-hugs/paygate-africa/releases/tag/v0.1.0
