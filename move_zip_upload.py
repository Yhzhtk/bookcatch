# coding=utf-8
'''
Created on 2013-8-30
打包上线
@author: gudh
'''

import bookauto, time

if __name__ == '__main__':
    # 打包上传的数量
    count = 1
    zip_path = "D:/ebook_zip/%s/" % time.strftime("%Y%m%d")
    bookauto.before_deal(count, zip_path)