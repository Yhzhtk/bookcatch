# coding=gbk
'''
Created on 2013-7-22
�������
@author: gudh
'''

import win32api,win32con,win32gui
import time
import ImageGrab,Image
import os

def move(loc):
    '''�ƶ����'''
    win32api.SetCursorPos(loc)

def click(left=True):
    '''�������'''
    if left:
        d = win32con.MOUSEEVENTF_LEFTDOWN
        u = win32con.MOUSEEVENTF_LEFTUP
    else:
        d = win32con.MOUSEEVENTF_RIGHTDOWN
        u = win32con.MOUSEEVENTF_RIGHTUP
    win32api.mouse_event(d, 0, 0) 
    time.sleep(0.01)
    win32api.mouse_event(u, 0, 0)
    time.sleep(0.01)

def cut(dect):
    '''��Ļ��ͼ'''
    im = ImageGrab.grab()
    im1 = im.crop(dect)
    return im1

def save(img, path):
    '''����ͼƬ'''
    img.save(path)
    spath = path.replace("high", "low")
    img.save(spath, 'JPEG', quality = 95)

def white(img):
    '''�ж��Ƿ���ȫ��ɫ'''
    size = img.size
    for x in range(size[0]):
        for y in range(size[1]):
            print img.getpixel((x, y))
            if img.getpixel((x, y)) != (255, 255, 255):
                return False
    return True

def prgb(img):
    '''��ӡ����RGB'''
    size = img.size
    for x in range(size[0]):
        for y in range(size[1]):
            print x,y,img.getpixel((x, y))

def iscu(img, w, h, p):
    '''�Ƿ��Ǵ���'''
    size = img.size
    arr = []
    for y in range(size[1]):
        arx = []
        for x in range(size[0]):
            pix = img.getpixel((x, y))
            r = False
            if pix[0] < p and pix[1] < p and pix[2] < p:
                # �ж����ص��Ƿ�����ڵ�����
                r = True
                if x >= w and y >= h:
                    # ����Ѿ���ȡ�����شﵽ�жϷ�Χ����з�Χ�ж�
                    b = True
                    # ����x,yΪ�����ǰ��w,h��������������ж��Ǵ��壬�������������ж�
                    for i in range(x-w, x):
                        for j in range(y-h, y):
                            b &= arr[j][i]
                            if not b:
                                break
                        else: continue
                        break
                    if b:
                        return True
            # ����ǰ������Ϣ��¼������
            arx.append(r)
        arr.append(arx)
    return False

# dect = (600, 600, 720, 720)
# img = cut(dect)
# save(img, "c:/a.jpg")
for i in range(202,206):
    p = r"D:\dd\�ø�ĸ��������һ��\high\%d.jpg".encode("gbk") % i
    if os.path.exists(p):
        img = Image.open(p)
        print p,iscu(img, 3, 3, 50)


