---
Event Name: AWS Summit Paris 2026
Event Room: X
Event Link: X
CFP link: X
CFP Submission Deadline: X
CFP Submission Link: X
CFP Submission Status: APPROVED | REJECTED | EXPIRED
---

<br>
<br>

![](https://img.shields.io/badge/FORMAT-ÉTUDE%20DE%20CAS-%23ca8a04?style=flat-square)

# Maîtriser les tests unitaires Python avec Boto3

### Stratégies avancées pour simuler les appels SDK & API AWS

<br>

## Résumé (150-250 mots)

L'intégration avec les services AWS via Boto3 est facile — tester correctement cette intégration est une autre histoire. En réalité, de nombreuses équipes se retrouvent avec des tests lents et fragiles qui ciblent de vrais comptes AWS, nécessitent une configuration complexe ou sont tout simplement ignorés.

Cette présentation propose une approche pratique et conviviale pour les développeurs afin de tester les projets Python dépendant d'AWS. Nous commencerons par un rappel rapide des bases des tests unitaires en Python ; ensuite, nous aborderons le mocking en général, en mettant l'accent sur les différents types de "Test Doubles" et le moment où utiliser chacun d'entre eux. Enfin, nous partagerons une étude de cas réelle dans laquelle nous avons mis en œuvre des tests unitaires et des techniques de simulation pour nous assurer que notre code fonctionne comme prévu, sans avoir à cibler le véritable environnement AWS. Nous verrons comment de petits choix de conception et le typage peuvent rendre notre code cloud correct et considérablement plus facile à tester.

Les participants repartiront avec des modèles concrets, des exemples pratiques et un modèle mental clair pour tester le code basé sur AWS en toute confiance.

<br>

## Points clés à retenir

À partir de là, nous aborderons :

- Les tests unitaires et les différents types de doublures de test en Python avec Pytest.
- Comment configurer un projet Python utilisant le SDK AWS pour les tests unitaires avec Pytest ? (application de la règle "pas de réseau" pour les tests unitaires)
- Comment chaque doublure de test, combinée au typage statique, est utilisée pour simuler les services AWS. (unittest.mock, monkeypatch, boto3-stubs)
- "certificate-renewal-operator" : un projet réel basé sur AWS qui implémente des tests unitaires.
- Les bibliothèques existantes pour faciliter encore davantage les tests unitaires.

<br>

## Audience

### Cible

- Développeurs Python utilisant AWS
- Ingénieurs Backend / DevOps / Cloud
- Équipes confrontées à des tests lents ou peu fiables liés au cloud

### Niveau

- 200 Intermédiaire

### Prérequis

- Aucune expertise approfondie d'AWS n'est requise — les exemples restent ciblés et pratiques.
- Connaissance des packages/modules en Python
- Bases de la programmation Python

<br>

## Exigences

Aucune

<br>

## Extras

Les participants recevront :

- [x] Diapositives

<br>

## Mots-clés

`testing`, `Python`, `unittest`, `mock`, `AWS`, `boto3`

<br>
