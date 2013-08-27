# coding=utf-8
'''
Created on 2013-8-27
@author: gudh
'''

import Image
import traceback, os

def zoom_cover(cover_path):
    try:
        img = Image.open(cover_path)
        size = os.path.getsize(cover_path) / 1024
        qua = 70
        if size > 20:
            qua = 5
        elif size > 15:
            qua = 10
        elif size > 10:
            qua = 20
        elif size > 5:
            qua = 30
        img.save(cover_path, 'JPEG', quality = qua)
    except:
        traceback.print_exc()

def deal_cover(path):
    for root, dirs, files in os.walk(path): 
        for f in files:
            if f.endswith(".jpg"):
                fname = os.path.join(root, f)
                print "deal cover %s" % fname
                zoom_cover(fname)

if __name__ == '__main__':
    deal_cover("")