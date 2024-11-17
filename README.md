# Simulation de Boids avec **Pygame**

## Description
Ce projet implémente une simulation interactive de **boids** (comportement d'essaim) en utilisant **Python** et la bibliothèque **Pygame**. Les boids sont des agents simulant des comportements collectifs tels que les vols d'oiseaux ou les bancs de poissons en suivant des règles simples d'alignement, de cohésion et de séparation.

L'interface offre plusieurs outils interactifs permettant de modifier les paramètres de la simulation en temps réel.

## Fonctionnalités

### 🐦 **Simulation réaliste**
- **Interactions basées sur trois comportements :**
  1. **Séparation** : éviter les collisions avec les voisins proches.
  2. **Alignement** : suivre la direction moyenne des voisins.
  3. **Cohésion** : se rapprocher du centre de masse du groupe.

- **Mouvement fluide** : limitation de la vitesse de rotation pour des trajectoires naturelles.

### 🎛️ **Interface utilisateur interactive**
- **Sliders** : ajustez les paramètres des boids (angle de vision, rayons d'alignement, séparation et cohésion).
- **Boutons** :
  - `+` : ajouter un boid.
  - `-` : retirer un boid.
  - `Clear` : réinitialiser tous les boids.
  - `Pause` : mettre en pause ou reprendre la simulation.
  - `Show/Hide` : afficher ou masquer les zones de vision.

### 🎨 **Affichage des interactions**
Chaque boid change de couleur en fonction du comportement dominant :
- **Alignement** : rose.
- **Cohésion** : rose clair.
- **Séparation** : violet.


## Prérequis

- **Python** 3.9+
- **Pygame** 2.0+

### Installation des dépendances
Pour installer les bibliothèques nécessaires, exécutez la commande suivante :

```bash
pip install pygame
```

## 💻 **Utilisation**

1. **Clonez ou téléchargez ce dépôt :**
   ```bash
   git clone https://github.com/votre-utilisateur/simulation-boids.git
   cd simulation-boids
   ```

2. Lancez le script principal :
   ```bash
   python boids_simulation.py
   ```

3. Interagissez avec l'interface :

- **Sliders** : ajustez les paramètres des boids.
- **Boutons** :
  - `+` : ajoute un boid.
  - `-` : retire un boid.
  - **Clear** : réinitialise tous les boids.
  - **Pause** : met en pause/reprend la simulation.
  - **Show/Hide** : affiche ou masque les zones de vision.

## 📂 **Structure du code**
**Classe** `Boid`:

- Classe représentant chaque agent avec ses propriétés (position, vitesse, accélération) et comportements.
- Méthodes principales :
   - `apply_behaviors` : applique les forces d'alignement, de cohésion et de séparation.
   - `update` : met à jour la position et la direction.
   - `draw` : dessine le boid à l'écran.
- Interface utilisateur :
   - **Sliders** : contrôle des paramètres en temps réel.
   - **Boutons** : ajout, suppression ou réinitialisation des boids.
- **Boucle principale** :
   Gère l'affichage, les événements utilisateurs et la mise à jour des boids.

## 🌀 **Scénarios d'interaction**

1. Comportements simples :

    Les boids se dirigent vers des groupes proches tout en évitant les collisions.

2. Changements dynamiques :

    - Ajustez le rayon d'alignement pour observer des comportements plus dispersés ou compacts.
    - Augmentez l'angle de vision pour voir les boids réagir à des voisins plus éloignés.

3. Ajout et suppression: 

    - Ajoutez des boids pour observer comment les nouveaux agents s'intègrent au groupe.
    - Supprimez des boids pour voir comment cela affecte la structure.

## 🔧 **Améliorations possibles**


- Ajouter un prédateur pour chasser les boids.
- Intégrer des obstacles que les boids doivent éviter.
- Exporter des animations sous forme de fichiers vidéo.

## 📜 **Licence**
Ce dépôt est privé. Toute utilisation, modification ou redistribution sans autorisation explicite est interdite. Veuillez consulter le fichier `LICENSE` pour plus d'informations.

## 👨‍💻 **Auteurs**

> AHMED SALAH ALI Adham
> ELAYOUBI Hadi
> AIBOUD Lyes
