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

def get_url_content(url, headers={}):
    '''以指定UA获取网页内容'''
    headers.update(bookconfig.default_header)
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    html = get_code_str(html)
    return html

def down_file(url, path, headers={}, style=2):
    '''下载文件'''
    if style == 1:
        urllib.urlretrieve(url, path)
    elif style == 2:
        f = urllib2.urlopen(url)
        data = f.read()
        with open(path, "wb") as code:  
            code.write(data)
    else:
        raise Exception,"no this style"

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
    return '"message":"成功"' in get_url_content(url, {"Cookie" : jd.cookie})

def del_cover(path):
    '''默认封面处理'''
    im = Image.open(path)
    if im.size[0] > 275 and im.size[0] < 285 and im.size[1] > 275 and im.size[1] < 285:
        dect = (40, 0, 240, 280)
        im = im.crop(dect)
        bookshot.save(im, path)

def crawl_book(bookId):
    '''抓取并解析书的信息'''
    book = Shotbook(bookId)
    url = jd.get_book_url(bookId)
    content = get_url_content(url)
    
    book.bookName = regex_one(jd.namereg, content)
    book.author = regex_one(jd.authorreg, content)
    book.set_id_coverpath() # 由书名和作者名生成nid和封面路径
    catearea = regex_one(jd.cateareareg, content)
    catelist = regex_all(jd.catereg, catearea)
    book.type = catelist[len(catelist) - 1].replace("/", "").replace("、", "")
    book.coverurl = regex_one(jd.coverimgreg, content)
    book.bookSize = int(float(regex_one(jd.sizereg, content)) * 1000)
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
    print "begin down cover: %s" % cover_path
    down_file(book.coverurl, cover_path)
    # 安装默认方法处理封面图片
    del_cover(cover_path)
    
    return book

def insert_book(book):
    '''book数据插入数据库'''
    print "crawl complete, insert db"
    bookorm.insert_book(book)
    bookorm.insert_chapter(book.chapters)

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
            print "begin insert: %s %s %s" % (book.bookName, book.nid, book_id) 
            insert_book(book)
    except Exception:
        exstr = traceback.format_exc()
        print exstr
        book = None
    return book

if __name__ == '__main__':
    for bid in range(30022649,30022659):
        crawl_insert_books(str(bid))
        


