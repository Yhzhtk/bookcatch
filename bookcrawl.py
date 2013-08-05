# coding=utf-8
'''
Created on 2013-7-23
抓取书
@author: gudh
'''
import re,os,time,traceback
import urllib,urllib2,Image
import jd,bookconfig
from bookmode import Shotbook,Chapter
import bookorm,bookshot

import socket,time
#这里对整个socket层设置超时时间。后续文件中如果再使用到socket，不必再设置
socket.setdefaulttimeout(10)

def get_url_content(url, headers={}):
    '''以指定UA获取网页内容'''
    headers.update(bookconfig.default_header)
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    html = get_code_str(html)
    return html

def urlcallback(a,b,c):
    """
        call back function
        a,已下载的数据块
        b,数据块的大小
        c,远程文件的大小
    """
    print "callback"
    prec= 100.0 * a * b / c
    if 100 < prec:
        prec = 100
    print "%.2f%%"%(prec,), a, b, c

def down_file(url, path, headers={}):
    '''下载策略，失败则多次下载'''
    n = 6
    sleep = 3
    ok = False
    for i in range(n):
        if __down_file(url, path, headers, i % 3):
            ok = True
            break
        print "%d sleep %d and contine." % (i,sleep)
        time.sleep(sleep)
    print "down file:" + str(ok)
    return ok

def __down_file(url, path, headers={}, style=0):
    '''下载文件'''
    try:
        if style == 0:
            urllib.urlretrieve(url, path, urlcallback)
            return True
        elif style == 1:
            headers.update(bookconfig.default_header)
            req = urllib2.Request(url, None, headers)
            data = urllib2.urlopen(req).read()
            with open(path, "wb") as code:  
                code.write(data)
            return True
        elif style == 2:
            request = urllib.urlopen(url)#这里是要读取内容的url  
            data = request.read()
            with open(path, "wb") as code:
                code.write(data)
            request.close()#记得要关闭
            return True
        else:
            raise Exception,"no this style"
    except Exception, e:
        print "down file error : " + str(e)
        return False

def print_local_info():
    '''打印本机的UA和IP信息'''
    ip_url = "http://iframe.ip138.com/ic.asp"
    content = get_url_content(ip_url)
    ip = regex_one('''<center>(.*?)</''', content)
    print "IP:" + ip
    
    ua_url = "http://useragentstring.com/"
    content = get_url_content(ua_url)
    ua = regex_one('''<textarea name='uas' id='uas_textfeld' rows='4' cols='30'>(.*?)<''', content)
    print "UA:" + ua

def regex_one(regex, content, group=1):
    '''正则查找第一个匹配返回指定分组'''
    pattern = re.compile(regex, re.DOTALL)
    match = pattern.search(content)
    return match.group(group)

def regex_all(regex, content, group=1):
    '''正则查找所有匹配返回指定分组'''
    pattern = re.compile(regex, re.DOTALL)
    matchs = pattern.finditer(content)
    return [match.group(group) for match in matchs if match]

def get_code_str(s, ts="gbk", cs="utf-8"):
    '''获取指定编码'''
    return str(s).decode(ts).encode(cs)

def add_book_to_lebook(bookId):
    '''将书添加到客户端，事先需要设置好jd的cookie'''
    url = jd.get_addbook_url(bookId)
    content = get_url_content(url, {"Cookie" : bookconfig.cookie})
    print "成功", content
    return '"message":"成功"' in content

def del_cover(path):
    '''默认封面处理'''
    im = Image.open(path)
    if im.size[0] > 275 and im.size[0] < 285 and im.size[1] > 275 and im.size[1] < 285:
        dect = (40, 0, 240, 280)
        im = im.crop(dect)
        bookshot.save(im, path)

def crawl_book(bookId):
    '''抓取并解析书的信息'''
    book = None
    try:
        book = Shotbook(bookId)
        url = jd.get_book_url(bookId)
        content = get_url_content(url)
        
        book.bookName = regex_one(jd.namereg, content)
        book.author = regex_one(jd.authorreg, content)
        book.set_id_coverpath() # 由书名和作者名生成nid和封面路径
        catearea = regex_one(jd.cateareareg, content)
        catelist = regex_all(jd.catereg, catearea)
        cate = u"分类"
        for i in range(len(catelist) - 1, -1, -1):
            cate = catelist[i]
            if cate not in ["其他", "其它"]:
                break
        book.type = cate.replace("/", "").replace("、", "")
        book.coverurl = regex_one(jd.coverimgreg, content)
        book.bookSize = int(float(regex_one(jd.sizereg, content)) * 1000)
        
        # 当书大小大于多少，则不再抓取
        if book.bookSize > bookconfig.max_book_size:
            print "bookSize more than max_book_size: %d" % book.bookSize
            return None
        
        desc = regex_one(jd.descreg, content).replace("<br />"," ").replace("　","").replace(" ", "").strip()
        desc = re.sub("<.*?>", "", desc)
        book.description = desc
        chapterarea = regex_one(jd.chaptersreg, content)
        # 处理章节中的尖括号
        nchapters = []
        for cc in re.split("<br ?/?>", chapterarea):
            if not cc:
                continue
            for c in re.split("</?p>", cc):
                c = c.replace("&nbsp;", " ").strip()
                if c:
                    print c
                    nchapters.append(c)
        book.chapters = [Chapter(book.nid, str(i), line, book.bookName, book.author, 0) for (i,line) in enumerate(nchapters, 1)]
        # 完善章节信息
        book.complete_chapter()
        
        # 下载封面
        cover_path = bookconfig.rootpath + time.strftime("%Y%m%d") + "/cover/" + book.coverImgPath
        # 如果路径不存在，则先创建路径
        if not os.path.exists(os.path.split(cover_path)[0]):
            os.makedirs(os.path.split(cover_path)[0])
        print "begin down cover: %s\n%s" % (cover_path,book.coverurl)
        down_file(book.coverurl, cover_path)
        # 安装默认方法处理封面图片
        del_cover(cover_path)
    except Exception:
        book = None
        print traceback.format_exc()
    
    return book

def crawl_insert_books(book_id):
    '''抓取指定ID的信息并插入数据库，返回书的列表'''
    print "-"*10 + "\r\ncrawl id: %s" % book_id
    book = None
    try:
        if bookorm.exist_book(book_id):
            print "%s has exist, continue" % book_id
        else:
            print "begin crawl: %s" % book_id
            book = crawl_book(book_id)
            if book != None:
                print "begin insert: %s %s %s" % (book.bookName, book.nid, book_id) 
                bookorm.insert_book_chapter(book)
    except Exception:
        print traceback.format_exc()
        book = None
    return book

if __name__ == '__main__':
    print_local_info()
    for bid in range(35023124,35023125):
        crawl_insert_books(str(bid))
