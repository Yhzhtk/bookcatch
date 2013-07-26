# coding=gbk
'''
Created on 2013-7-22
�������
@author: gudh
'''

import win32api,win32con,win32gui
import time
import ImageGrab
import os
import bookconfig

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

def double_click():
    '''˫�����'''
    click()
    time.sleep(0.05)
    click()

def move_click_sleep(pos_sleep):
    '''�ƶ���꣬���������ʱ'''
    move(pos_sleep[0:2])
    click()
    time.sleep(pos_sleep[2])

def move_double_click_sleep(pos_sleep):
    '''�ƶ���꣬˫��������ʱ'''
    move(pos_sleep[0:2])
    double_click()
    time.sleep(pos_sleep[2])

def cut(dect):
    '''������Ļ��ͼ'''
    im = ImageGrab.grab()
    im1 = im.crop(dect)
    return im1

def save(img, path, qualit=85):
    '''����ͼƬ'''
    if not os.path.exists(os.path.split(path)[0]):
        os.makedirs(os.path.split(path)[0])
    img.save(path, 'JPEG', quality = qualit)

def is_white(img):
    '''�ж��Ƿ���ȫ��ɫ'''
    size = img.size
    for x in range(size[0]):
        for y in range(size[1]):
            if img.getpixel((x, y)) != (255, 255, 255):
                return False
    print "iswhite true"
    return True

def print_rgb(img):
    '''��ӡ����RGB'''
    size = img.size
    for x in range(size[0]):
        for y in range(size[1]):
            print x,y,img.getpixel((x, y))

def is_bold(img, w, h, p):
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

def is_equal(img1, img2, jump=1):
    '''�ж�����ͼƬ�Ƿ�һ��'''
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

def shot_book(img_dect, next_pos_sleep, nid, cid):
    '''����'''
    flag = 0
    path = bookconfig.rootpath + time.strftime("%Y%m%d") + "/content/%s/" + nid[0:2] + "/" + nid[2:4] + "/" + nid[4:] + "/%s/%s.jpg"
    last_img = None
    i = 0
    while True:
        i += 1
        img = cut(img_dect)
        if is_white(img) or is_equal(img, last_img):
            # �ж��Ƿ���ͼ������
            flag += 1
            if flag > 1:
                break
            else:
                i -= 1
                continue
        else:
            flag = 0
        s_i = str(i)
        if is_bold(img, 3, 3, 65):
            s_i = s_i + "_b"
        hpath = path % ("high", cid, s_i)
        lpath = path % ("low", cid, s_i)
        save(img, hpath)
        save(img, lpath, 30)
        print "save ok: " + hpath
        # ��¼��һ��ͼƬ
        last_img = img
        # ��ҳ����һ��
        move_click_sleep(next_pos_sleep)
        

def pos_to_first_book(down_time=10):
    '''����һ����Ľ�β��λ����һ���������Ķ�ҳ'''
    
    move_click_sleep(bookconfig.fhsj_pos_sleep)
    move_click_sleep(bookconfig.wdcd_pos_sleep)
    move_click_sleep(bookconfig.sx_pos_sleep)
    move_click_sleep(bookconfig.zxcd_first_pos_sleep)
    move_double_click_sleep(bookconfig.zxcd_first_pos_sleep)
    print "begin down book sleep: %d" % down_time
    time.sleep(down_time) # ����ʱ��
    move_double_click_sleep(bookconfig.zxcd_first_pos_sleep)

def shot_first_book(nid, cid="1", down_time=10):
    '''����ǰ��һ����'''
    pos_to_first_book(down_time)
    shot_book(bookconfig.dect, bookconfig.next_pos_sleep, nid, cid)

if __name__ == '__main__':
    time.sleep(2)
    nid = "49be5990e3ec92ad8e9fcc3a25b391d2"
    shot_first_book(nid)

