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
    __uuid = uuid.uuid4()
    local_img, anime_img = img_paths(__uuid)
    print(local_img, anime_img)
    # TODO 把文件保存到地址 local_img

    _kawayi(local_img)
    return "kawayi"


def img_paths(__uuid: str):
    return os.path.join(image_folder, __uuid + ".png"), os.path.join(image_folder, __uuid + "_anime.png")

# 以下は、試しに動かしてみる
# return static image path


def _kawayi(fpath: str):
    print("恭喜你转换卡通成功!!!")
    return
