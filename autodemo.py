# coding=gbk
'''
Created on 2013-7-22
ʹ��win32����Demo
@author: gudh
'''

import win32gui,win32api,win32con
import time

DialogName = "��¼".encode("gbk")
ButtonName = "��¼".encode("gbk")

win = win32gui.FindWindow(0,DialogName) #��ȡ���ھ�����Դ���title��ȡ
while win == 0: #Ϊ0��ʾû���ҵ�
    win = win32gui.FindWindow(0,DialogName)
    
#win32api.MessageBox(0, "��������**".encode("gbk"), "����".encode("gbk"), win32con.MB_ICONERROR)
#win32api.SendMessage(win,16) #����16�ǹرմ��ڵ���˼

time.sleep(1) # ����X��
hbtn = win32gui.FindWindowEx(win,None,None,ButtonName) #��ȡ��ť���
(left,top,right,bottom) = win32gui.GetWindowRect(hbtn) #��ȡ��ť����
win32api.SetCursorPos((left+(right-left)/2,top+(bottom-top)/2)) #��궨λ��ť
time.sleep(0.5)

# �����
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0) 
time.sleep(0.05)
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
time.sleep(0.05)

#��ȡ���ƶ����λ��
oldCursorPos = win32gui.GetCursorPos()
win32api.SetCursorPos((1,1))

#��������������׳�������ֱ���÷���Ϣ�ķ�ʽ������Ҳ�����׳���
savewin = win32gui.FindWindow(None,'Save as...')
inputfile = win32gui.GetDlgItem(savewin,0x47C)
win32gui.SendMessage(inputfile,win32con.WM_SETTEXT,0,'result')
savebtn = win32gui.GetDlgItem(savewin,1)
win32gui.SendMessage(savebtn,win32con.BM_CLICK,0,0)

