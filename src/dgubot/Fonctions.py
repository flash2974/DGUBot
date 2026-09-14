import os
import random as r

import yt_dlp as youtube_dl
from ytmusicapi import YTMusic

yt = YTMusic()


def recherche(mot: str) -> list:
    dico = open("Data/Dico.txt", "r", encoding="utf-8")
    position_connues = positions_connues(mot)
    mots = []
    for ligne in dico:
        if test_longueur(mot, ligne) and teste_toutes_positions(
            position_connues, mot, ligne
        ):
            mots.append(ligne.strip())
    dico.close()
    return list(set(mots))


def positions_connues(mot: str) -> list:
    tab = []
    for indice in range(len(mot)):
        if mot[indice] != "*":
            tab.append(indice)
    return tab


def positions_inconnues(mot: str) -> list:
    tab = []
    for indice in range(len(mot)):
        if mot[indice] == "*":
            tab.append(indice)
    return tab


def test_longueur(str1: str, str2: str) -> bool:
    return len(str1.strip()) == len(str2.strip())


def teste_toutes_positions(positions_connues: list, mot: str, ligne: str) -> bool:
    trouve = True
    for num in positions_connues:
        if mot[num] != ligne[num]:
            trouve = False
            break
    return trouve


def lettres_possibles(mot: str, mots_trouves: list) -> dict:
    lettres = {}
    pos_inconnues = positions_inconnues(mot)
    for element in mots_trouves:
        for position in pos_inconnues:
            if lettres.get(element[position], None) == None:
                lettres[element[position]] = 1
            else:
                lettres[element[position]] += 1
    return lettres


def tri_dico(dictionnaire: dict) -> dict:
    dic_trie = dict(
        sorted(dictionnaire.items(), key=lambda item: item[1], reverse=True)
    )
    return dic_trie


def pourcentage_lettres(dico_lettres: dict) -> list:
    total = 0
    liste = []
    dico_lettres = tri_dico(dico_lettres)
    for cle in dico_lettres:
        total += dico_lettres[cle]
    for cle_2 in dico_lettres:
        liste.append(
            cle_2 + " à " + str(round(100 * dico_lettres[cle_2] / total)) + " %"
        )
    return liste


def transformation(mot: str) -> int:
    mot_liste = []
    for lettre in mot:
        mot_liste.append(lettre.lower())

    code = ""
    for element in mot_liste:
        if element != " ":
            code += lettre_correspondante(element)
    return int(code)


def lettre_correspondante(lettre: str) -> str:
    dico = {
        2: ["a", "à", "ä", "â", "b", "c"],
        3: ["d", "e", "é", "è", "ê", "ë", "f"],
        4: ["g", "h", "i", "ï", "î"],
        5: ["j", "k", "l"],
        6: ["m", "n", "o", "ô", "ö"],
        7: ["p", "q", "r", "s"],
        8: ["t", "u", "ù", "û", "ü", "v"],
        9: ["w", "x", "y", "z"],
    }

    for cle in dico:
        if lettre in dico[cle]:
            return str(cle)


def tri_telephone(theme, mot) -> str:
    code = transformation(mot)

    file = open("Data/code_telephone.txt", "r", encoding="utf-8")
    dico = eval(file.read().strip())
    file.close()
    possible = True
    if theme in dico and mot in dico[theme]["mot"]:
        possible = False
    else:
        if theme in dico:
            dico[theme]["mot"].append(mot)
            dico[theme]["code"].append(code)
        else:
            mini_dic = {}
            mini_dic["mot"] = [mot]
            mini_dic["code"] = [code]
            dico[theme] = mini_dic

    file = open("Data/code_telephone.txt", "w", encoding="utf-8")
    file.write(str(dico))
    file.close()

    return code, possible


