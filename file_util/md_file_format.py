# -*- coding: utf-8 -*-


"""
处理Markdown文件，自动加入Hexo博客所需标签等信息，自动加入"阅读更多"分割线
详细步骤：
1. 处理文件夹下文件名称
2. 在文件头部插入标签等信息
3. 在文件中间某行插入分隔符<!-- more -->
"""

import os

path = "/Users/yangzhendong/Desktop/blog"
files = os.listdir(path)

datanames = os.listdir(path)
for file_name in datanames:
    # 只取文件名
    file_name_real = file_name
    file_name = file_name.split(".")[0]
    # print("处理文件：" + file_name)
    file_name = file_name.replace("[", "【")
    file_name = file_name.replace("]", "】")
    file_name = file_name.replace("_", " ")
    print("处理名称文件：" + file_name)

    # 在文件头部插入
    with open('/Users/yangzhendong/Desktop/blog/' + file_name_real, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write('---\ntitle: ' + file_name + '\ntags: [旧文归档]\ncategories: 旧文归档\n---\n\n' + content)

    # 插入中间
    lines = []
    insert_line = 0
    with open('/Users/yangzhendong/Desktop/blog/' + file_name_real, 'r+') as f:
        for i in f.readlines():
            lines.append(i)
            insert_line = insert_line + 1
            if insert_line == 10:
                lines.append('\n\n<!-- more -->\n\n')
    with open('/Users/yangzhendong/Desktop/blog/' + file_name_real, 'w') as f:
        for line in lines:
            f.write(line)



