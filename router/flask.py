import logging
import os
import uuid

from kawayi import Anime

from flask import Flask, request

from ..kawayi import Anime

app = Flask(__name__)

anime = Anime()

image_folder = os.path.join(
    os.path.dirname(
        os.path.realpath(__file__)),
    "../image"
)

log = logging.Logger()


@app.route("/upload", methods=["POST"])
def index():
    if request.method == "POST":
        def run():
            __uuid = uuid.uuid4()
            local_img, anime_img = img_paths(str(__uuid))
            log.info("生成文件地址", local_img, anime_img)

            f = request.files.get('file')
            f.save(local_img)
            _kawayi(local_img, anime_img)
            return "kawayi"

        try:
            return run()
        except Exception as e:
            log.error(e)
            return str(e.with_traceback())


def img_paths(__uuid: str):
    return os.path.join(image_folder, __uuid + ".png"), os.path.join(image_folder, __uuid + "_anime.png")

# 以下は、試しに動かしてみる
# return static image path


def _kawayi(fpath: str, fpath_anime: str):
    log.info("正在进行图片包转换中", fpath, fpath_anime)
    anime(fpath, fpath_anime)
    log.info("恭喜你转换卡通成功!!!")
    return
