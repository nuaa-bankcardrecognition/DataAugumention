

from xml_merge_handler import convert_annotation
from data_augmentation import augmentate
# 两份xml数据合成在一次
convert_annotation('upleft_xml', 'number_xml', 'complex_xml')


# 数据增强
src_path = 'JPEGImages'
dest_path = 'generate_image'
src_xml_path = 'complex_xml'
dest_xml_path = 'generate_xml'
augmentate(src_path, dest_path, src_xml_path, dest_xml_path)
