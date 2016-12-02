-----------------------------------------------------------------------------------------------
__ATTENTION: Ce programme est actuellement en cours de développement et n'a pas vocation à être utilisé.__
-----------------------------------------------------------------------------------------------
# PyJoke
Programme écrit en Python permettant d'effectuer des actions à l'insu d'un utilisateur pour lui faire une blague.

Actuellement le programme permet :
* d'ouvrir des fenêtres avec des images
* de jouer des sons
* d'ouvrir le lecteur CD

## Dépendances (Python2.7):
* Tkinter
* pygame
* PIL
* docopt

# Utilisation
- **SERVER.py** Démarre le serveur
- **CLIENT.py** Permet de se connecter à un serveur PyJoke

# Configuration du serveur
Le fichier **config.json** contient la configuration du serveur:
```json
{
  "PORT": 2048,
  "PASSWORD": "password",
  "IMAGES_DIR": "img/",
  "SOUNDS_DIR": "sound/",
  "CMDIDSIZE": 8,
  "SALTSIZE": 8,
  "TIMEOUT": 5,
  "NTWBUFSIZE": 2048,
  "WINDOWS_POSUPDATEINTERVAL": 300
}
```
```PASSWORD```  est le mot de passe utilisé par le serveur

```PORT```      est le port en écoute sur le serveur

```WINDOWS_POSUPDATEINTERVAL``` est l'interval (ms) entre deux changements de position d'une fenêtre
