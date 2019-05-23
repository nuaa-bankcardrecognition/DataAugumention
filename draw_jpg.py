from PIL import Image, ImageFont, ImageDraw
import numpy as np
import my_object_node
import xml.etree.ElementTree as ET

'''
用以验证数据增强部分处理是否得当
'''


def draw_jpg(image_path, xml_path):
    image = Image.open(image_path)
    # 厚度
    thickness = (image.size[0] + image.size[1]) // 300
    # global draw
    my_draw = ImageDraw.Draw(image)

    object_list = []
    in_file = open(xml_path)
    tree = ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        cls = obj.find('name').text
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text),
             int(xmlbox.find('ymax').text))
        one = my_object_node.Object_node(cls, '0', b[0], b[1], b[2], b[3])
        object_list.append(one)

    for one in object_list:
        top = one.ymin
        left = one.xmin
        bottom = one.ymax
        right = one.xmax

        # 画框
        my_draw.rectangle([left, top, right, bottom])
        # for i in range(thickness):
        #     my_draw.rectangle([left + i, top + i, right - i, bottom - i], outline=None)

    del my_draw

    image.show()


if __name__ == '__main__':
    image_path = 'origin_image/cyw0012_1.jpg'
    xml_path = 'number_xml/cyw0012_1.xml'
    draw_jpg(image_path, xml_path)
    image_path = 'origin_image/cyw0012.jpg'
    xml_path = 'number_xml/cyw0012.xml'
    draw_jpg(image_path, xml_path)
