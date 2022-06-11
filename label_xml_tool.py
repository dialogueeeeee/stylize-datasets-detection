"""
    @Author  : Dai Yalun
    @Time    : 2022/6/10
    @Comment : xml 文件更新
"""

import os
from xml.dom.minidom import parse

def update_filename(image_path, image_name):
    output_image    = os.path.join(image_path, image_name)
    domTree         = parse(original_file)
    rootNode        = domTree.documentElement

    filename    = rootNode.getElementsByTagName("filename")
    path        = rootNode.getElementsByTagName("path")
    filename.childNodes[0].data = image_name
    path.childNodes[0].data     = output_image
