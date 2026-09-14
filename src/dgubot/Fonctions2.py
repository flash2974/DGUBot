import asyncio
import codecs
import datetime
import json
import urllib.request

import requests
from ntscraper import Nitter

reader = codecs.getreader("utf-8")
import random
import time

import numpy as np
from bs4 import BeautifulSoup
from PIL import Image


def last10TweetLink(profile, n=10):
    "retourne {url : [], date : []} des 10 derniers tweets"
    try:
        tweets = scraper.get_tweets(profile, mode="user", number=n)
    except Exception as e:
        print(e)

    else:
        if len(tweets["tweets"]) != 10:
            raise Not10Tweets(
                "10 tweets supposed to be returned, but not the case (causing error)"
            )
        if pinnedTweet(tweets):
            start = 1
        else:
            start = 0

        urls = []
        for indice in range(start, len(tweets["tweets"])):
            if not tweets["tweets"][indice]["is-retweet"]:
                urls.append(tweets["tweets"][indice]["link"])

        return urls


def newTweet(profile):
    now = time.time()
    print(f"{now - debut}s écoulées")
    if now - debut > 86400:
        init(profile)

    try:
        newList = last10TweetLink(profile)
    except Not10Tweets:
        raise Not10Tweets(
            "10 tweets supposed to be returned, but not the case (causing error)"
        )

    with open("Data/TweetsData.txt", "r", encoding="utf-8") as file:
        oldList = eval(file.read().strip())
        file.close()

    if newList == []:
        print("NewList vide")
        return [False]
    if oldList == [] and len(newList) > 0:
        print("OldList vide mais nv tweet")
        return [True, newList]

    # Si aucun nouveau tweet n'a été posté
    if oldList[0] == newList[0]:
        return [False]

    i = 1
    while newList[i] != oldList[0] and i < len(newList):
        i += 1

    newTweets = newList[0:i]
    res = [True, newTweets]
    oldList = newList + oldList
    oldList = clearList(oldList)
    with open("Data/TweetsData.txt", "w", encoding="utf-8") as file:
        file.write(str(oldList))
        file.close()
    return res  # res = [True, [url1, url2]] ou [False]


def init(profile):
    global debut
    debut = time.time()
    global scraper
    scraper = Nitter()
    try:
        lastTweet = last10TweetLink(profile)
    except IndexError:
        init(profile)
    else:
        with open("Data/ErrLogs.txt", "w") as file:
            file.close()
        with open("Data/TweetsData.txt", "w", encoding="utf-8") as file:
            file.write(str(lastTweet))
            file.close()


def addFx(link):
    link = link.split("https://")[1]
    res = "https://fx" + link
    return res


def pinnedTweet(tweets):
    if len(tweets["tweets"]) != 10:
        raise IndexError(
            "10 tweets supposed to be returned, but not the case (causing IndexError)"
        )
    dateTweet1 = transformDate(tweets["tweets"][0]["date"])
    dateTweet2 = transformDate(tweets["tweets"][1]["date"])
    print("tweet epingle" if dateTweet1 < dateTweet2 else "tweet non epingle")
    return (
        dateTweet1 < dateTweet2
    )  # Si le 1er tweet est plus vieux que le 2e, alors le 1er est épinglé


def transformDate(date: str):
    """Transforme une date au format : 'MMM JJ, AAAA · HH:MM A/PM UTC en objet datetime"""
    hourMinutes = date.split(" · ")[1].split(":")
    if "PM" in hourMinutes[1]:
        minutes = int(hourMinutes[1].split(" PM")[0])
        hour = int(hourMinutes[0]) + 12

    else:
        minutes = int(hourMinutes[1].split(" AM")[0])
        hour = int(hourMinutes[0])

    day = date[4:6]
    month = date[0:3]
    year = date[8:12]
    if not day.isdigit():
        day = date[4:5]
        year = date[7:11]
    day = int(day)
    year = int(year)

    month_dict = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }

    month = month_dict[month]

    date = datetime.datetime(year, month, day, hour, minutes)
    return date


def clearList(liste):
    if len(liste) > 10:
        liste = liste[:10]
        return liste


