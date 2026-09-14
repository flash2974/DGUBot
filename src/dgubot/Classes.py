import asyncio
import time

import discord
from discord.ext import commands

import dgubot.Fonctions as n


class Dialogue_CodeTel(discord.ui.Modal, title="Créer code"):
    theme = discord.ui.TextInput(
        label="Thème", required=True, placeholder="Voitures, Animaux, ..."
    )

    mot = discord.ui.TextInput(
        label="Mot", required=True, placeholder="Supra Mk4, Tigre, ..."
    )

    async def on_submit(self, interaction: discord.Interaction):
        theme = self.theme.value
        mot = self.mot.value

        code, possible = n.tri_telephone(theme, mot)
        if possible:
            await interaction.response.send_message(
                f"Le mot `{mot}` ayant pour code `{code}` enregistré dans le thème `{theme}`",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message("Mot déjà enregistré !")

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        print(error)
        await interaction.response.send_message(
            "Une erreur est survenue", ephemeral=True
        )


class Dialogue_SupprCodeTel(discord.ui.Modal, title="Supprimer code"):
    mot = discord.ui.TextInput(label="Mot à supprimer", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        mot = self.mot.value

        reussi = n.del_key(mot)
        if reussi:
            await interaction.response.send_message("Mot suppprimé !", ephemeral=True)
        else:
            await interaction.response.send_message("Erreur")

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        print(error)
        await interaction.response.send_message(
            "Une erreur est survenue", ephemeral=True
        )


class ChoixJeuTelephone(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Créer code", style=discord.ButtonStyle.blurple, emoji="📌"
    )
    async def creationCodes(
        self, interaction: discord.Interaction, button=discord.ui.Button
    ):
        await interaction.response.send_modal(Dialogue_CodeTel())

    @discord.ui.button(
        label="Supprimer code", style=discord.ButtonStyle.danger, emoji="🚮"
    )
    async def suppressionCodes(
        self, interaction: discord.Interaction, button=discord.ui.Button
    ):
        await interaction.response.send_modal(Dialogue_SupprCodeTel())

    @discord.ui.button(
        label="Voir la liste des codes", style=discord.ButtonStyle.primary, emoji="👀"
    )
    async def liste_tel(
        self, interaction: discord.Interaction, button=discord.ui.Button
    ):
        if interaction.user.id in [706296024326602762, 921740204094672906]:
            await interaction.response.send_message(n.afficher_dico_telephone())
        else:
            await interaction.response.send_message(
                "T'as pas le droit de voir ça ! 😡", ephemeral=True
            )

    @discord.ui.button(label="Jouer", style=discord.ButtonStyle.success, emoji="🕹️")
    async def jeu(self, interaction: discord.Interaction, button=discord.ui.Button):
        await interaction.response.defer()
        await interaction.followup.send(
            content="# Règles du jeu\nUn mot est codé avec le clavier de téléphone, à vous de trouver d'abord le numéro correspondant puis le mot !\nÀ tout moment, envoyez `stop` et le jeu s'arrêtera.",
            view=ComprisTel(self.bot),
        )


class ComprisTel(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.compris = False
        self.bot = bot

    @discord.ui.button(label="Compris", style=discord.ButtonStyle.blurple, emoji="✅")
    async def test1(self, interaction: discord.Interaction, button=discord.ui.Button):
        debut = time.time()
        await interaction.response.defer()

        def check(message):
            return (
                message.author == interaction.user
                and message.channel == interaction.channel
            )

        ok = False
        while not ok:
            await interaction.followup.send(
                content=f"Quel thème voulez-vous parmis ceux proposés ? Entrez son nom en tant que message Discord.\n{n.liste_themes('Data/code_telephone.txt')}\n||{interaction.user.mention}||"
            )

            try:
                mess = await self.bot.wait_for("message", check=check, timeout=None)
                entree = mess.content.lower().strip()

                ok = n.test(entree, "code_telephone.txt")
                if not ok:
                    await interaction.followup.send(
                        f"Ce thème n'est pas dans la base de données. Veuillez réessayer.\n||{interaction.user.mention}||"
                    )

            except TimeoutError:
                await interaction.followup.send(
                    f"Temps écoulé. Veuillez réessayer.\n||{interaction.user.mention}||"
                )

        mot_a_trouver, code, theme = n.choix_alea_tel(entree)
        await interaction.followup.send(
            f"### Thème : {theme}\nEntrez un code en tant que message Discord.\n||{interaction.user.mention}||",
            file=discord.File("Data/image.png"),
        )
        trouve = False
        nbr = True
        chaine = False
        while not trouve:
            try:
                message = await self.bot.wait_for("message", check=check, timeout=None)
                entree = message.content.lower().strip()

                if entree == "stop":
                    await interaction.followup.send(content="Fin du jeu")
                    break

                if entree == str(code):
                    nbr = False
                    chaine = True
                    await interaction.followup.send(
                        content=f"Bravo ! Vous avez trouvé le code. Trouvez maintenant le mot !\n||{interaction.user.mention}||",
                        file=discord.File("Data/image.png"),
                    )

                if not any(char.isdigit() for char in entree) and nbr:
                    await interaction.followup.send(
                        content=f"Trouvez d'abord le code !\n||{interaction.user.mention}||"
                    )

                elif nbr and len(entree) > len(code):
                    await interaction.followup.send(
                        content=f"Code trop long ! Le code à rechercher est composé de {len(code)} chiffres\n||{interaction.user.mention}||"
                    )

                elif nbr and len(entree) < len(code):
                    await interaction.followup.send(
                        content=f"Code trop court ! Le code à rechercher est composé de {len(code)} chiffres\n||{interaction.user.mention}||"
                    )

                elif nbr:
                    sortie = f"### Thème : {theme}\n"

                    for indice in range(len(entree)):
                        if entree[indice] == code[indice]:
                            sortie += entree[indice].upper()
                        elif entree[indice] != code[indice]:
                            sortie += " . "
                    await interaction.followup.send(
                        content=sortie + f"\n||{interaction.user.mention}||",
                        file=discord.File("Data/image.png"),
                    )

                if (
                    chaine
                    and entree != str(code)
                    and not any(char.isdigit() for char in entree)
                ):
                    if entree == mot_a_trouver:
                        fin = time.time()
                        temps = int(fin - debut)
                        if temps > 60:
                            minute = temps // 60
                            seconde = temps % 60
                            if minute > 1:
                                chaine_m = "minutes"
                            else:
                                chaine_m = "minute"

                            if seconde > 1:
                                chaine_s = "secondes"
                            else:
                                chaine_s = "seconde"

                            await interaction.followup.send(
                                content=f"Vous avez gagné en {minute} {chaine_m} et {seconde} {chaine_s} ! Bravo\n||{interaction.user.mention}||"
                            )
                        else:
                            await interaction.followup.send(
                                content=f"Vous avez gagné en {temps} secondes ! Bravooo c'était très rapide 😎\n||{interaction.user.mention}||"
                            )
                        trouve = True
                    else:
                        await interaction.followup.send(
                            content=f"### Thème : {theme}\nMot incorrect. Je rappelle le code : {code}\n||{interaction.user.mention}||",
                            file=discord.File("Data/image.png"),
                        )

                if (
                    chaine
                    and entree != str(code)
                    and any(char.isdigit() for char in entree)
                ):
                    await interaction.followup.send(
                        content=f"Code déjà trouvé (c'est {code}) ! Trouvez maintenant le mot correspondant.\n||{interaction.user.mention}||",
                        file=discord.File("Data/image.png"),
                    )

            except TimeoutError:
                await interaction.followup.send(
                    f"Temps écoulé. Veuillez réessayer.\n||{interaction.user.mention}||"
                )


class Dialogue_CodeJUSTEPRIX(discord.ui.Modal, title="Créer code"):
    theme = discord.ui.TextInput(
        label="Thème", required=True, placeholder="Voitures, Animaux, ..."
    )

    objet = discord.ui.TextInput(
        label="Objet", required=True, placeholder="Supra Mk4, Tigre, ..."
    )

    prix = discord.ui.TextInput(
        label="Prix", required=True, placeholder="30 000, 350 (en €)"
    )

    async def on_submit(self, interaction: discord.Interaction):
        theme = self.theme.value
        objet = self.objet.value
        prix = self.prix.value

        possible = n.tri_justeprix(theme, objet, prix)
        if possible:
            await interaction.response.send_message(
                f"L'objet `{objet}`, coûtant `{prix} €` enregistré dans le thème `{theme}`",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message("Mot déjà enregistré !")

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        print(error)
        await interaction.response.send_message(
            "Une erreur est survenue", ephemeral=True
        )


class Dialogue_SupprCodeJUSTEPRIX(discord.ui.Modal, title="Supprimer code"):
    objet = discord.ui.TextInput(label="Mot à supprimer", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        objet = self.objet.value

        reussi = n.del_key_prix(objet)
        if reussi:
            await interaction.response.send_message("Objet suppprimé !", ephemeral=True)
        else:
            await interaction.response.send_message("Erreur")

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        print(error)
        await interaction.response.send_message(
            "Une erreur est survenue", ephemeral=True
        )


class ChoixJustePrix(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(
        label="Créer code", style=discord.ButtonStyle.blurple, emoji="📌"
    )
    async def creationCodes(
        self, interaction: discord.Interaction, button=discord.ui.Button
    ):
        await interaction.response.send_modal(Dialogue_CodeJUSTEPRIX())

    @discord.ui.button(
        label="Supprimer code", style=discord.ButtonStyle.danger, emoji="🚮"
    )
    async def suppressionCodes(
        self, interaction: discord.Interaction, button=discord.ui.Button
    ):
        await interaction.response.send_modal(Dialogue_SupprCodeJUSTEPRIX())

    @discord.ui.button(
        label="Voir la liste des codes", style=discord.ButtonStyle.primary, emoji="👀"
    )
    async def liste_tel(
        self, interaction: discord.Interaction, button=discord.ui.Button
    ):
        if interaction.user.id in [706296024326602762, 921740204094672906]:
            await interaction.response.send_message(n.afficher_dico_justePrix())
        else:
            await interaction.response.send_message(
                "T'as pas le droit de voir ça ! 😡", ephemeral=True
            )

    @discord.ui.button(label="Jouer", style=discord.ButtonStyle.success, emoji="🕹️")
    async def jeu(self, interaction: discord.Interaction, button=discord.ui.Button):
        await interaction.response.defer()
        await interaction.followup.send(
            content="# Règles du jeu\nPar tatonnement, vous allez devoir trouver le prix d'un objet, puis deviner quel est cet objet en question, en s'aidant du thème choisi ! À tout moment, envoyez `stop` et le jeu s'arrêtera. Vous enverrez d'abord le prix auquel vous pensez, et le bot vous guidera. Quand vous aurez trouvé le juste prix, devinez l'objet en vous aidant du thème !",
            view=ComprisJustePrix(self.bot),
        )


class ComprisJustePrix(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.compris = False
        self.bot = bot

    @discord.ui.button(label="Compris", style=discord.ButtonStyle.blurple, emoji="✅")
    async def test2(self, interaction: discord.Interaction, button=discord.ui.Button):
        debut = time.time()
        await interaction.response.defer()

        def check(message):
            return (
                message.author == interaction.user
                and message.channel == interaction.channel
            )

        ok = False
        while not ok:
            await interaction.followup.send(
                f"Quel thème voulez-vous parmis ceux proposés ? Entrez son nom en tant que message Discord.\n{n.liste_themes('Data/justePrix.txt')}||{interaction.user.mention}||"
            )

            mess = await self.bot.wait_for("message", check=check, timeout=None)
            entree_1 = mess.content.lower().strip()

            ok = n.test(entree_1, "justePrix.txt")
            if not ok:
                await interaction.followup.send(
                    f"Ce thème n'est pas dans la base de données. Veuillez réessayer.\n||{interaction.user.mention}||"
                )

        objet, prix, theme = n.choix_alea_justePrix(entree_1)
        await interaction.followup.send(
            f"### Thème : {theme}\nEntrez un prix (sans euros) en tant que message Discord.\nPar exemple : `400` pour 400 €.\n||{interaction.user.mention}||"
        )
        objet_trouve = False
        prix_trouve = False

        while not objet_trouve:
            try:
                message = await self.bot.wait_for("message", check=check, timeout=None)
                entree = message.content.lower().strip()

                if entree == "stop":
                    await interaction.followup.send(content="Fin du jeu")
                    break

                if not any(char.isdigit() for char in entree) and not prix_trouve:
                    await interaction.followup.send(
                        content=f"Trouvez d'abord le prix de l'objet !\n||{interaction.user.mention}||"
                    )

                elif [char.isdigit() for char in entree] and not prix_trouve:
                    temperature, smiley = n.prixcorrect_chaleur(entree, prix)
                    if int(entree) > int(prix):
                        await interaction.followup.send(
                            content=f"C'est moins ! 🌡️ {temperature}°C {smiley}\n||{interaction.user.mention}||"
                        )

                    elif int(entree) < int(prix):
                        await interaction.followup.send(
                            content=f"C'est plus ! 🌡️ {temperature}°C {smiley}\n||{interaction.user.mention}||"
                        )

                    else:
                        prix_trouve = True
                        await interaction.followup.send(
                            content=f"Bravo ! Vous avez trouvé le juste prix de l'objet. Trouvez maintenant cet objet !\n||{interaction.user.mention}||"
                        )

                if prix_trouve and entree != str(prix) and not entree.isdigit():
                    if entree == objet:
                        fin = time.time()
                        temps = int(fin - debut)
                        if temps > 60:
                            minute = temps // 60
                            seconde = temps % 60
                            if minute > 1:
                                chaine_m = "minutes"
                            else:
                                chaine_m = "minute"

                            if seconde > 1:
                                chaine_s = "secondes"
                            else:
                                chaine_s = "seconde"

                            await interaction.followup.send(
                                content=f"Vous avez gagné en {minute} {chaine_m} et {seconde} {chaine_s} ! Bravo\n||{interaction.user.mention}||"
                            )
                        else:
                            await interaction.followup.send(
                                content=f"Vous avez gagné en {temps} secondes ! Bravooo c'était très rapide 😎\n||{interaction.user.mention}||"
                            )
                        objet_trouve = True
                    else:
                        await interaction.followup.send(
                            content=f"### Thème : {theme}\nObjet incorrect. Je rappelle le prix : {prix} €\n||{interaction.user.mention}||"
                        )

                if prix_trouve and entree != str(prix) and entree.isdigit():
                    await interaction.followup.send(
                        content=f"Prix déjà trouvé (c'est {prix} €) ! Trouvez maintenant l'objet.\n||{interaction.user.mention}||"
                    )

            except TimeoutError:
                await interaction.followup.send(
                    "Temps écoulé. Veuillez réessayer.\n||{interaction.user.mention}||"
                )


# Blind Test
class Menu(discord.ui.View):
    def __init__(
        self,
        controle,
        blind_test,
        url,
        temps_musique,
        bot: commands.Bot,
        idRole,
        blind_test_play,
    ):
        super().__init__(timeout=None)
        self.temps_musique = temps_musique
        self.url = url
        self.voice_channel = None
        self.voice_client = None
        self.musique_dl = None
        self.message = None
        self.i = 0
        self.is_playing = False
        self.titre = ""
        self.artiste = ""
        self.winners_dico = {}
        self.interaction = None
        self.titre = False
        self.auteur = False
        self.winner = None
        self.indice = 1
        self.titre_playing = ""
        self.auteur_playing = ""
        self.membres_avec_role = []
        self.controle = controle
        self.blind_test = blind_test
        self.gg = None
        self.debut = True
        self.pause = False
        self.scores = None
        self.debut_compteur = 0
        self.tps_pause = 0
        self.moment_pause = 0
        self.timeout = False
        self.dico_log = {}
        self.bot = bot
        self.idRole = idRole
        self.blind_test_play = blind_test_play

    def add_points(self, user, points):
        if user in self.winners_dico:
            self.winners_dico[user] += points
        else:
            self.winners_dico[user] = points

    def droits(self, interaction: discord.Interaction):
        return interaction.user.id in [706296024326602762, 921740204094672906]

    def chrono(self):
        tps_actuel = time.time()
        if self.pause:
            temps_restant = 1
        else:
            temps_restant = (
                self.temps_musique
                - round(tps_actuel - self.debut_compteur)
                + self.tps_pause
            )
        print(temps_restant)
        return temps_restant

    async def bonne_rep(self, musique: dict):
        def check(message):
            return message.channel.id == self.blind_test_play

        try:
            self.timeout = False
            message = await self.bot.wait_for(
                "message", check=check, timeout=Menu.chrono(self)
            )
            await message.delete()
            self.dico_log[message.author.display_name].append(message.content.lower())
        except TimeoutError:
            self.timeout = True
            return
        entree = n.del_accent_phrase(message.content.lower())
        titre = musique["titre"]
        auteur = musique["auteurs"]

        titre_clean = n.del_accent_phrase(titre)
        auteur_clean = n.del_accent_phrase(auteur)
        auteur_ok, points, auteur_manquant = n.check_auteur(entree, auteur_clean)

        if not self.pause:
            if (
                entree == titre_clean and not self.titre and not self.auteur
            ):  # Si l'entrée correspond au titre et que ni le titre ni l'auteur ont été trouvés
                self.titre = True
                Menu.add_points(self, message.author.display_name, 5)
                self.winner = message.author.mention
                await self.blind_test.send(
                    f"{message.author.mention} a trouvé le titre de la musique ({titre}) : `+5 points` 😀 ! Trouvez maintenant son auteur. Il vous reste {Menu.chrono(self)} secondes.",
                    delete_after=5,
                )
                await self.scores.edit(content=Menu.ecran_score(self))

            elif (
                entree == titre_clean and not self.titre and self.auteur
            ):  # Si l'entrée correspond au titre et et que le titre n'a pas encore été trouvé, par contre l'auteur si
                self.titre = True
                Menu.add_points(self, message.author.display_name, 5)
                await self.blind_test.send(
                    f"{message.author.mention} a trouvé le titre de la musique : `+5 points` 😀 ! Bravo à toi et à {self.winner}.",
                    delete_after=4,
                )
                await self.scores.edit(content=Menu.ecran_score(self))

            elif (
                entree == titre_clean and self.titre and not self.auteur
            ):  # Si l'entrée correspond au titre mais qu'il a déjà été trouvé, et que l'auteur n'a pas encore été trouvé
                await self.blind_test.send(
                    f"Titre déjà trouvé par {self.winner} ({titre}). Trouvez maintenant l'auteur de la musique. Il vous reste {Menu.chrono(self)} secondes.",
                    ephemeral=True,
                    delete_after=4,
                )

            elif (
                titre_clean in entree
                and auteur_ok
                and not self.titre
                and not self.auteur
            ):
                Menu.add_points(self, message.author.display_name, 5 + points)
                self.auteur = True
                self.titre = True
                await self.blind_test.send(
                    f"Gros GG à toi {message.author.mention} !! Tout trouvé d'un seul coup. `+{5 + points}` 😎",
                    delete_after=4,
                )
                await self.scores.edit(content=Menu.ecran_score(self))

            elif (
                auteur_ok and not self.titre and not self.auteur
            ):  # Si l'entrée correspond à l'auteur et que ni le titre ni l'auteur ont été trouvés
                self.auteur = True
                Menu.add_points(self, message.author.display_name, points)
                self.winner = message.author.mention
                await self.blind_test.send(
                    f"{message.author.mention} a trouvé l'auteur de la musique ({auteur}) : `+5 points` 😀 ! Trouvez maintenant son titre. Il vous reste {Menu.chrono(self)} secondes.",
                    delete_after=5,
                )
                await self.scores.edit(content=Menu.ecran_score(self))

            elif (
                auteur_ok and not self.auteur and self.titre
            ):  # Si l'entrée correspond au titre et et que l'auteur n'a pas encore été trouvé, par contre le titre si
                self.auteur = True
                Menu.add_points(self, message.author.display_name, points)
                await self.blind_test.send(
                    f"{message.author.mention} a trouvé le l'auteur de la musique : `+5 points` 😀 ! Bravo à toi et à {self.winner}.",
                    delete_after=4,
                )
                await self.scores.edit(content=Menu.ecran_score(self))

            elif (
                auteur_ok and self.auteur and not self.titre
            ):  # Si l'entrée correspond à l'auteur mais qu'il a déjà été trouvé, et que le titre n'a pas encore été trouvé
                await self.blind_test.send(
                    f"Auteur déjà trouvé par {self.winner} ({auteur}). Trouvez maintenant le titre de la musique. Il vous reste {Menu.chrono(self)} secondes.",
                    ephemeral=True,
                    delete_after=4,
                )

        else:
            if message.author.mention != "<@1109564010958946385>":
                await self.blind_test.send(
                    f"Tss ! On est en pause ça compte pas {message.author.mention}",
                    delete_after=3,
                )

    def roles(self, interaction: discord.Interaction):
        membres_avec_role = []
        role = discord.utils.get(interaction.guild.roles, id=self.idRole)
        for member in self.bot.get_all_members():
            if role in member.roles:
                membres_avec_role.append(member.display_name)
        return membres_avec_role

    def ecran_score_first(self, interaction: discord.Interaction):
        membres_avec_role = self.roles(interaction=interaction)
        self.membres_avec_role = sorted(membres_avec_role)
        chaine = "## Tableau des scores\n```"
        for personne in self.membres_avec_role:
            self.winners_dico[personne] = 0
            chaine += f"{personne} : 0 point\n"
            self.dico_log[personne] = []
        chaine += "```"
        return chaine

    def ecran_score(self):
        chaine = "## Tableau des scores\n```"
        for personne in self.membres_avec_role:
            chaine += f"{personne} : {self.winners_dico[personne]} points\n"
        chaine += "```"
        return chaine

    def is_winner(self):
        max_score = [
            self.membres_avec_role[0],
            self.winners_dico[self.membres_avec_role[0]],
        ]
        for user, points in self.winners_dico.items():
            if points > max_score[1]:
                max_score = [user, points]
        return max_score

    async def waiting(self, contexte):
        temps = 5
        if contexte == "entre_2":
            chaine = "Prochaine musique dans"
        elif contexte == "debut":
            chaine = "Lancement de la musique dans"
        message = await self.blind_test.send(content=f"{chaine} {temps} secondes ...")
        await asyncio.sleep(1)
        for indice in range(temps - 1, 0, -1):
            if indice == 1:
                sec = "seconde"
            else:
                sec = "secondes"
            await message.edit(content=f"{chaine} {indice} {sec}...")
            await asyncio.sleep(1)
        await message.delete()

    async def lecture_musique(self, interaction: discord.Interaction):
        self.scores = await self.blind_test.send(
            content=Menu.ecran_score_first(self, interaction=interaction)
        )
        print(self.musique_dl)
        for indice in range(len(self.musique_dl)):
            self.debut_compteur = time.time()
            self.pause = False
            self.voice_client.play(
                discord.FFmpegPCMAudio(self.musique_dl[indice])
            )

            playlist = n.find_playlist(self.url)
            self.titre_playing = playlist["musiques"][indice]["titre"]
            auteur = playlist["musiques"][indice]["auteurs"]
            self.auteur_playing = auteur.split(".")[0]
            await Menu.lecture_en_cours(self)
            self.winner = None
            self.titre = False
            self.auteur = False
            self.tps_pause = 0
            while self.voice_client.is_playing() or self.pause:
                if not (self.titre and self.auteur):
                    await Menu.bonne_rep(self, playlist["musiques"][indice])
                    if self.timeout and not self.pause and Menu.chrono(self) == 0:
                        self.voice_client.stop()
                        break

                else:
                    self.voice_client.stop()
                    break
            await self.blind_test.send(
                f"La musique était `{self.titre_playing}` de `{self.auteur_playing}`",
                delete_after=4,
            )
            if self.indice != len(self.musique_dl):
                await Menu.waiting(self, contexte="entre_2")
            self.indice += 1

        winner = Menu.is_winner(self)
        await self.blind_test.send(
            f"## Fin du jeu ! {winner[0]} a gagné avec {winner[1]} points !"
        )
        await self.voice_client.disconnect()
        n.del_all()
        file = open("Data/BlindTest.txt", "w", encoding="utf-8")
        file.write(str(self.dico_log))
        file.close()

    async def lecture_en_cours(self):
        await self.message.edit(
            content=f"💿 Musique en cours : `{self.titre_playing}` de `{self.auteur_playing}` ({self.indice}/{len(self.musique_dl)})"
        )

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="📥")
    async def bouton1(self, interaction: discord.Interaction, button=discord.ui.Button):
        await interaction.response.defer()
        if interaction.user.voice is None:
            a = await interaction.followup.send(
                "Tu dois être connecté à un canal vocal."
            )
            await asyncio.sleep(2)
            await a.delete()
            return
        self.voice_channel = interaction.user.voice.channel

        i = 1
        self.message = await interaction.followup.send("Préparation ...")
        try:
            musiques = n.find_dl(self.url)
        except Exception as e:
            # print(e)
            await self.message.edit(content=f"Erreur : {e}")
            return
        else:
            for self.musique_dl, nb_musiques in musiques:
                if self.musique_dl == False:
                    await self.message.edit(
                        content=f"Téléchargement en cours ... ({i}/{nb_musiques}, environ {5 * (nb_musiques - i + 1)}s restantes)"
                    )
                    i += 1
            await self.message.edit(content="Téléchargement terminé !")
            button.disabled = True
            if self.voice_client == None or not self.voice_client.is_connected():
                self.voice_client = await self.voice_channel.connect()

    @discord.ui.button(style=discord.ButtonStyle.blurple, emoji="⏯️")
    async def bouton2(self, interaction: discord.Interaction, button=discord.ui.Button):
        await interaction.response.defer()
        if self.debut:
            self.debut = False
            await self.message.edit(content="💿 Lancement de la musique !")
            await Menu.waiting(self, contexte="debut")
            await Menu.lecture_musique(self, interaction)

        else:
            if self.voice_client.is_playing():
                await self.blind_test.send("ㅤ")
                self.moment_pause = time.time()
                self.pause = True
                self.voice_client.pause()

            else:
                moment_relance = time.time()
                self.tps_pause += round(moment_relance - self.moment_pause)
                self.pause = False
                self.voice_client.resume()

    @discord.ui.button(label="Quitter", style=discord.ButtonStyle.blurple, emoji="❌")
    async def bouton3(self, interaction: discord.Interaction, button=discord.ui.Button):
        await self.voice_client.disconnect()
        await self.message.edit(content="Déconnexion du bot")
