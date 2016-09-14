# coding:gbk

import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

_letter_cases = "abcdefghijklmnopqrstuvwxyz"                   # Сд��ĸ
_upper_cases = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"                    # ��д��ĸ
_numbers = "0123456789"                                         # ����
init_chars = ''.join([_letter_cases, _upper_cases, _numbers])   # ����������ַ�����
default_font = "./Arial.ttf"                                   # ��֤������


# ������֤��ӿ�
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
    image = Image.new(mode, (width, height), bg_color)          # ����ͼ��
    draw = ImageDraw.Draw(image)                                # ��������

    def get_chars():
        return random.sample(chars, length)

    def create_lines():
        """���Ƹ�����"""
        line_num = random.randint(*n_line)  # 1����2
        for i in xrange(line_num):
            begin_point = (random.randint(0, size[0]), random.randint(0, size[1]))
            end_point = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line((begin_point, end_point), fill=(0, 0, 0))

    def create_points():
        """ ���Ƹ��ŵ�"""
        chance = min(100, max(0, int(point_chance)))    # ����������0-100
        for x in xrange(width):
            for y in xrange(height):
                temp = random.randint(0, 100)
                if temp > 100 - chance:
                    draw.point((x, y), fill=(0, 0, 0))

    # ������֤���ı�
    def create_strings():
        c_chars = get_chars()
        strings = ' '.join(c_chars)
        font = ImageFont.truetype(font_type, font_size)             # �������������������С
        font_width, font_height = font.getsize(strings)                # �����ı��Ŀ�Ⱥ͸߶�
        # position���������ı����Ͻǵ�λ��
        draw.text(((width - font_width) / 3, (height - font_height) / 3), strings, font=font, fill=fg_color)
        return ''.join(c_chars)

    if draw_lines:
        create_lines()
    if draw_points:
        create_points()
    strs = create_strings()

    # ͼ��Ť������
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
