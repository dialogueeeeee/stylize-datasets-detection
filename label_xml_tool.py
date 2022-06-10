"""
    @Author  : DaiYalun
    @Time    : 2022/6/10
    @Comment : xml 文件更新
"""

import os
from xml.dom.minidom import parse

def update_filename(file_path, file_name, image_name):
    original_file   = os.path.join(file_path, file_name)
    domTree         = parse(original_file)
    rootNode        = domTree.documentElement

    names = rootNode.getElementsByTagName("name")
    for name in names:
        if name.childNodes[0].data == "Acme Inc.":
            # 获取到name节点的父节点
            pn = name.parentNode
            # 父节点的phone节点，其实也就是name的兄弟节点
            # 可能有sibNode方法，我没试过，大家可以google一下
            phone = pn.getElementsByTagName("phone")[0]
            # 更新phone的取值
            phone.childNodes[0].data = 99999