class Not10Tweets(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class YTStats:
    def __init__(self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id
        self.quota = 10000
        self.videos_count = self.get_channel_videos_count()

    def quota_verify(self):
        return self.quota > 0

    def get_channel_videos_count(self):
        self.quota -= 1
        url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}"
        json_url = requests.request("GET", url)
        data = json.loads(json_url.text)
        try:
            res = int(data["items"][0]["statistics"]["videoCount"])
            return res
        except KeyError:
            print(data)
            print("ouin")

    def get_last_videos_data(self):
        self.quota -= 100
        data = json.load(
            reader(
                urllib.request.urlopen(
                    f"https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=snippet,id&order=date"
                )
            )
        )
        return [
            len(data["items"]) - 1,
            "https://www.youtube.com/watch?v=" + data["items"][0]["id"]["videoId"],
        ]

    async def newVideo(self):
        if not self.quota_verify():
            raise Exception("Quota exceeded")
        video_count_now = self.get_channel_videos_count()
        print(video_count_now, self.videos_count)
        if video_count_now > self.videos_count:
            await asyncio.sleep(10)
            self.videos_count = video_count_now
            videoData = self.get_last_videos_data()

            while videoData[0] != video_count_now:
                await asyncio.sleep(5)
                print("pas le time")
                videoData = self.get_last_videos_data()
            return [True, videoData[1]]

        else:
            return [False]


def ajout_points(user_id):
    with open("Data/user.txt", "r") as fichier:
        dicoPoints = eval(fichier.read().strip())

        if user_id in dicoPoints:
            dicoPoints[user_id] += 1
        else:
            dicoPoints[user_id] = 1
        fichier.close()

    with open("Data/user.txt", "w") as fichier:
        fichier.write(str(dicoPoints))
        fichier.close()


def lecture_points(user_id):
    with open("Data/user.txt", "r") as fichier:
        dicoPoints = eval(fichier.read().strip())
        fichier.close()

    if user_id in dicoPoints:
        return dicoPoints[user_id]
    else:
        return 0


def classement():
    with open("Data/user.txt", "r") as fichier:
        dicoPoints = eval(fichier.read().strip())
        fichier.close()

    dicoPoints = {
        k: v
        for k, v in sorted(dicoPoints.items(), key=lambda item: item[1], reverse=True)
    }
    return dicoPoints


def blague(type):
    if type == "blonde":
        url = "http://www.top-blagues.com/blagues-Blondes.html"
        color = 0xFFD700
    elif type == "divers":
        url = "http://www.top-blagues.com/blagues-Divers.html"
        color = 0x008000
    elif type == "belges":
        url = "http://www.top-blagues.com/blagues-Belges.html"
        color = 0xFF4500
    elif type == "animaux":
        url = "http://www.top-blagues.com/blagues-Animaux.html"
        color = 0x1E90FF
    elif type == "couples":
        url = "http://www.top-blagues.com/blagues-Couples.html"
        color = 0xFF69B4
    elif type == "devinettes":
        url = "http://www.top-blagues.com/blagues-Devinettes.html"
        color = 0x8B4513
    elif type == "stupides":
        url = "http://www.top-blagues.com/blagues-Stupides.html"
        color = 0x2E8B57
    elif type == "mr et mme":
        url = r"http://www.top-blagues.com/blagues-Mr%20et%20Mme....html"
        color = 0xDAA520
    elif type == "actualites":
        url = "http://www.top-blagues.com/blagues-Actualites.html"
        color = 0xADFF2F
    elif type == "informatique":
        url = "http://www.top-blagues.com/blagues-Informatique.html"
        color = 0xFF00FF
    elif type == "contrepeteries":
        url = "http://www.top-blagues.com/blagues-Contrepeteries.html"
        color = 0x00FFFF
    elif type == "pour enfants":
        url = r"http://www.top-blagues.com/blagues-Pour%20enfants.html"
        color = 0xDC143C
    elif type == "fetes":
        url = "http://www.top-blagues.com/blagues-Fetes.html"
        color = 0x00008B
    else:
        url = None
        color = 0x000000

    # Envoyer une requête HTTP pour obtenir le contenu de la page
    response = requests.get(url)

    # Vérifier si la requête s'est bien passée (code de statut 200 signifie succès)
    if response.status_code == 200:
        # Analyser le contenu HTML de la page en utilisant BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        res = soup.find_all("div", class_="blague")
        liste = []
        for i in res:
            liste.append(i.text)

        num = random.randint(0, len(liste) - 1)
        return liste[num], url, color
    else:
        return None


def bonjour(mess: str):
    mots_de_salutation = [
        "bonjour",
        "salut",
        "selem",
        "yo",
        "coucou",
        "hey",
        "hello",
        "hi",
        "hola",
        "yop",
        "wesh",
        "cc",
        "slt",
        "bjr",
        "bonsoir",
    ]
    mots_du_message = mess.split()
    mot_ok = False
    for mot in mots_du_message:
        if mot in mots_de_salutation:
            mot_ok = True

    return mot_ok


def pixelate(image_path, max_pixel):
    image = Image.open(image_path)
    original_size = image.size

    maximum = max(image.size)
    width = image.size[0] * max_pixel // maximum
    height = image.size[1] * max_pixel // maximum

    image = image.resize((width, height), Image.NEAREST)
    # image.resize(original_size, Image.NEAREST).show()

    return image


emoji_dico = {
    "🟥": {"hex": "dd2e44", "rgb": (248, 49, 47)},
    "🟧": {"hex": "f4900c", "rgb": (255, 103, 35)},
    "🟨": {"hex": "fdcb58", "rgb": (255, 176, 46)},
    "🟩": {"hex": "78b159", "rgb": (0, 210, 106)},
    "🟪": {"hex": "aa8ed6", "rgb": (199, 144, 241)},
    "🟦": {"hex": "55acee", "rgb": (0, 166, 237)},
    "🟫": {"hex": "c1694f", "rgb": (165, 105, 83)},
    "⬛": {"hex": "31373d", "rgb": (0, 0, 0)},
    "⬜": {"hex": "e6e7e8", "rgb": (255, 255, 255)},
}

palette = []
for dico in emoji_dico.values():
    palette.extend(dico["rgb"])


def emoji_correspondant(rgb):
    for element, valeurs in emoji_dico.items():
        if np.array_equal(valeurs["rgb"], rgb):
            return element


def changePalette(img: Image.Image, colors, dither):
    palette = Image.new("P", (16, 16))
    palette.putpalette(colors)

    img = img.convert("RGBA")
    img = img.convert("RGB").quantize(palette=palette, dither=dither)
    img = img.convert("RGB")

    return img


def image_to_txt(image_path, taille_max, dither):
    pixelated = pixelate(image_path, taille_max)
    coloredModif = changePalette(pixelated, palette, dither)

    matrice = np.array(coloredModif)

    res = ""
    cpt = 0
    for ligne in matrice:
        for elem in ligne:
            res += emoji_correspondant(elem)
            cpt += 1
        res += "\n"
    return res


def download_image(url, filename="temp.jpg"):
    response = requests.get(url)
    with open(filename, "wb") as file:
        file.write(response.content)
    return filename


def verif_taille(image_path, taille_max):
    pixelated = pixelate(image_path, taille_max)
    matrice = np.array(pixelated)
    taille = matrice.shape
    return taille[0] * taille[1] < 1000
