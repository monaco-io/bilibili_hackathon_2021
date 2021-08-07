import os
import uuid

from flask import Flask
from flask import request

from kawayi import Anime

app = Flask(__name__)

anime = Anime()

image_folder = os.path.join(
    os.path.dirname(
        os.path.realpath(__file__)),
    "../image"
)


@app.route("/upload", methods=["POST"])
def index():
    if request.method == "POST":
        __uuid = uuid.uuid4()
        local_img, anime_img = img_paths(str(__uuid))
        print(local_img, anime_img)

        f = request.files.get('file')
        f.save(local_img)
        _kawayi(local_img)
        return "kawayi"


def img_paths(__uuid: str):
    return os.path.join(image_folder, __uuid + ".png"), os.path.join(image_folder, __uuid + "_anime.png")

# 以下は、試しに動かしてみる
# return static image path


def _kawayi(fpath: str):
    print("恭喜你转换卡通成功!!!")
    return


if __name__ == "__main__":
    print('fuck')
