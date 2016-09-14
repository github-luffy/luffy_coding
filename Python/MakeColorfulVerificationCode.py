# coding:gbk

import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

_letter_cases = "abcdefghijklmnopqrstuvwxyz"                   # 小写字母
_upper_cases = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"                    # 大写字母
_numbers = "0123456789"                                         # 数字
init_chars = ''.join([_letter_cases, _upper_cases, _numbers])   # 生成允许的字符集合
default_font = "./Arial.ttf"                                   # 验证码字体


# 生成验证码接口
def generate_verify_image(size=(60 * 4, 60),
                          mode='RGB',
                          image_type="JPEG",
                          bg_color=(255, 255, 255),
                          fg_color=(0, 0, 255),
                          chars=init_chars,
                          length=4,
                          font_type=default_font,
                          font_size=36,
                          draw_lines=True,
                          n_line=(1, 2),
                          draw_points=True,
                          point_chance=2,
                          save_img=False):

    width, height = size
    image = Image.new(mode, (width, height), bg_color)          # 创建图形
    draw = ImageDraw.Draw(image)                                # 创建画笔

    def get_chars():
        return random.sample(chars, length)

    def create_lines():
        """绘制干扰线"""
        line_num = random.randint(*n_line)  # 1或者2
        for i in xrange(line_num):
            begin_point = (random.randint(0, size[0]), random.randint(0, size[1]))
            end_point = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line((begin_point, end_point), fill=(0, 0, 0))

    def create_points():
        """ 绘制干扰点"""
        chance = min(100, max(0, int(point_chance)))    # 点数控制在0-100
        for x in xrange(width):
            for y in xrange(height):
                temp = random.randint(0, 100)
                if temp > 100 - chance:
                    draw.point((x, y), fill=(0, 0, 0))

    # 创建验证码文本
    def create_strings():
        c_chars = get_chars()
        strings = ' '.join(c_chars)
        font = ImageFont.truetype(font_type, font_size)             # 设置字体类型与字体大小
        font_width, font_height = font.getsize(strings)                # 返回文本的宽度和高度
        # position给出的是文本左上角的位置
        draw.text(((width - font_width) / 3, (height - font_height) / 3), strings, font=font, fill=fg_color)
        return ''.join(c_chars)

    if draw_lines:
        create_lines()
    if draw_points:
        create_points()
    strs = create_strings()

    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 2)) / 100,
              0,
              0.0000007,
              float(random.randint(1, 2)) / 500]
    image = image.transform(size, Image.PERSPECTIVE, params)
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)

    mstream = StringIO.StringIO()
    image.save(mstream, image_type)

    if save_img:
        image.save('validate.' + image_type.lower(), image_type)
    return mstream, strs

if __name__ == '__main__':
    mstream, strs = generate_verify_image(save_img=True)
    print strs
