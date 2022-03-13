# -*- coding: utf-8 -*-

"""
扫描文件夹下md文件中图片引用 与 文件夹下图片文件 对比
删除没有引用的图片文件
详细步骤：
1. 扫描文件夹将md文件和图片文件存入数组
2. 遍历md文件内容，获取所有图片引用
3. 将正确的图片引用从图片数组中删除
4. 图片数组中剩下的图片是未引用的图片可以删除
5. 通过调用系统函数删除

正则表达式：
1. 常规引用 形如 ![]()
(?:!\[在这里插入图片描述\]\((.*?)\)) # 只提取url
(?:!\[(.*?)\]\((.*?)\)) # 提取描述与rul

2. html引用 形如 <img src="image-20220123110227320.png" alt="image-20220123110227320" style="zoom:50%;" />
src=\".*(?=\")\"
"""

import os
import re

# 删除开关，请谨慎操作
enable_delete = 0

path = "/Users/yangzhendong/Library/Mobile Documents/com~apple~CloudDocs/Typora/学习/数据结构算法/算法题题解/分类题解"
file_names = os.listdir(path)
md_list = []
pic_list = []

for file_name in file_names:
    suffix_name = file_name.split(".")[-1]
    if suffix_name in ["md"]:
        print("发现Markdown：" + file_name)
        md_list.append(file_name)
    if suffix_name in ["png", "jpg", "jpeg", "gif", "svg"]:
        print("发现图片：" + file_name)
        pic_list.append(file_name)

print("--------------------------------------------------")
print("Markdown列表：", md_list)
print("图片列表：", pic_list)
print("--------------------------------------------------")

for md_name in md_list:
    print("--------------------------------------------------")
    print("文章：", md_name)
    with open(path + "/" + md_name, 'r+') as f:
        content = f.read()
        # 查找常规引用
        pic_info = re.findall(r'(?:!\[(.*?)\]\((.*?)\))', content)
        print("本文图片信息：", pic_info.__len__(), pic_info)
        for info in pic_info:
            if info[1] in pic_list:
                print("发现正确图片引用：", info[1])
                pic_list.remove(info[1])

        # 查找HTML引用
        pic_info_html = re.findall(r'src=\".*(?=\")\"', content)
        print("本文HTML图片信息：", pic_info_html.__len__(), pic_info_html)
        for info in pic_info_html:
            img_url = info.split("\"")[1]
            if img_url in pic_list:
                print("发现正确HTML图片引用：", img_url)
                pic_list.remove(img_url)

print("--------------------------------------------------")
print("未引用可删除图片列表：", pic_list.__len__(), pic_list)
print("--------------------------------------------------")

if enable_delete:
    for pic in pic_list:
        url = path + "/" + pic
        print("准备删除图片：", url)
        os.remove(url)
