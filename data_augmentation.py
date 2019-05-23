from PIL import Image
import numpy as np
import os
import xml.etree.ElementTree as ET
import my_object_node
from xml_generate import write_xml
import math


def rand(a=0, b=1):
    return np.random.rand() * (b - a) + a


def number_rotate(xmin, ymin, xmax, ymax, angle, image_x, image_y):
    # 角度转换成弧度
    angle = -angle * math.pi / 180.0
    center_x = image_x / 2.0
    center_y = image_y / 2.0
    # print(center_x)
    # print(angle)
    x = [xmin, xmax, xmin, xmax]
    y = [ymin, ymin, ymax, ymax]
    # 旋转公式
    # x = (x1 - x2)cosθ - (y1 - y2)sinθ + x2
    # y = (x1 - x2)sinθ + (y1 - y2)cosθ + y2
    # 逆时针旋转的情况
    if angle < 0:
        nxmin = (x[0] - center_x) * math.cos(angle) - (y[0] - center_y) * math.sin(angle) + center_x
        nymin = (x[1] - center_x) * math.sin(angle) + (y[1] - center_y) * math.cos(angle) + center_y
        nymax = (x[2] - center_x) * math.sin(angle) + (y[2] - center_y) * math.cos(angle) + center_y
        nxmax = (x[3] - center_x) * math.cos(angle) - (y[3] - center_y) * math.sin(angle) + center_x
    # 顺时针旋转的情况
    else:
        nymin = (x[0] - center_x) * math.sin(angle) + (y[0] - center_y) * math.cos(angle) + center_y
        nxmax = (x[1] - center_x) * math.cos(angle) - (y[1] - center_y) * math.sin(angle) + center_x
        nxmin = (x[2] - center_x) * math.cos(angle) - (y[2] - center_y) * math.sin(angle) + center_x
        nymax = (x[3] - center_x) * math.sin(angle) + (y[3] - center_y) * math.cos(angle) + center_y

    return (str(int(nxmin)), str(int(nymin)), str(int(nxmax)), str(int(nymax)))


def augmentate(src_path, dest_path, src_xml_path, dest_xml_path):
    for file in os.listdir(src_path):
        file_path = os.path.join(src_path, file)
        print(file_path)
        image = Image.open(file_path)
        # w, h = image.size
        tmp = image
        for i in range(20):
            image = tmp
            # 随机生成缩放比例 (针对分辨率)
            # scale = rand(.25, 2)
            # image = image.resize((int(scale * w), int(scale * h)), Image.BICUBIC)
            # 角度范围 [-10,-1] & [1,10]
            scale = i - 10
            # 避免做数字运算的时候除数为 0
            if scale == 0:
                continue
            # print(scale)
            # 对jpg文件操作
            image = image.rotate(scale)
            image.save(dest_path + '\\' + file[0:7] + '_' + str(i + 1) + '.jpg')
            # 对xml文件操作
            my_src_xml_path = os.path.join(src_xml_path, file[0:7] + '.xml')
            my_dest_xml_path = os.path.join(dest_xml_path, file[0:7] + '_' + str(i + 1) + '.xml')
            object_list = []
            in_file = open(my_src_xml_path)
            tree = ET.parse(in_file)
            root = tree.getroot()

            for obj in root.iter('object'):
                cls = obj.find('name').text
                xmlbox = obj.find('bndbox')
                b = (float(xmlbox.find('xmin').text), float(xmlbox.find('ymin').text), float(xmlbox.find('xmax').text),
                     float(xmlbox.find('ymax').text))
                # 图片旋转对选定框也需更改
                nb = number_rotate(b[0], b[1], b[2], b[3], scale, image.size[0], image.size[1])
                one = my_object_node.Object_node(cls, '0', nb[0], nb[1], nb[2], nb[3])
                object_list.append(one)
            # 生成一个新的xml文件
            write_xml(object_list, my_dest_xml_path)


if __name__ == "__main__":
    # src_path = 'origin_image'
    src_path = 'JPEGImages'
    dest_path = 'generate_image'
    src_xml_path = 'complex_xml'
    # src_xml_path = 'Annotations'
    dest_xml_path = 'generate_xml'
    augmentate(src_path, dest_path, src_xml_path, dest_xml_path)
