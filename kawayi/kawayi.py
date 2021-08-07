import base64
import os

from PIL import Image

from .config import *
from .sdk.aip import AipImageProcess

LABEL_SUMMER = os.path.join(os.path.dirname(
    __file__), "../static/bilibili_summer.png")


class Anime():

    def __init__(self):
        self.__client = AipImageProcess(APP_ID, API_KEY, SECRET_KEY)

    """ 读取图片 """

    def __call__(self, file_path, new_path, new_label_path=None):
        self.__calculate(file_path, new_path)
        if new_label_path:
            self.add_label(new_path, new_label_path)

    def __get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def __save_base64_img(self, b64, file_path):
        with open(file_path, "wb") as fh:
            fh.write(base64.b64decode(b64))

    def __calculate(self, file_path, new_path):
        image = self.__get_file_content(file_path)

        """ 调用人物动漫化 """
        self.__client.selfieAnime(image)

        """ 如果有可选参数 """
        options = {
            "type": "anime",
            # "type": "anime_mask",
            # "mask_id": 3,
        }

        """ 调用人物动漫化, 图片参数为本地图片 """
        resp = self.__client.selfieAnime(image, options)
        log_id = resp["log_id"]
        image_b64 = resp["image"]

        print("log_id: ", log_id)
        # print("image_b64: ", image_b64)
        self.__save_base64_img(image_b64, new_path)
        return new_path

    def add_label(self, file_path, file_label_path):
        img = Image.open(file_path)
        label_img = Image.open(LABEL_SUMMER)
        layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        layer.paste(label_img, (0, 0))
        out = Image.composite(layer, img, layer)
        out.save(file_label_path)

        img.close()
        label_img.close()
