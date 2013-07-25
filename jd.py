# coding=gbk
'''
Created on 2013-7-23
jd的配置文件
@author: gudh
'''
import time

addlebkurl = "http://cread.e.jd.com/openread/openRead.action?callback=jsonp%d053&_=%d850&bookId=%s&readType=0"
bookurl = "http://e.jd.com/%s.html"
cookie = "__utma=122270672.572055792.1368524510.1368524510.1368524510.1; __utmz=122270672.1368524510.1.1.utmcsr=jd.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _jzqa=1.1097886078779985200.1368525250.1368525250.1368696109.2; _jzqx=1.1368525250.1368696109.2.jzqsr=item%2Ejd%2Ecom|jzqct=/592191%2Ehtml.jzqsr=item%2Ejd%2Ecom|jzqct=/310607%2Ehtml; aview=967.1016278229|2690.1014848697|880.1020205892|880.530472|880.777621|880.183314|6977.265763|700.836670; atw=700.836670.30|693.592191.14|880.1020205892.9|967.1016278229.5|2690.1014848697.4|2691.310607.2|6977.265763.-1|694.503212.-6; ipLocation=%u5317%u4EAC; ipLoc-djd=1-2800-2851-0; eb=0; cn=0; JD_lastTime30022649=%7B%22bookId%22%3A%2230022649%22%2C%22readType%22%3A%221%22%2C%22curPage%22%3A%221%22%2C%22charterIndex%22%3A%223%22%2C%22curPId%22%3A%223%22%2C%22word%22%3A%22%E4%BB%80%E4%B9%88%E6%98%AF%E5%95%86%E6%9C%BA%EF%BC%9F%E5%B9%B6%E4%B8%8D%E6%98%AF%E7%AD%89%E6%89%80%E6%9C%89%E7%9A%84%E4%BA%BA%E9%83%BD%E7%9C%8B%E6%B8%85%E4%BA%86%E6%89%8D%E6%98%AF%22%2C%22isDoubleModel%22%3A%22true%22%2C%22skinIndex%22%3A%221%22%2C%22multipleIndex%22%3A%221%22%2C%22catalogId%22%3A%2228506434%22%7D; _pst=jd_62f28d4daaeef; pin=jd_62f28d4daaeef; unick=jd_yd7611; ceshi3.com=FE3CFDAC8B33C696145B5875B5AC4A2145BFD9A588D90339FE718291493B77C2F0BCA48F3BDEB0E14E326AC40A72F30375CC856EA7933F9FDD5427AC66A3D8AD1142A1B1C835D0FB29D3B3E017FE839FD608628771D5F24239538DE121CC69163AE77AC7BF0A0AAD40C93705F449205BC2CBE421DFD344EF70AF5201237393210731EEC0589CBA550139C5C9D4A8FE1AB26119CE04AAFAB368A984793525F523; __jda=122270672.664423796.1367563664.1374471909.1374561179.15; __jdb=122270672.22.664423796|15.1374561179; __jdc=122270672; __jdv=122270672|www.jd.com|-|referral|-; _jzqco=%7C%7C%7C%7C1374561196135%7C1.966261202.1367563664193.1374562220084.1374563060535.1374562220084.1374563060535..0.0.148.148"

namereg = '''<div class="fl" id="name".*?<h2>(.*?)<'''
authorreg = '''<span>作&nbsp;&nbsp;&nbsp;&nbsp;者：</span>\\s*<a .*?>(.*?)<'''
cateareareg = '''<div class="fl">(.*?)</div>'''
catereg = '''<a .*?>(.*?)</a>'''
coverimgreg = '''<div id="spec-n1" class="jqzoom"><img src="(.*?)"'''
descreg = '''<h3>内容简介</h3>.*?<div class="con">(.*?)</div>'''
chaptersreg = '''<h3>目录</h3>.*?<div class="con">(.*?)</div>'''

rootpath = "F:/ebook/"

def get_addbook_url(bookId):
    t = int(time.time())
    return addlebkurl % (t,t+15320,bookId) 

def get_book_url(bookId):
    return bookurl % bookId




