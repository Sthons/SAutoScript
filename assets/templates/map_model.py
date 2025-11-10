

class MM():

    def __init__(self):
        pass

    def load(self, img_name: str):
        """
            获取映射坐标
            :param img_name: 图片名称
            :return: img_name, x, y
        """
        coordinate = self.map_dict.get(img_name, ())
        if not coordinate:
            raise ValueError(f"未找到图片 {img_name} 的映射坐标")

        return img_name, *coordinate

    map_dict = {
        "mod\\general\\again.png": (0, 0),
    }


