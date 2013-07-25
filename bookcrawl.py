# coding=gbk
'''
Created on 2013-7-23
ץȡ��
@author: gudh
'''
import re
import urllib2
import jd
from bookmode import Shotbook,Chapter
import bookorm

def crawl_book(book_ids):
    for bid in book_ids:
        print "crawl book_id:%d" % bid
        book = crawlbook(str(bid))
        bookorm.insert_book(book)
        bookorm.insert_chapter(book.chapters)
        
crawl_book(range(23001,23002))

def geturlcontent(url, headers={}):
    '''��ָ��UA��ȡ��ҳ����'''
    headers.update({'User-Agent' : 'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.84 Safari/537.22' })
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    return html

def regexone(regex, content, group=1):
    '''������ҵ�һ��ƥ�䷵��ָ������'''
    pattern = re.compile(regex, re.DOTALL)
    match = pattern.search(content)
    return match.group(group)

def regexall(regex, content, group=1):
    '''�����������ƥ�䷵��ָ������'''
    pattern = re.compile(regex, re.DOTALL)
    matchs = pattern.finditer(content)
    return [match.group(group) for match in matchs if match]

def addbook(bookId):
    '''������ӵ��ͻ��ˣ�������Ҫ���ú�jd��cookie'''
    url = jd.getaddbookurl(bookId)
    return '"message":"�ɹ�"' in geturlcontent(url, {"Cookie" : jd.cookie})

def crawlbook(bookId):
    '''ץȡ�����������Ϣ'''
    book = Shotbook(bookId)
    url = jd.getbookurl(bookId)
    content = geturlcontent(url)
    
    book.bookName = regexone(jd.namereg, content)
    book.author = regexone(jd.authorreg, content)
    book.set_id_coverpath() # ������������������nid�ͷ���·��
    catearea = regexone(jd.cateareareg, content)
    catelist = regexall(jd.catereg, catearea)
    book.type = catelist[len(catelist) - 1].replace("/", "").replace("��", "")
    book.coverurl = regexone(jd.coverimgreg, content)
    desc = regexone(jd.descreg, content).replace("<br />"," ").replace("��","").replace(" ", "").strip()
    desc = re.sub("<.*?>", "", desc)
    book.description = desc
    chapterarea = regexone(jd.chaptersreg, content)
    book.chapters = [Chapter(book.nid, str(i), line.strip(), book.bookName, book.author, 0) for (i,line) in enumerate(chapterarea.split("<br />"), 1)]
    book.complete_chapter()
    
    return book

