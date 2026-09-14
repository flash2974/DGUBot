# DGUBot


Ce dépôt contient le code source de DGUBot, un bot Discord multifonctions développé aux alentours de 2023. Codé en Python, il propose une multitudes de fonctionnalités, en utilisant beaucoup de fonctionnalités offertes par `discord.py`, notamment les boutons, les interfaces pop-up, etc.
Le bot est fonctionnel, mais pas vraiment destiné à un usage réel. C'est plutôt une archive de mon tout premier projet de programmation.

Ses fonctionnalités les plus anecdotiques incluent :
- Si un message contient "quoi", le bot répond "FEUR" et ajoute une réaction 💇
- Il ajoute une réaction 👋 aux messages contenant "bonjour", "salut", "hey", etc
- Il transmet tous les messages reçus en MP à l'admin du serveur


## À propos du projet

DGUBot est volontairement conservé dans son état d'origine autant que possible. Les seules modifications apportées ont principalement consisté à le transformer en module et à ajouter son déploiement avec `uv`. Son architecture et son style de code ne correspondent plus nécessairement à mes pratiques actuelles : il s'agit d'un projet historique, et non d'un projet destiné à servir de référence technique.

Avec environ 2 200 lignes de Python, il représente néanmoins une étape importante de mon apprentissage : manipulation d'une API, programmation événementielle, interfaces interactives, traitement d'images, tâches asynchrones et persistance de données.

Le dépôt est donc principalement conservé comme une trace de mes débuts en programmation.


### Liste des commandes

**Jeux**

* `/blind_test [url] [temps_musique]`
Permet de lancer une partie de blind test à partir d'une playlist YouTube ou YouTube Music. Un menu interactif avec des boutons permet de gérer le téléchargement en direct, la lecture, et la mise en pause de la musique. Le bot gère le chronomètre, attribue les points si les joueurs trouvent le titre et/ou l'auteur, et déclare le gagnant à la fin.


* `/justeprix`
Lance le mini-jeu du Juste Prix. Un menu initial permet de gérer la base de données locale (créer, supprimer ou lister des objets avec leurs prix) ou de jouer. En mode jeu, le joueur doit d'abord deviner le prix exact grâce à des indices de "chaleur" 🌡️, puis trouver le nom de l'objet mystère.


* `/telephone`
Lance le jeu du Téléphone, basé sur la cryptographie des vieux claviers T9 (type Nokia). Il possède un menu complet pour ajouter, supprimer, lister les codes, ou lancer la partie. Le joueur doit deviner le code chiffré associé à un mot, puis le mot lui-même.


* `/aide_pendu [mot]`
Cherche des lettres au jeu du pendu de manière automatisée. L'algorithme fouille un dictionnaire local et renvoie la lettre manquante qui possède la plus grande probabilité d'apparaître dans le mot donné (en remplaçant les lettres inconnues par des étoiles `*`).


* `/blague [type]`
Renvoie une blague extraite aléatoirement du site *top-blagues.com* en fonction de la thématique sélectionnée (Informatique, Devinettes, etc.). Le résultat est affiché dans un embed contenant la blague, le lien source, et une couleur spécifique à la catégorie choisie.

**Trucs fun**

* `/img2emoji [taille_max] [dither]`
Transforme une image en une mosaïque d'emojis carrés natifs de Discord. La commande crée un fil de discussion (thread) demandant à l'utilisateur d'y déposer l'image ou son URL. L'image est redimensionnée, et ses couleurs sont converties selon une palette définie correspondant aux emojis de la plateforme.


* `/info_membre [membre]`
Donne des informations sur un membre du serveur. La commande génère un embed affichant la date de création du compte, attribue un "amoureux" factice choisi aléatoirement sur le serveur, et injecte une fausse photo de visage humain (générée par IA via *thispersondoesnotexist.com*).


* `/classement`
Affiche le classement en direct des 10 membres les plus actifs du serveur, calculé grâce au système interne de points de participation (qui ajoute 1 point à chaque message envoyé par un utilisateur).



**Divers**

* `/activer_twitter [enable]`
Active ou désactive une boucle de vérification automatique des nouveaux tweets du profil configuré (via le scraper `ntscraper`). Les liens récupérés sont transformés avec le préfixe `fx` (fxtwitter) pour forcer le bon affichage de l'intégration vidéo/image dans Discord.


* `/activer_youtube [enable]`
Active ou désactive la tâche de vérification automatique des nouvelles vidéos YouTube d'une chaîne spécifique. Si une vidéo est postée, le bot s'occupe d'envoyer un message d'alerte avec une mention globale `@everyone`.


* `/stop`
Commande de fermeture d'urgence. Elle publie le fichier texte contenant les données utilisateurs (`user.txt`) avant de stopper le processus système du bot et de le déconnecter.

* `/help`
Affiche une présentation simplifiée et un résumé textuel des commandes principales du bot.

## Requirements
- Python3
- uv
- FFmpeg