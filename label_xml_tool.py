"""
    @Author  : Dai Yalun
    @Time    : 2022/6/10
    @Comment : xml 文件更新
"""

import os
from xml.dom.minidom import parse

def update_filename(xml_file, image_name, image_file):
    domTree         = parse(xml_file)
    rootNode        = domTree.documentElement

    filename    = rootNode.getElementsByTagName("filename")[0]
    path        = rootNode.getElementsByTagName("path")[0]
    filename.childNodes[0].data = image_name
    path.childNodes[0].data     = image_file

    with open(xml_file, 'w') as f:
        domTree.writexml(f, addindent=' ', encoding='utf-8')
