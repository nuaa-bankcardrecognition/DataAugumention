'''
object的数据结构
'''


class Object_node:
    def __init__(self, name, difficult, xmin, ymin, xmax, ymax):
        self.name = name
        self.difficult = difficult
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
