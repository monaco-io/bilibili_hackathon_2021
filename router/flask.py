import base64
import logging
import os
import uuid

from flask_cors import cross_origin
from kawayi import Anime

from flask import Flask, request, send_file

app = Flask(__name__)

anime = Anime()

image_folder = os.path.join(
    os.path.dirname(
        os.path.realpath(__file__)),
    "../image"
)

log = logging.Logger("bilibili-anime")
log.setLevel(logging.DEBUG)


@app.route("/upload", methods=["POST"])
@cross_origin()
def index():
    if request.method == "POST":
        def run():
            log.info("开始上传图片 ...")
            __uuid = uuid.uuid4()
            local_img, anime_img, label_img = img_paths(str(__uuid))
            log.info("生成文件地址", local_img, anime_img)

            f = request.files.get('file')
            f.save(local_img)
            is_tencent = request.args.get("is_tencent")
            log.info("is_tencent", is_tencent)
            if is_tencent:
                is_tencent = True
            if is_tencent == "false":
                is_tencent = False
            tencent_cdn_path = _kawayi(
                local_img, anime_img, label_img, is_tencent)
            if is_tencent:
                return tencent_cdn_path
            return send_file(label_img, mimetype='image/png')

        try:
            return run()
        except Exception as e:
            log.error("crash !!!", e)
            return e


def img_paths(__uuid: str):
    return os.path.join(image_folder, __uuid + ".png"), os.path.join(image_folder, __uuid + "_anime.png"), os.path.join(image_folder, __uuid + "_label.png")

# 以下は、試しに動かしてみる
# return static image path


def _kawayi(fpath: str, fpath_anime: str, fpath_label: str, is_tencent: bool = False):
    log.info("正在进行图片包转换中", fpath, fpath_anime)
    p = anime(fpath, fpath_anime, fpath_label, is_tencent)
    log.info("恭喜你转换卡通成功!!!")
    return p
