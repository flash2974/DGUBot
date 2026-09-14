import os

from dotenv import load_dotenv


load_dotenv()

# twitter
ID = "__Flash__74__"
CHANNEL_ID_TWITTER = 1201117117836173405
CHANNEL_ID_YT = 1201110452374097940


DIC_SERVEUR = {
    "DGU": [
        706305950323048459,
        1104162966691135598,
        1106706201875599370,
        1006741760162144296,
    ],  # id serveur, id ctrl blind test, id blind test, id role
    "Polytech": [
        1030116220244078662,
        1179713532154089492,
        1179713492408873081,
        1030117372775903232,
    ],
    "Test": [
        1109562836251836620,
        1109562837602422888,
        1116718903498899517,
        1116691415116816478,
    ],
}


serv_utilise = "Test"
serveur = DIC_SERVEUR[serv_utilise][0]
ctrl_blind_test = DIC_SERVEUR[serv_utilise][1]
blind_test_play = DIC_SERVEUR[serv_utilise][2]
idRole = DIC_SERVEUR[serv_utilise][3]

TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")
