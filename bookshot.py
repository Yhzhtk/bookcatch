# coding=utf-8
'''
Created on 2013-7-22

@author: gudh
'''

import win32api,win32con,win32gui
import time
import ImageGrab,Image
import os

def move(loc):
    '''移动鼠标'''
    win32api.SetCursorPos(loc)

def click(left=True):
    '''单击鼠标'''
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
    '''屏幕截图'''
    im = ImageGrab.grab()
    im1 = im.crop(dect)
    return im1

def save(img, path):
    '''保存图片'''
    img.save(path)
    spath = path.replace("high", "low")
    img.save(spath, 'JPEG', quality = 95)

def white(img):
    '''判断是否是全白色'''
    size = img.size
    for x in range(size[0]):
        for y in range(size[1]):
            print img.getpixel((x, y))
            if img.getpixel((x, y)) != (255, 255, 255):
                return False
    return True

def prgb(img):
    '''打印所有RGB'''
    size = img.size
    for x in range(size[0]):
        for y in range(size[1]):
            print x,y,img.getpixel((x, y))

def iscu(img, w, h, p):
    '''是否是粗体'''
    size = img.size
    arr = []
    for y in range(size[1]):
        arx = []
        for x in range(size[0]):
            pix = img.getpixel((x, y))
            r = False
            if pix[0] < p and pix[1] < p and pix[2] < p:
                # 判断像素点是否满足黑的条件
                r = True
                if x >= w and y >= h:
                    # 如果已经获取的像素达到判断范围则进行范围判断
                    b = True
                    # 在以x,y为坐标的前面w,h点均满足条件则判断是粗体，否则跳出继续判断
                    for i in range(x-w, x):
                        for j in range(y-h, y):
                            b &= arr[j][i]
                            if not b:
                                break
                        else: continue
                        break
                    if b:
                        return True
            # 将当前像素信息记录到数组
            arx.append(r)
        arr.append(arx)
    return False

# dect = (600, 600, 720, 720)
# img = cut(dect)
# save(img, "c:/a.jpg")
for i in range(202,206):
    p = r"D:\dd\好父母决定孩子一生\high\%d.jpg".encode("gbk") % i
    if os.path.exists(p):
        img = Image.open(p)
        print p,iscu(img, 3, 3, 50)


