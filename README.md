# DGUBot


This repository contains the source code for DGUBot, a multi-purpose Discord bot developed between 2022 and 2024, without AI (i spent way too many hours on this!). I used `discord.py` library to offer multiple (useless/fun) features.
While the bot is functional, it is not intended for actual, practical use. It serves primarily as an archive of my very first programming project.

Some of its more trivial features include:
- If a message contains "quoi" (what), the bot replies "FEUR" and adds a 💇 reaction (this is a famous joke in french, "quoi" meaning "what?" and "quoi+feur" meaning "barber").
- It adds a 👋 reaction to messages containing greetings like "bonjour," "salut," "hey," etc.
- It forwards all direct messages (DMs) received by the bot to the server administrator.


## About the Project

DGUBot has been kept as close to its original state as possible. The only modifications made were to convert it into a module and set up its deployment using `uv`. Its architecture and coding style do not necessarily reflect my current practices; this is a historical project, not one intended to serve as a technical reference.

Comprising approximately 2,200 lines of Python, it represents a significant milestone in my learning journey—covering API interaction, event-driven programming, interactive interfaces, image processing, asynchronous tasks, and data persistence.

The repository is therefore preserved mainly as a record of my early days in programming.


### List of Commands

**Games**

* `/blind_test [url] [music_duration]`
Starts a "blind test" (music guessing game) using a YouTube or YouTube Music playlist. An interactive menu with buttons allows for managing live downloads, playback, and pausing the music. The bot manages the timer, awards points if players correctly identify the title and/or author, and declares the winner at the end.


* `/justeprix`
Launches the "Price is Right" mini-game. An initial menu allows you to manage the local database (create, delete, or list items and their prices) or start a game. In game mode, the player must first guess the exact price using "warmth" (proximity) hints 🌡️, and then identify the mystery item.


* `/telephone`
Launches the "Telephone" (T9) game, based on the keypad encoding used on old mobile phones (like Nokia). It includes a comprehensive menu for adding, removing, or listing codes, as well as starting a game. The player must guess the numeric code associated with a word, and then the word itself.


* `/aide_pendu [word]`
Automatically suggests letters for a game of Hangman. The algorithm searches a local dictionary and identifies the missing letter with the highest probability of appearing in the given word (where unknown letters are represented by asterisks `*`).


* `/blague [type]`
Retrieves a random joke from *top-blagues.com* based on a selected category (e.g., IT, riddles, etc.). The result is displayed in an embed containing the joke, the source link, and a color specific to the chosen category.

**Fun Features**

* `/img2emoji [max_size] [dither]`
Converts an image into a mosaic made of native Discord square emojis. The command creates a thread, prompting the user to upload an image or provide an image URL. The image is resized, and its colors are mapped to a palette corresponding to the platform's available emojis. * `/info_membre [member]`
Provides information about a server member. The command generates an embed displaying the account creation date, assigns a randomly selected "significant other" (chosen from other server members), and includes a AI-generated image of a human face (sourced from *thispersondoesnotexist.com*).


* `/classement`
Displays a live leaderboard of the 10 most active members on the server, calculated using an internal participation point system (which awards 1 point for every message sent by a user).



**Miscellaneous**

* `/activer_twitter [enable]`
Enables or disables an automated check for new tweets from a configured profile (using the `ntscraper` tool). Retrieved links are modified with an `fx` prefix (fxtwitter) to ensure that video and image previews display correctly within Discord.


* `/activer_youtube [enable]`
Enables or disables an automated check for new YouTube videos from a specific channel. If a new video is posted, the bot sends an alert message, including an `@everyone` mention.


* `/stop`
An emergency shutdown command. It exports the text file containing user data (`user.txt`) before terminating the bot's system process and disconnecting it.

* `/help`
Displays a brief overview and a text-based summary of the bot's primary commands.