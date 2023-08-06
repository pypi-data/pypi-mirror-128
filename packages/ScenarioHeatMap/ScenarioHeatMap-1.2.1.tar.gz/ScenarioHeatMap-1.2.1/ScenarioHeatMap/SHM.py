"""
@author:HY
@time:2021/11/21:22:37
"""

from PIL import ImageDraw2, Image
import matplotlib.pyplot as plt
import numpy as np
import cv2


def generate_heatmap_color(n=240):
    """
    制作颜热区图色盘，HSL色彩，蓝色到红色的过渡色盘
    :param n:
    :return:
    """
    colors = []
    n1 = int(n * 0.4)
    n2 = n - n1
    for i in range(n1):
        color = "hsl(240, 100%%, %d%%)" % (100 * (n1 - i / 2) / n1)
        colors.append(color)
    for i in range(n2):
        color = "hsl(%.0f, 100%%, 50%%)" % (240 * (1.0 - float(i) / n2))
        colors.append(color)
    return colors


def is_num(v):
    """
    判断是否为数字
    """
    if type(v) in (int, float):
        return True
    if ("%d" % v).isdigit():
        return True
    return False


def generate_circle(r, w):
    """
    根据半径r以及图片宽度 w ，产生一个圆的list
    :param r:
    :param w:
    :return:
    """
    position_dic = {}

    def get_position(ix, iy, v=1):
        # 8对称性,通过八分之一圆获得整个圆的坐标
        ps = (
            (ix, iy),
            (-ix, iy),
            (ix, -iy),
            (-ix, -iy),
            (iy, ix),
            (-iy, ix),
            (iy, -ix),
            (-iy, -ix),
        )
        for x2, y2 in ps:
            p = w * y2 + x2
            position_dic.setdefault(p, v)  # 键值对 key=p, value=v

    # 中点圆画法,根据推导，遍历八分之一圆，所以终止条件是x = y的时候
    x = 0
    y = r
    d = 3 - (r << 1)  # 左移一位，即 * 2。 递推关系式，大于0时候选择下面的点，小于0时候选择上面的点
    while x <= y:
        for k in range(x, y + 1):
            get_position(x, k, y + 1 - k)
        if d < 0:
            d += (x << 2) + 6
        else:
            d += ((x - y) << 2) + 10
            y -= 1  # y不断变小
        x += 1  # x不断变大
    return position_dic.items()


