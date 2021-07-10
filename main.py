import os
import uuid

from kawayi import Anime

anime = Anime()

image_folder = os.path.join(
    os.path.dirname(
        os.path.realpath(__file__)),
    "image"
)


def img_path(p):
    return os.path.join(image_folder, p)


def cal(_uuid):
    return anime(img_path(_uuid+".png"), img_path(_uuid+"_anime.png"))


if __name__ == "__main__":

    __uuid = uuid.uuid4()

    try:
        cal(__uuid)
    except Exception as e:
        print(e)