def afficher_dico_telephone() -> str:
    file = open("Data/code_telephone.txt", "r", encoding="utf-8")
    dico = eval(file.read().strip())
    file.close()
    res = ""
    for theme in dico:
        res += f"### Thème : {theme}\n\n"
        for indice in range(len(dico[theme]["code"])):
            res += (
                "Mot : `"
                + str(dico[theme]["mot"][indice])
                + "` ; code : `"
                + str(dico[theme]["code"][indice])
                + "`\n"
            )
    return res


def del_key(mot):

    file = open("Data/code_telephone.txt", "r", encoding="utf-8")
    dico = eval(file.read().strip())
    suppr = False

    for theme in dico:
        if mot in dico[theme]["mot"]:
            indice = dico[theme]["mot"].index(mot)
            del dico[theme]["mot"][indice]
            del dico[theme]["code"][indice]
            suppr = True
            break

    if suppr:
        file = open("Data/code_telephone.txt", "w", encoding="utf-8")
        file.write(str(dico))
    file.close()
    return suppr


def liste_themes(file: str) -> str:
    file = open(file, "r", encoding="utf-8")
    dico = eval(file.read().strip())
    file.close()

    res = "# Thèmes\n"
    for theme in dico:
        res += f"* {theme}\n"
    return res


def choix_alea_tel(theme: str) -> tuple:
    file = open("Data/code_telephone.txt", "r", encoding="utf-8")
    dico = eval(file.read().strip())
    file.close()
    if theme in dico:
        mots_possibles = dico[theme]["mot"]
        mot_random = r.choice(mots_possibles)

        indice = 0
        trouve = False
        while not trouve:
            if mots_possibles[indice] == mot_random:
                trouve = True
            else:
                indice += 1

        code_random = dico[theme]["code"][indice]

        return mot_random, str(code_random), theme


def test(cle: str, file: str) -> bool:
    file = open("Data/" + file, "r", encoding="utf-8")
    dico = eval(file.read().strip())
    file.close()
    return True if cle in dico else False


def tri_justeprix(theme, objet, prix):

    file = open("Data/justePrix.txt", "r", encoding="utf-8")
    dico = eval(file.read().strip())
    file.close()

    possible = True
    if theme in dico and objet in dico[theme]["objet"]:
        possible = False

    else:
        if theme in dico:
            dico[theme]["objet"].append(objet)
            dico[theme]["prix"].append(prix)
        else:
            mini_dic = {}
            mini_dic["objet"] = [objet]
            mini_dic["prix"] = [prix]
            dico[theme] = mini_dic

    file = open("Data/justePrix.txt", "w", encoding="utf-8")
    file.write(str(dico))
    file.close()

    return possible


def choix_alea_justePrix(theme: str) -> tuple:
    file = open("Data/justePrix.txt", "r", encoding="utf-8")
    dico = eval(file.read().strip())
    file.close()
    if theme in dico:
        objets_possibles = dico[theme]["objet"]
        objet_random = r.choice(objets_possibles)

        indice = 0
        trouve = False
        while not trouve:
            if objets_possibles[indice] == objet_random:
                trouve = True
            else:
                indice += 1

        prix_random = dico[theme]["prix"][indice]

        return objet_random, str(prix_random), theme


def afficher_dico_justePrix() -> str:
    file = open("Data/justePrix.txt", "r", encoding="utf-8")
    dico = eval(file.read().strip())
    file.close()
    res = ""
    for theme in dico:
        res += f"### Thème : {theme}\n\n"
        for indice in range(len(dico[theme]["objet"])):
            res += (
                "Objet : `"
                + str(dico[theme]["objet"][indice])
                + "` ; prix : `"
                + str(dico[theme]["prix"][indice])
                + "`\n"
            )
    return res


def del_key_prix(objet):

    file = open("Data/justePrix.txt", "r", encoding="utf-8")
    dico = eval(file.read().strip())
    file.close()
    suppr = False

    for theme in dico:
        if objet in dico[theme]["objet"]:
            indice = dico[theme]["objet"].index(objet)
            del dico[theme]["objet"][indice]
            del dico[theme]["prix"][indice]
            suppr = True
            break

    if suppr:
        file = open("Data/justePrix.txt", "w", encoding="utf-8")
        file.write(str(dico))
        file.close()
    return suppr


