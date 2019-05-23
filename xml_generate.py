# -*- coding:utf8 -*-

import xml.dom.minidom as Dom
from xml.dom import minidom

'''
写入到xml文件
'''
# 这个方法用来代替minidom里格式化代码，实现节点不换行
def fixed_writexml(self, writer, indent="", addindent="", newl=""):
    writer.write(indent + "<" + self.tagName)
    attrs = self._get_attributes()
    a_names = attrs.keys()

    for a_name in a_names:
        writer.write(" %s=\"" % a_name)
        minidom._write_data(writer, attrs[a_name].value)
        writer.write("\"")
    if self.childNodes:
        if len(self.childNodes) == 1 \
                and self.childNodes[0].nodeType == minidom.Node.TEXT_NODE:
            writer.write(">")
            self.childNodes[0].writexml(writer, "", "", "")
            writer.write("</%s>%s" % (self.tagName, newl))
            return
        writer.write(">%s" % (newl))
        for node in self.childNodes:
            if node.nodeType is not minidom.Node.TEXT_NODE:
                node.writexml(writer, indent + addindent, addindent, newl)
        writer.write("%s</%s>%s" % (indent, self.tagName, newl))
    else:
        writer.write("/>%s" % (newl))


minidom.Element.writexml = fixed_writexml


def write_xml(object_list, src_path):
    doc = Dom.Document()
    root_node = doc.createElement("annotation")
    doc.appendChild(root_node)

    for one in object_list:
        object_node = doc.createElement("object")

        name_node = doc.createElement("name")
        name_value = doc.createTextNode(one.name)
        name_node.appendChild(name_value)

        difficult_node = doc.createElement("difficult")
        difficult_value = doc.createTextNode(one.difficult)
        difficult_node.appendChild(difficult_value)

        bndbox = doc.createElement("bndbox")
        # bndbox中写入min_value
        xmin_node = doc.createElement("xmin")
        xmin_value = doc.createTextNode(one.xmin)
        xmin_node.appendChild(xmin_value)
        bndbox.appendChild(xmin_node)
        # bndbox中写入ymin_value
        ymin_node = doc.createElement("ymin")
        ymin_value = doc.createTextNode(one.ymin)
        ymin_node.appendChild(ymin_value)
        bndbox.appendChild(ymin_node)
        # bndbox中写入xmax_value
        xmax_node = doc.createElement("xmax")
        xmax_value = doc.createTextNode(one.xmax)
        xmax_node.appendChild(xmax_value)
        bndbox.appendChild(xmax_node)
        # bndbox中写入ymax_value
        ymax_node = doc.createElement("ymax")
        ymax_value = doc.createTextNode(one.ymax)
        ymax_node.appendChild(ymax_value)
        bndbox.appendChild(ymax_node)
        # obeject中写入name
        object_node.appendChild(name_node)
        # oject中写入difficult
        object_node.appendChild(difficult_node)
        # oject中写入bndbox
        object_node.appendChild(bndbox)
        # annotation中写入object_node
        root_node.appendChild(object_node)

    # print(doc.toxml("utf-8"))
    f = open(src_path, "wb")
    f.write(doc.toprettyxml(indent="\t", newl="\n", encoding="utf-8"))
    f.close()


if __name__ == "__main__":
    write_xml()
