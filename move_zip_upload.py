# coding=utf-8
'''
Created on 2013-8-30
打包上线
@author: gudh
'''

import bookauto, bookconfig
import time, os

if __name__ == '__main__':
    # 打包上传的数量
    count = -1
    zip_path = "D:/ebook_zip/%s/" % time.strftime("%Y%m%d")
    if os.path.exists(bookconfig.uploadfile):
        # 如果存在则备份
        uploadback = os.path.dirname(bookconfig.uploadfile) + "/upback/upload" + time.strftime("%Y%m%d") + ".txt"
        print "back upload to %s" % uploadback
        os.rename(bookconfig.uploadfile, uploadback)
    bookauto.before_deal(count, zip_path)
    # 打开需要上传的目录
    print u"请将目录 %s 中的zip文件全部上传到ftp中的 /ebook_zip/路径下，谢谢。" % zip_path
    os.startfile(zip_path)