def prixcorrect_chaleur(prix_rentre: str, prix_reel: str) -> tuple:
    dif = abs(int(prix_rentre) - int(prix_reel))
    temp = round(100 * (1 - dif / int(prix_reel)))
    chaine = ""
    if temp > 80:
        chaine = "🥵"
    elif temp > 60:
        chaine = "😀☀️"
    elif temp > 40:
        chaine = "😀"
    elif temp > 20:
        chaine = "🥶"
    elif temp > 10:
        chaine = "🥶🧊"
    else:
        chaine = "🥶🧊🧊"
    return temp, chaine


def download(url, nom):
    ydl_opts = {"format": "bestaudio/best", "outtmpl": nom}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def find_playlist(playlist_url: str):
    ID = playlist_url.split("list=")[1]
    if "&" in ID:
        ID = ID.split("&")[0]
    playlist = yt.get_playlist(ID)

    new_dico = {}
    new_dico["nom"] = playlist["title"]
    new_dico["musiques"] = []
    for indice in range(len(playlist["tracks"])):
        titre = playlist["tracks"][indice]["title"]

        if " (" in titre:
            titre = titre.split(" (")[0]

        auteurs = ""
        longueur = len(playlist["tracks"][indice]["artists"])
        i_artistes = longueur
        for dic in playlist["tracks"][indice]["artists"]:
            if i_artistes > 1:
                auteurs += dic["name"] + " et "
            else:
                auteurs += dic["name"]
            i_artistes -= 1

        ID = playlist["tracks"][indice]["videoId"]
        lien = f"https://music.youtube.com/watch?v={ID}"

        new_dico["musiques"].append({"titre": titre, "auteurs": auteurs, "lien": lien})

    return new_dico


def find_dl(playlist_url: str):
    del_all()
    try:
        dico = find_playlist(playlist_url)
    except Exception as e:
        raise Exception(str(e))
    else:
        return generator(dico)


def generator(dico: dict):
    filenames = []
    i = 1
    os.makedirs("musiques", exist_ok=True)
    for musique in dico["musiques"]:
        new_filename = f"musiques/musique{i}.webm"
        yield False, len(dico["musiques"])
        download(musique["lien"], new_filename)
        filenames.append(new_filename)
        i += 1
    yield filenames, len(dico["musiques"])


def del_all():
    for fichier in os.listdir():
        if fichier.endswith(".webm"):
            chemin_fichier = os.path.join(fichier)
            os.remove(chemin_fichier)


def listage():
    liste = []
    for fichier in os.listdir():
        if fichier.endswith(".webm"):
            liste.append(fichier)
    return liste


def check_auteur(entree, auteurs):
    entree = del_accent_phrase(entree.lower())
    auteurs = del_accent_phrase(auteurs.lower())
    auteurs = auteurs.split(" et ")
    points_par_auteur = round(5 / len(auteurs), 2)
    res = [False, 0, ""]
    for auteur in auteurs:
        if auteur in entree:
            res[0] = True
            res[1] += points_par_auteur
        else:
            res[2] += f"{auteur} "
    if type(res[1]) == float and res[1].is_integer():
        res[1] = int(res[1])
    return res


def del_accent_lettre(lettre):
    lettre = lettre.lower()
    dico = {
        "a": ["à", "ä", "â"],
        "e": ["é", "è", "ê", "ë"],
        "i": ["ï", "î"],
        "o": ["ô", "ö"],
        "u": ["ù", "û", "ü"],
    }
    for cle in dico:
        if lettre in dico[cle]:
            res = cle
            break
        else:
            res = lettre
    return res.lower()


def del_accent_phrase(phrase):
    mot_final = ""
    for lettre in phrase:
        mot_final += del_accent_lettre(lettre)
    return mot_final
