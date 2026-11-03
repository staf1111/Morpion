#  Morpion – Python & Pygame

Jeu de morpion (tic-tac-toe) à deux joueurs sur le même ordinateur, développé en **Python** avec la bibliothèque **Pygame**.

Projet commencé en terminale en version console, puis repris avec une interface graphique.

![Aperçu du jeu](apercu.png)

##  Fonctionnalités
- Partie à deux joueurs (X et O) à la souris
- Animation à l'apparition des symboles
- Aperçu du symbole au survol d'une case vide
- Ligne animée sur l'alignement gagnant
- Détection des victoires (lignes, colonnes, diagonales) et du match nul
- Tableau des scores conservé entre les parties
- Bouton « Rejouer » (ou touche **R**)

## Technologies
- **Python 3**
- **Pygame** : affichage, gestion des événements souris/clavier, boucle de jeu à 60 FPS
- **Programmation orientée objet** :
  - `Morpion` : logique du jeu (plateau, tours, détection de fin de partie)
  - `Interface` : affichage et interactions avec Pygame

## Installation et lancement

1. Installer [Python 3](https://www.python.org/downloads/)
2. Installer Pygame :
   ```bash
   pip install pygame
   ```
3. Lancer le jeu :
   ```bash
   python morpion.py
   ```

## 🕹️ Commandes
| Action | Commande |
|---|---|
| Jouer un coup | Clic gauche sur une case |
| Nouvelle partie | Bouton « Rejouer » ou touche **R** |
| Quitter | Fermer la fenêtre |

## 📌 Évolutions possibles
- Mode un joueur contre l'ordinateur (algorithme minimax)
- Sons et musique
- Choix des couleurs et des noms des joueurs

---
