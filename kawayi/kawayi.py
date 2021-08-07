import base64
import json
import os

from PIL import Image
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import \
    TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ft.v20200304 import ft_client, models

from .config import *
from .sdk.aip import AipImageProcess

LABEL_SUMMER = os.path.join(os.path.dirname(
    __file__), "../static/bilibili_summer.png")


class Anime():

    def __init__(self):
        self.__client_baidu = AipImageProcess(APP_ID, API_KEY, SECRET_KEY)
        self.__client_tencent = None

        def t_init():
            try:
                cred = credential.Credential(TENCENT_SEC_ID, TENCENT_SECRECT)
                httpProfile = HttpProfile()
                httpProfile.endpoint = "ft.tencentcloudapi.com"

                clientProfile = ClientProfile()
                clientProfile.httpProfile = httpProfile
                self.__client_tencent = ft_client.FtClient(
                    cred, "ap-shanghai", clientProfile)

            except TencentCloudSDKException as err:
                print(err)
        t_init()

    """ 读取图片 """

    def __call__(self, file_path, new_path, new_label_path=None, is_tencent=False) -> str:
        if is_tencent:
            self.add_label(file_path, new_label_path)
            return self.__call_tencent(new_label_path, new_path)
        else:
            self.__call_baidu(file_path, new_path)
            if new_label_path:
                self.add_label(new_path, new_label_path)
                return new_label_path
            return new_path

    def __get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def __get_file_b64_str(self, file_path):
        with open(file_path, 'rb') as fp:
            return base64.b64encode(fp.read()).decode()

    def __save_base64_img(self, b64, file_path):
        with open(file_path, "wb") as fh:
            fh.write(base64.b64decode(b64))

    def ttt(self, file_path):
        return self.__call_tencent(file_path)

    def __call_tencent(self, file_path) -> str:
        image = self.__get_file_b64_str(file_path)

        params = {
            # "Action": "FaceCartoonPic",
            # "Version": "2020-03-04",
            # "Region": "ap-shanghai",
            "Image": image,
            "RspImgType": "url",  # base64/url url expire in 24h
            # "DisableGlobalEffect": False
        }

        req = models.FaceCartoonPicRequest()

        req.from_json_string(json.dumps(params))

        resp = self.__client_tencent.FaceCartoonPic(req)
        print("tencent resp: ", resp)
        return eval(resp.to_json_string())["ResultUrl"]

    def __call_baidu(self, file_path, new_path):
        image = self.__get_file_content(file_path)

        """ 调用人物动漫化 """
        self.__client_baidu.selfieAnime(image)

        """ 如果有可选参数 """
        options = {
            "type": "anime",
            # "type": "anime_mask",
            # "mask_id": 3,
        }

        """ 调用人物动漫化, 图片参数为本地图片 """
        resp = self.__client_baidu.selfieAnime(image, options)
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
