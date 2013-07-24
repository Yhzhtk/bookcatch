# coding=gbk
'''
Created on 2013-7-22
使用win32操作Demo
@author: gudh
'''

import win32gui,win32api,win32con
import time

DialogName = "登录".encode("gbk")
ButtonName = "登录".encode("gbk")

win = win32gui.FindWindow(0,DialogName) #获取窗口句柄，以窗口title获取
while win == 0: #为0表示没有找到
    win = win32gui.FindWindow(0,DialogName)
    
#win32api.MessageBox(0, "请先运行**".encode("gbk"), "错误！".encode("gbk"), win32con.MB_ICONERROR)
#win32api.SendMessage(win,16) #发送16是关闭窗口的意思

time.sleep(1) # 休眠X秒
hbtn = win32gui.FindWindowEx(win,None,None,ButtonName) #获取按钮句柄
(left,top,right,bottom) = win32gui.GetWindowRect(hbtn) #获取按钮区域
win32api.SetCursorPos((left+(right-left)/2,top+(bottom-top)/2)) #光标定位按钮
time.sleep(0.5)

# 鼠标点击
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0) 
time.sleep(0.05)
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
time.sleep(0.05)

#获取和移动鼠标位置
oldCursorPos = win32gui.GetCursorPos()
win32api.SetCursorPos((1,1))

#上面代码慢且容易出错，可以直接用发消息的方式，更快也不容易出错：
savewin = win32gui.FindWindow(None,'Save as...')
inputfile = win32gui.GetDlgItem(savewin,0x47C)
win32gui.SendMessage(inputfile,win32con.WM_SETTEXT,0,'result')
savebtn = win32gui.GetDlgItem(savewin,1)
win32gui.SendMessage(savebtn,win32con.BM_CLICK,0,0)

