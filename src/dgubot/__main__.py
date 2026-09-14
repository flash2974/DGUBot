import asyncio
import datetime
import os
import random
import sys
import time

import discord
from discord import app_commands
from discord.ext import commands, tasks

import dgubot.Classes as c
import dgubot.Fonctions as n
import dgubot.Fonctions2 as f
from dgubot import (
    API_KEY,
    CHANNEL_ID,
    CHANNEL_ID_TWITTER,
    ID,
    TOKEN,
    blind_test_play,
    ctrl_blind_test,
    idRole,
    serveur,
)

actualisation = 10

# Twitter
# f.init(ID)

# Discord
serveur_obj = discord.Object(id=serveur)


intents = discord.Intents().all()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("Bot lancé !")
    try:
        global start
        start = time.time()
        synced = await bot.tree.sync(guild=serveur_obj)
        print(f"{len(synced)} commande(s) synchronisée(s)")

    except Exception as e:
        print(e)


@bot.event
async def on_message(message: discord.Message):

    if len(message.mentions) > 0 and message.mentions[0].id == 1109564010958946385:
        if any(mot in message.content.lower() for mot in ["amour", "aime", "love"]):
            await message.reply("Je t'aime aussi 😘")
        elif f.bonjour(message.content.lower()):
            await message.reply("Hey 👋")

        elif any(mot in message.content.lower() for mot in ["con", "idiot"]):
            await message.reply("C'est celui qui dit qui est 😏")

        else:
            await message.reply(
                f"Hey {message.author.name} ! (je sais pas quoi dire d'autre :sob:)"
            )

    # Vérifie si le message est un DM et si le bot n'est pas l'auteur du message
    if isinstance(message.channel, discord.DMChannel) and message.author != bot.user:
        if message.author == bot.get_user(921740204094672906):
            if message.content.lower() == "temps":
                await message.author.send(
                    f"Fonctionne depuis {int(time.time() - start)}s, soit {int((time.time() - start) / 3600)}h"
                )
        else:
            await message.channel.send(
                "Hey, le message a été transmis à <@921740204094672906>"
            )
            user = bot.get_user(921740204094672906)
            await user.send(
                f"Nouveau message de <@{message.author.id}> ({message.author.name}) :\n {message.content}"
            )

    elif (
        isinstance(message.channel, discord.TextChannel) and message.author != bot.user
    ):
        f.ajout_points(message.author.id)
        if message.content.lower() == "quoi":
            await message.add_reaction("💇")
            await message.reply("FEUR")
        elif "dgubot" in message.content.lower():
            await message.reply(f"Hey <@{message.author.id}> !")
        elif "!points" in message.content.lower():
            await message.reply(
                f"Yop {message.author.name} tu as {f.lecture_points(message.author.id)} points^^"
            )
        elif "twopical" in message.content.lower():
            await message.channel.send("Jordan aka Twopical 🌴🥥")
        elif "linsaw est nul" in message.content.lower():
            await message.add_reaction("🤏")
        elif message.content.lower() == "uwu":
            await message.add_reaction("👉")
            await message.add_reaction("👈")

        if f.bonjour(message.content.lower()):
            await message.add_reaction("👋")


def a_les_droits():
    async def predicate(interaction: discord.Interaction):
        return interaction.user.id in [706296024326602762, 921740204094672906]

    return app_commands.check(predicate)


@bot.tree.command(
    # guild=serveur_obj,
    name="aide_pendu",
    description="Cherchez des lettres au pendu !",
)
async def pendu(interaction: discord.Interaction, mot: str):
    try:
        mots_trouves = n.recherche(mot)
        lettres = n.pourcentage_lettres(n.lettres_possibles(mot, mots_trouves))
        await interaction.response.send_message(
            content=f"La lettre la plus probable pour le mot {mot} est : {lettres[0]}",
            ephemeral=True,
        )
    except Exception as e:
        await interaction.response.send_message(e, ephemeral=True)


