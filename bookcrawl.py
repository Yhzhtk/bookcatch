# coding=gbk
'''
Created on 2013-7-23
抓取书
@author: gudh
'''
import re,os,time,traceback
import urllib,urllib2
import jd
from bookmode import Shotbook,Chapter
import bookorm

def get_url_content(url, headers={}):
    '''以指定UA获取网页内容'''
    headers.update({'User-Agent' : 'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.84 Safari/537.22' })
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    return html

def down_file(url, path):
    '''下载文件'''
    urllib.urlretrieve(url, path)

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

def add_book_to_lebook(bookId):
    '''将书添加到客户端，事先需要设置好jd的cookie'''
    url = jd.get_addbook_url(bookId)
    return '"message":"成功"' in get_url_content(url, {"Cookie" : jd.cookie})

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
    desc = regex_one(jd.descreg, content).replace("<br />"," ").replace("　","").replace(" ", "").strip()
    desc = re.sub("<.*?>", "", desc)
    book.description = desc
    chapterarea = regex_one(jd.chaptersreg, content)
    book.chapters = [Chapter(book.nid, str(i), line.strip(), book.bookName, book.author, 0) for (i,line) in enumerate(chapterarea.split("<br />"), 1)]
    book.complete_chapter()
    
    # 下载封面
    cover_path = jd.rootpath + time.strftime("%Y%m%d") + "/cover/" + book.coverImgPath
    # 如果路径不存在，则先创建路径
    if not os.path.exists(os.path.split(cover_path)[0]):
        os.makedirs(os.path.split(cover_path)[0])
    down_file(book.coverurl, cover_path)
    
    return book

def crawl_insert_books(book_ids):
    '''抓取指定ID的信息并插入数据库'''
    for bid in book_ids:
        print "-"*10 + "\r\ncrawl id: %d" % bid
        try:
            if bookorm.exist_book(str(bid)):
                print "%d has exist, continue" % bid
                continue
            book = crawl_book(str(bid))
            print "crawl complete, insert db"
            bookorm.insert_book(book)
            bookorm.insert_chapter(book.chapters)
        except Exception:
            exstr = traceback.format_exc()
            print exstr
        
crawl_insert_books(range(30022649,30022659))

