# -*- coding: utf-8 -*-

"""
基于md_file_pic_scan的扫描md和图片的方式
详细步骤：
1. 扫描文件夹将md文件和图片文件存入数组
2. 遍历md文件内容，获取所有图片引用
3. 若有正确的图片引用，新建.assets文件夹，将图片复制进去
4. 修改md文件中的引用
"""

import os
import re
import html


path = "/Users/yangzhendong/Library/Mobile Documents/com~apple~CloudDocs/Typora/学习/Java/基础知识点"
file_names = os.listdir(path)
md_list = []
existed_pic_list = []

for file_name in file_names:
    suffix_name = file_name.split(".")[-1]
    if suffix_name in ["md"]:
        print("发现Markdown：" + file_name)
        md_list.append(file_name)
    if suffix_name in ["png", "jpg", "jpeg", "gif", "svg"]:
        print("发现图片：" + file_name)
        existed_pic_list.append(file_name)

print("--------------------------------------------------")
print("Markdown列表：", md_list)
print("图片列表：", existed_pic_list)
print("--------------------------------------------------")

for md_name in md_list:
    print("--------------------------------------------------")
    print("开始处理文章：", md_name)
    md_related_pic_list = []
    md_error_pic_list = []
    need_move_pic_list = []
    with open(path + "/" + md_name, 'r+') as f:
        content = f.read()

        md_raw_name = md_name[:-3]
        dic_assets_name = md_raw_name + ".assets"
        print("当前文章图片目录:", dic_assets_name + "/")

        # 查找常规引用
        pic_info = re.findall(r'(?:!\[(.*?)\]\((.*?)\))', content)
        print("本文非HTML图片信息：", pic_info.__len__(), pic_info)
        for info in pic_info:
            # 若图片在和文档同级目录中
            if info[1] in existed_pic_list:
                print("发现正确图片引用：", info[1])
                md_related_pic_list.append(info[1])
                need_move_pic_list.append(info[1])
            # 若图片在assets文件夹中，也算正确
            elif html.unescape(info[1].split("/")[0]) == dic_assets_name:
                print("发现assets文件夹内正确图片引用：", info[1])
                md_related_pic_list.append(info[1])
            else:
                print("发现找不到图片的引用：", info[1])
                md_error_pic_list.append(info[1])

        # 查找HTML引用
        pic_info_html = re.findall(r'src=\".*(?=\")\"', content)
        print("本文HTML图片信息：", pic_info_html.__len__(), pic_info_html)
        for info in pic_info_html:
            img_url = info.split("\"")[1]
            if img_url in existed_pic_list:
                print("发现正确HTML图片引用：", img_url)
                md_related_pic_list.append(img_url)
                need_move_pic_list.append(img_url)
            # 若图片在assets文件夹中，也算正确
            elif html.unescape(img_url.split("/")[0]) == dic_assets_name:
                print("发现assets文件夹内正确HTML图片引用：", img_url)
                md_related_pic_list.append(img_url)
            else:
                print("发现找不到HTML图片的引用：", img_url)
                md_error_pic_list.append(img_url)

    print(
        "本文正确引用数量：%s 本文图片数量 %s 本文HTML图片数量 %s 本文缺失图片数量 %s " % (md_related_pic_list.__len__(),
                                                                                          pic_info.__len__(),
                                                                                          pic_info_html.__len__(),
                                                                                          md_error_pic_list.__len__()))
    print("本文有图片引用且有实际图片的列表：", md_related_pic_list)
    print("本文有图片引用但无实际图片的列表：", md_error_pic_list)
    print("本文需要移动的图片：", need_move_pic_list)

    # 移动需要移动的图片
    if need_move_pic_list.__len__() > 0:
        # 创建.assets文件夹
        if not os.path.exists(path + "/" + dic_assets_name):
            os.mkdir(path + "/" + dic_assets_name)
            print("创建.assets文件夹成功")
        else:
            print("已存在.assets文件夹")

        # 移动图片
        for pic in need_move_pic_list:
            url = path + "/" + pic
            print("准备移动图片：", url)
            os.rename(url, path + "/" + dic_assets_name + "/" + pic)
            print("完成移动图片到：", path + "/" + dic_assets_name + "/" + pic)