@bot.tree.command(
    # guild=serveur_obj,
    name="telephone",
    description="Jouer au téléphone",
)
async def telephone(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.followup.send(
        "Que voulez-vous faire ?", view=c.ChoixJeuTelephone(bot)
    )


@bot.tree.command(
    # guild=serveur_obj,
    name="help",
    description="Affiche la liste de toutes les commandes disponibles",
)
async def help(interaction: discord.Interaction):
    try:
        await interaction.response.defer()
        await interaction.followup.send(
            "# Commandes\n## Aide pour jeu\n* ** aide_pendu** : Cette commande prend en argument un mot incomplet (avec des étoiles * pour les lettres inconnues) et renvoie la lettre ayant le plus de chance d'être dans ce mot.\n## Aide\n* ** help** : Affiche l'aide.\n## Jeux\n* **blind_test** : Permet de jouer au blind test (avec une playlist YTMusic)\n* **justeprix** : Permet de jouer au juste prix (trouver le prix d'un objet par tatonnement)\n* **telephone** : Permet de jouer au téléphone (on doit trouver un mot avec son code sur un clavier type nokia)"
        )
    except Exception as e:
        await interaction.response.send_message(e, ephemeral=True)


@bot.tree.command(
    # guild=serveur_obj,
    name="justeprix",
    description="Jouer au jeu du Juste prix",
)
async def justeprix(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.followup.send(
        "Que voulez-vous faire ?", view=c.ChoixJustePrix(bot)
    )


@a_les_droits()
@bot.tree.command(
    # guild=serveur_obj,
    name="blind_test",
    description="Jouer au blind test",
)
@app_commands.describe(
    url="URL de la playlist",
    temps_musique="Temps de lecture par musique (en secondes), 30s par défaut",
)
async def blindtest(
    interaction: discord.Interaction, url: str, temps_musique: int = 30
):
    await interaction.response.defer()
    controle = discord.utils.get(interaction.guild.channels, id=ctrl_blind_test)
    blind_test = discord.utils.get(interaction.guild.channels, id=blind_test_play)

    await interaction.followup.send(
        "## MENU - Blind test\n📥 Lance le téléchargement des musiques\n⏯️ Bouton play/pause\n❌ Déconnecter le bot",
        view=c.Menu(controle, blind_test, url, temps_musique, bot, idRole, blind_test_play),
    )


@tasks.loop(minutes=actualisation)
async def verifNewTweet():
    try:
        tweet = await asyncio.to_thread(f.newTweet, ID)
    except Exception as e:
        now = datetime.datetime.now()
        with open("Data/ErrLogs.txt", "a") as file:
            file.write(f"{now.strftime('%d/%m/%Y %H:%M')} --> {e}\n")
            file.close()
        print(e)
        return

    else:
        print(f"Nouveau tweet : {tweet}")
        channel = bot.get_channel(CHANNEL_ID_TWITTER)

        if tweet[0]:
            for url in reversed(tweet[1]):
                await channel.send("Nouveau tweet !\n" + f.addFx(url))


@a_les_droits()
@bot.tree.command(
    # guild = serveur_obj,
    name="activer_twitter",
    description="Active la récupération automatique des tweets",
)
@app_commands.describe(enable="Activer ou désactiver")
async def members(interaction: discord.Interaction, enable: bool = True):
    if not a_les_droits():
        await interaction.response.send_message(
            content="T'as pas les droits pour faire ça (bruh)"
        )
    if enable:
        await interaction.response.send_message(
            content="Récupération automatique des tweets : `activée`", delete_after=5
        )
        await verifNewTweet.start()  # start la task ligne 37

    else:
        await interaction.response.send_message(
            content="Récupération automatique des tweets : `désactivée`", delete_after=5
        )
        verifNewTweet.cancel()


@tasks.loop(minutes=actualisation)
async def verifNewVideo():
    try:
        video = await yt.newVideo()
    except Exception:
        return

    else:
        print(f"Nouvelle vidéo : {video}")
        channel = bot.get_channel(channel_id_yt)
        if video[0]:
            await channel.send(
                "Hey toi 😎 ! Oui toi là qui lis ce message, viens dire bonjour 😱 ! Aller on t’attend 👀 !\n|| @everyone || \n"
                + video[1]
            )


@a_les_droits()
@bot.tree.command(
    # guild = serveur_obj,
    name="activer_youtube",
    description="Active la récupération automatique des vidéos youtube",
)
@app_commands.describe(enable="Activer ou désactiver")
async def members(interaction: discord.Interaction, enable: bool = True):
    if not a_les_droits():
        await interaction.response.send_message(
            content="T'as pas les droits pour faire ça (bruh)"
        )
    if enable:
        await interaction.response.send_message(
            content="Récupération automatique des vidéos : `activée`", delete_after=5
        )

        global yt
        yt = f.YTStats(API_KEY, CHANNEL_ID)
        await verifNewVideo.start()  # start la task ligne 37
    else:
        await interaction.response.send_message(
            content="Récupération automatique des vidéos : `désactivée`", delete_after=5
        )
        verifNewVideo.cancel()


@bot.tree.command(
    # guild=serveur_obj,
    name="classement",
    description="Classement des membres les plus actifs",
)
async def classement(interaction: discord.Interaction):
    classement = f.classement()
    res = "## Classement des 10 membres les plus actifs\n"
    i = 0
    for user, points in classement.items():
        name = bot.get_user(user).name
        res += f"{name} : {points} points\n"
        i += 1

        if i == 10:
            break
    await interaction.response.send_message(content=res)


@a_les_droits()
@bot.tree.command(
    # guild=serveur_obj,
    name="stop",
    description="Arrête le bot",
)
async def stop(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Arrêt du bot", file=discord.File("Data/user.txt")
    )
    await bot.close()
    sys.exit()


@app_commands.choices(
    type=[
        app_commands.Choice(name="Divers", value="divers"),
        app_commands.Choice(name="Blondes", value="blonde"),
        app_commands.Choice(name="Belges", value="belges"),
        app_commands.Choice(name="Animaux", value="animaux"),
        app_commands.Choice(name="Couples", value="couples"),
        app_commands.Choice(name="Devinettes", value="devinettes"),
        app_commands.Choice(name="Stupides", value="stupides"),
        app_commands.Choice(name="Mr et Mme...", value="mr et mme"),
        app_commands.Choice(name="Actualités", value="actualites"),
        app_commands.Choice(name="Informatique", value="informatique"),
        app_commands.Choice(name="Contrepeteries", value="contrepeteries"),
        app_commands.Choice(name="Pour enfants", value="pour enfants"),
        app_commands.Choice(name="Fêtes", value="fetes"),
    ]
)
@bot.tree.command(
    # guild=serveur_obj,
    name="blague",
    description="Renvoie des blagues !",
)
async def user(interaction: discord.Interaction, type: app_commands.Choice[str]):
    try:
        blague, url, color = f.blague(type.value)
    except Exception:
        await interaction.response.send_message(
            "Erreur. Veuillez réessayer", ephemeral=True
        )
    else:
        embed = discord.Embed(
            title=f"Blague ```{type.name}```",
            url=url,
            colour=color,
            timestamp=datetime.datetime.now(),
        )

        if blague == None:
            embed.add_field(name="Erreur", value="Aucune blague trouvée", inline=False)
        else:
            embed.add_field(name="Blague", value=blague, inline=False)
        await interaction.response.send_message(embed=embed)


@bot.tree.command(
    # guild=serveur_obj,
    name="img2emoji",
    description="Transforme une image en emojis carrés",
)
@app_commands.describe(
    taille_max="Taille maximum (en longueur ou largeur) de l'image-emoji à renvoyer",
    dither="Active ou désactive le dithering",
)
async def useruu(
    interaction: discord.Interaction, taille_max: int = 20, dither: bool = False
):

    await interaction.response.defer()

    # Créer un thread
    thread: discord.Thread = await interaction.channel.create_thread(
        name="Déposer l'image ici"
    )
    await thread.add_user(interaction.user)

    await thread.send(
        f"{interaction.user.mention} envoie l'image ici (message discord) ou url"
    )
    try:
        mess: discord.Message = await bot.wait_for(
            "message",
            timeout=60,
            check=lambda message: (
                message.channel == thread and message.author == interaction.user
            ),
        )

    except TimeoutError:
        await interaction.followup.send(
            f"Temps écoulé. Veuillez réessayer.\n||{interaction.user.mention}||"
        )
        await asyncio.sleep(2)
        await thread.delete()

    else:
        if mess.attachments:  # Vérifie si le message a des pièces jointes
            for attachment in mess.attachments:  # Parcourt toutes les pièces jointes
                if attachment.filename.endswith(
                    (".png", ".jpg", ".jpeg")
                ):  # Vérifie si la pièce jointe est une image
                    await attachment.save(attachment.filename)
                    await thread.send("UwU merci !!")
                    filename = attachment.filename
                    await asyncio.sleep(1)

        elif mess.content.startswith("https"):
            url = mess.content

            try:
                filename = f.download_image(url)
                await thread.send("UwU merci !!")
                await asyncio.sleep(1)
            except Exception:
                pass

        else:
            filename = None

        await thread.delete()
        if filename is not None:
            if not f.verif_taille(filename, taille_max):
                await interaction.followup.send("Message trop grand pour discord.")
                return
            try:
                await interaction.followup.send(
                    f.image_to_txt(filename, taille_max, dither)
                )
            except Exception as e:
                await interaction.followup.send("Erreur. Relance la commande !")
                print(str(e))
            finally:
                if os.path.exists(filename):
                    os.remove(filename)

        else:
            await interaction.followup.send("Erreur. Relance la commande !")


class MyView(discord.ui.View):
    @discord.ui.select(  # the decorator that lets you specify the properties of the select menu
        placeholder="Choose a Flavor!",  # the placeholder text that will be displayed if nothing is selected
        min_values=1,  # the minimum number of values that must be selected by the users
        max_values=2,  # the maximum number of values that can be selected by the users
        options=[  # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="Vanilla", description="Pick this if you like vanilla!"
            ),
            discord.SelectOption(
                label="Chocolate", description="Pick this if you like chocolate!"
            ),
            discord.SelectOption(
                label="Strawberry", description="Pick this if you like strawberry!"
            ),
        ],
    )
    async def callback(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):  # Quand le les options sont sélectionnées
        await interaction.response.send_message(
            f"You selected: {', '.join(select.values)}"
        )


@bot.tree.command(guild=serveur_obj, name="tetstt", description="Renvoie des blagues !")
async def flavor(ctx: discord.Interaction, type: discord.User = None):
    await ctx.response.send_message("Choose a flavor!", view=MyView())


@bot.tree.command(name="info_membre", description="Donne des infos sur un membre")
async def member_description(interaction: discord.Interaction, membre: discord.User):
    embed = discord.Embed(
        title=membre.global_name, timestamp=datetime.datetime.now(), color=membre.color
    )
    embed.set_author(
        name=membre.name, url=membre.avatar.url, icon_url=membre.avatar.url
    )

    url = f"https://thispersondoesnotexist.com/?{time.time()}"
    embed.set_image(url=url)

    love = random.choice(list(interaction.guild.members))
    embed.add_field(name="Amour", value=f"Amoureux de ||{love.name}||", inline=False)

    embed.add_field(
        name="Date de création du compte",
        value=membre.created_at.strftime("%d/%m/%Y à %H:%M:%S UTC"),
        inline=False,
    )

    await interaction.response.send_message(embed=embed)

print(TOKEN)
bot.run(TOKEN)
