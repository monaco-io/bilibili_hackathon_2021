from PIL import Image


class Merger(object):
    def __init__(self, label_img_path=None):
        if not label_img_path:
            label_img_path = "./static/smoker.png"
        self.label_img = Image.open(label_img_path)

    def merge_img(self, user_img_path) -> str:
        '''
        合并两张图片
        '''
        assert user_img_path is not None,\
            'user_img不能为空'

        user_img = Image.open(user_img_path)
        layer = Image.new('RGBA', user_img.size, (0, 0, 0, 0))
        layer.paste(self.label_img, (0, 0))
        out = Image.composite(layer, user_img, layer)
        out.save('./static/haha.png')


if __name__ == '__main__':
    mg = Merger()
    mg.merge_img("./static/user_img.png")
