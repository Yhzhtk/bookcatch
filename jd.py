# coding=utf-8
'''
Created on 2013-7-23
jd的配置文件
@author: gudh
'''
import time

addlebkurl = "http://cread.e.jd.com/openread/openRead.action?callback=jsonp%d053&_=%d850&bookId=%s&readType=0"
bookurl = "http://e.jd.com/%s.html"

namereg = '''<div class="fl" id="name".*?<h2>(.*?)<'''
authorreg = '''<span>作&nbsp;&nbsp;&nbsp;&nbsp;者：</span>\\s*<a .*?>(.*?)<'''
cateareareg = '''<div class="fl">(.*?)</div>'''
catereg = '''<a .*?>(.*?)</a>'''
coverimgreg = '''<div id="spec-n1" class="jqzoom"><img src="(.*?)"'''
descreg = '''<h3>内容简介</h3>.*?<div class="con">(.*?)</div>'''
chaptersreg = '''<h3>目录</h3>.*?<div class="con">(.*?)</div>'''
sizereg = '''<div>文件大小：(.*?)M'''

def get_addbook_url(bookId):
    t = int(time.time())
    return addlebkurl % (t,t+15320,bookId) 

def get_book_url(bookId):
    return bookurl % bookId
