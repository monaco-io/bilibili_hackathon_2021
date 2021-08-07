import os

from kawayi import Anime

from flask import Flask

app = Flask(__name__)

anime = Anime()

image_folder = os.path.join(
    os.path.dirname(
        os.path.realpath(__file__)),
    "../image"
)


@app.route("/")
def index():
    _kawayi("xxx")
    return "kawayi"


def img_path(p):
    return os.path.join(image_folder, p)


def cal(_uuid):
    return anime(img_path(_uuid+".png"), img_path(_uuid+"_anime.png"))


# 以下は、試しに動かしてみる
# return static image path
def _kawayi(fpath: str) -> str:
    pass
