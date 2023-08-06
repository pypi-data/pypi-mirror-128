# -*- coding=utf-8 -*-

import os, zipfile


# 打包目录为zip文件
def zip(src_dir, zfile_name):
    if not os.path.isdir(src_dir):
        print("The first arg is not dir, please check!")
        return False

    zfile = zipfile.ZipFile(zfile_name + '.zip', 'w')
    pre_len = len(os.path.dirname(src_dir))
    for parent, dirnames, filenames in os.walk(src_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)
            zfile.write(pathfile, arcname)
    zfile.close()


if __name__ == '__main__':
    zip("E:/django/package/tar", "ttt")  # 注意结尾带不带 / 打包的目录层数不一样
    # zip("E:/django/package/tar/", "ttt")
