# coding=utf-8
'''
Created on 2013-7-22
拍书操作
@author: gudh
'''

import win32api,win32con,win32gui
import time
import ImageGrab
import os
import bookconfig,bookorm

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
    time.sleep(0.1)
    win32api.mouse_event(u, 0, 0)
    time.sleep(0.1)

def double_click():
    '''双击鼠标'''
    click()
    time.sleep(0.1)
    click()

def move_click_sleep(pos_sleep):
    '''移动鼠标，点击，并延时'''
    move(pos_sleep[0:2])
    click()
    time.sleep(pos_sleep[2])

def move_double_click_sleep(pos_sleep):
    '''移动鼠标，双击，并延时'''
    move(pos_sleep[0:2])
    double_click()
    time.sleep(pos_sleep[2])

def cut(dect):
    '''返回屏幕截图'''
    im = ImageGrab.grab()
    im1 = im.crop(dect)
    return im1

def save(img, path, qualit=85):
    '''保存图片'''
    if not os.path.exists(os.path.split(path)[0]):
        os.makedirs(os.path.split(path)[0])
    img.save(path, 'JPEG', quality = qualit)

def is_white(img):
    '''判断是否是全白色'''
    size = img.size
    for x in range(size[0]):
        for y in range(size[1]):
            if img.getpixel((x, y)) != (255, 255, 255):
                return False
    print "iswhite true"
    return True

def print_rgb(img):
    '''打印所有RGB'''
    size = img.size
    for x in range(size[0]):
        for y in range(size[1]):
            print x,y,img.getpixel((x, y))

def is_bold(img, blod_para):
    '''是否是粗体'''
    size = img.size
    arr = []
    (w, h, p) = blod_para
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

def is_equal(img1, img2, jump=1):
    '''判断两张图片是否一致'''
    if img1 == None or img2 == None:
        return False
    size = img1.size
    if size != img2.size:
        return False
    for y in range(0, size[1], jump):
        for x in range(0, size[0], jump):
            if img1.getpixel((x, y)) != img2.getpixel((x, y)):
                return False
    print "isequal true"
    return True

def shot_book(img_dect, inner_blank_sleep, next_pos_sleep, nid, cid):
    '''拍书'''
    flag = 0
    path = bookconfig.rootpath + time.strftime("%Y%m%d") + "/content/%s/" + nid[0:2] + "/" + nid[2:4] + "/" + nid[4:] + "/%s/%s.jpg"
    last_img = None
    i = 0
    # 点击空白位
    move_click_sleep(inner_blank_sleep)
    while True:
        i += 1
        img = cut(img_dect)
        if is_white(img) or is_equal(img, last_img):
            # 判断是否拍图到结束
            flag += 1
            if flag > 1:
                i -= 1
                break
            else:
                i -= 1
                continue
        else:
            flag = 0
        s_i = str(i)
        if is_bold(img, bookconfig.blod_para):
            s_i = s_i + "_b"
        hpath = path % ("h", cid, s_i)
        lpath = path % ("l", cid, s_i)
        save(img, hpath)
        save(img, lpath, 30)
        print "save ok: " + hpath
        # 记录上一张图片
        last_img = img
        # 翻页到下一张
        move_click_sleep(next_pos_sleep)
    
    book = bookorm.get_book(nid)
    book.imgCount = i
    book.upTime()
    bookorm.save_book(book)

def pos_to_first_book(down_time=10):
    '''从上一本书的结尾定位到第一本畅读的阅读页'''
    
    move_click_sleep(bookconfig.fhsj_pos_sleep)
    move_click_sleep(bookconfig.wdcd_pos_sleep)
    move_click_sleep(bookconfig.sx_pos_sleep)
    move_click_sleep(bookconfig.zxcd_first_pos_sleep)
    move_double_click_sleep(bookconfig.zxcd_first_pos_sleep)
    print "begin down book sleep: %d" % down_time
    time.sleep(down_time) # 下载时间
    move_double_click_sleep(bookconfig.zxcd_first_pos_sleep)
    move_double_click_sleep(bookconfig.zxcd_first_pos_sleep)

def shot_first_book(nid, cid="1", down_time=10):
    '''拍最前面一本书'''
    pos_to_first_book(down_time)
    start_pos = bookconfig.start_pos
    shot_size = bookconfig.shot_size
    dect = (start_pos[0], start_pos[1], start_pos[0] + shot_size[0], start_pos[1] + shot_size[1])
    shot_book(dect, bookconfig.inner_blank_sleep, bookconfig.next_pos_sleep, nid, cid)

if __name__ == '__main__':
    time.sleep(2)
    nid = "49be5990e3ec92ad8e9fcc3a25b391d2"
    shot_first_book(nid)

