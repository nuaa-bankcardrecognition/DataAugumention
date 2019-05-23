import xml.etree.ElementTree as ET
import os
import my_object_node
from xml_generate import write_xml

'''
把两份xml数据整合到一起
'''

def convert_annotation(src_path, src2_path, origin_dest_path):
    for file in os.listdir(src_path):
        file_path = os.path.join(src_path, file)

        dest_path = os.path.join(origin_dest_path, file)

        object_list = []

        in_file = open(file_path)
        tree = ET.parse(in_file)
        root = tree.getroot()

        for obj in root.iter('object'):
            cls = obj.find('name').text
            xmlbox = obj.find('bndbox')
            b = ((xmlbox.find('xmin').text), (xmlbox.find('ymin').text), (xmlbox.find('xmax').text),
                 (xmlbox.find('ymax').text))

            one = my_object_node.Object_node(cls, '0', b[0], b[1], b[2], b[3])
            object_list.append(one)

        file_path2 = os.path.join(src2_path, file)
        in_file2 = open(file_path2,encoding="utf-8")
        tree2 = ET.parse(in_file2)
        root2 = tree2.getroot()

        for obj2 in root2.iter('object'):
            cls2 = obj2.find('name').text
            xmlbox2 = obj2.find('bndbox')
            b2 = ((xmlbox2.find('xmin').text), (xmlbox2.find('ymin').text), (xmlbox2.find('xmax').text),
                  (xmlbox2.find('ymax').text))

            # number 选用第一份文档里面的
            if cls2 == 'number':
                continue
            one = my_object_node.Object_node(cls2, '0', b2[0], b2[1], b2[2], b2[3])
            object_list.append(one)

        write_xml(object_list, dest_path)


if __name__ == "__main__":
    convert_annotation('upleft_xml', 'number_xml', 'complex_xml')