class HeatMap(object):

    def __init__(self, data, base=None, width=0, height=0, screen_cross=False, transparency=0.5, colorful=False):
        """
        :param data: 热力点数据
        :param base: 给定图也可以取出长宽
        :param width: 图片的长
        :param height: 图片的宽
        :param screen_cross: 是否允许边界的色块在另一个方向出现
        :param transparency: 透明度
        :param colorful: 是否彩色图片
        """
        assert type(data) in (list, tuple)
        # assert base is None or os.path.isfile(base)

        if base is None:
            self.width = width
            self.height = height
            self.base = None
        else:
            self.width = base.shape[1]
            self.height = base.shape[0]
            self.base = Image.new("RGB", (self.width, self.height), color=0)

        self.image = base
        self.data = data
        self.save_as = None
        self.screen_cross = screen_cross
        self.transparency = transparency
        self.colorful = colorful
        self.My_Heat_Map = None
        self.My_Heat_Map_without_base = None

    def __geo_pixel(self, lng, lat):
        """
        从坐标点转移到像素点位置，其中坐标是左下为起点，而像素点是左上为起点
        :return:
        """
        y = int((self.Dlat - lat) / self.ODlat * self.height)
        x = int((lng - self.Olng) / self.ODlng * self.width)
        return x, y

    def __generate_image(self):
        base = self.base
        self.__im0 = None

        if base:
            str_type = (str,)
            self.__im0 = Image.open(base) if type(base) in str_type else base
            self.width, self.height = self.__im0.size

        self.__im = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))

    def __get_heatmap_data(self, heat_data, x, y, n, template, r):
        """

        :param heat_data:
        :param x:
        :param y:
        :param n: 1
        :param template:
        :return:
        """

        l = len(heat_data)
        width = self.width
        p = width * y + x

        for ip, iv in template:
            p2 = p + ip
            now_x, now_y = p2 % width, p // width

            if self.screen_cross:
                if 0 <= p2 < l:
                    heat_data[p2] += iv * n
            else:
                # 防止图片色块穿越
                if abs(y - now_y) <= r and abs(x - now_x) <= r and 0 <= p2 < l:
                    heat_data[p2] += iv * n

    def __paint_heat(self, heat_data, colors, max_weight=-1, min_weight=-1):
        """"""

        import re

        im = self.__im
        rr = re.compile(", (\d+)%\)")  # 将正则表达式转化为对象
        dr = ImageDraw2.ImageDraw.Draw(im)
        width = self.width
        height = self.height

        max_v = max(heat_data) if max_weight == -1 else max_weight
        min_v = min(heat_data) if min_weight == -1 else min_weight
        self.max_heat = max(heat_data)
        self.min_heat = min(heat_data)

        max_v -= min_v

        if max_v <= 0:
            return

        r = 240.0 / max_v
        heat_data2 = [int(i * r) - 1 for i in heat_data]

        size = width * height

        for p in range(size):
            v = heat_data2[p]  # 记录颜色， 并且p可以分解出x、y坐标也就是每个位置对应的颜色
            if v > 0:
                x, y = p % width, p // width  # 地板除，先除再向下取整
                color = colors[v]
                alpha = int(rr.findall(color)[0])
                if alpha > 50:
                    # continue
                    al = 255 - 255 * (alpha - 50) // 50
                    im.putpixel((x, y), (0, 0, 250, al))
                else:
                    dr.point((x, y), fill=color)

    def __add_base(self):
        if not self.__im0:
            return

        self.__im0.paste(self.__im, mask=self.__im)
        self.__im = self.__im0

    def __heatmap_plus(self):
        if self.colorful:
            hit_img = cv2.cvtColor(np.asarray(self.__im), cv2.COLOR_RGB2BGR, dstCn=4)  # Image格式转换成cv2格式 彩色底图则用4
        else:
            hit_img = cv2.cvtColor(np.asarray(self.__im), cv2.COLOR_RGB2BGR, dstCn=3)

        overlay = self.image.copy()
        alpha = self.transparency  # 设置覆盖图片的透明度
        cv2.rectangle(overlay, (0, 0), (self.image.shape[1], self.image.shape[0]), (0, 0, 0), -1)  # 设置蓝色为热度图基本色蓝色(255,0,0)

        My_Heat_Map = cv2.addWeighted(overlay, alpha, self.image, 1 - alpha, 0)  # 将背景热度图覆盖到原图
        My_Heat_Map = cv2.addWeighted(hit_img, alpha, My_Heat_Map, 1 - alpha, 0)  # 将热度图覆盖到原图

        self.My_Heat_Map = My_Heat_Map
        cv2.imshow('My_Heat_Map', My_Heat_Map)

        cv2.waitKey()

    def __save(self):
        if self.My_Heat_Map is not None:
            cv2.imwrite(self.save_as, self.My_Heat_Map)
        else:
            plt.savefig(self.save_as)

    def get_max_min_heat(self):
        """
        获取当前热力图中颜色的最大最小权重
        :return:
        """
        return self.max_heat, self.min_heat
    
    def data_transform(self, postion=None):
        """
        :param postion:  左下角坐标（Olng，Olat）右上角坐标（Dlng，Dlat）
        :return:
        """
        hit_num = 0  # 记录有几个点
        data_3D = []  # 处理成三维的data

        if postion is not None:
            Olng, Olat, Dlng, Dlat = postion
            self.Dlat = Dlat
            self.Olng = Olng
            self.ODlng = Dlng - Olng
            self.ODlat = Dlat - Olat

            new_data = []
            for one in self.data:
                x, y = self.__geo_pixel(one[0], one[1])
                new_data.append([x, y, 1])
                hit_num += 1
            self.data = new_data

        else:
            # 处理热力点位置
            for hit in self.data:
                if len(hit) == 3:
                    x, y, n = hit
                elif len(hit) == 2:
                    x, y, n = hit[0], hit[1], 1
                else:
                    raise Exception(u"length of hit is invalid!")

                data_3D.append((x, y, n))
                hit_num += n

            self.data = data_3D
        self.count = hit_num
        
    def heatmap(self, save_as=None, r=10, max_weight=-1, min_weight=-1):
        """
        绘制热图
        :param save_as:
        :param base:
        :param data:
        :param r:
        :return:
        """

        self.__generate_image()

        # 热力图的圈
        circle = generate_circle(r, self.width)

        heat_data = [0] * self.width * self.height  # 记录颜色,二维颜色位置记录在以为列表中

        for point in self.data:
            # 每一个中心点调一次
            x, y, n = point
            if x < 0 or x >= self.width or y < 0 or y >= self.height:  # 热力中点超出图像范围的点不要了
                continue

            self.__get_heatmap_data(heat_data, x, y, n, circle, r)

        self.__paint_heat(heat_data, generate_heatmap_color(), max_weight, min_weight)

        self.__add_base()

        if self.image is not None:
            self.__heatmap_plus()
            if save_as:
                self.save_as = save_as
                self.__save()
        else:
            plt.imshow(np.asarray(self.__im))
            plt.colorbar()
            if save_as:
                self.save_as = save_as
                self.__save()
            plt.show()



