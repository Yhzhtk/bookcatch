# coding=gbk
'''
Created on 2013-7-23
ץȡ��
@author: gudh
'''
import re,os,time,traceback
import urllib,urllib2   
import jd,bookconfig
from bookmode import Shotbook,Chapter
import bookorm

def get_url_content(url, headers={}):
    '''��ָ��UA��ȡ��ҳ����'''
    headers.update(bookconfig.default_header)
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    return html

def down_file(url, path, headers={}, style=2):
    '''�����ļ�'''
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
    '''������ҵ�һ��ƥ�䷵��ָ������'''
    pattern = re.compile(regex, re.DOTALL)
    match = pattern.search(content)
    return match.group(group)

def regex_all(regex, content, group=1):
    '''�����������ƥ�䷵��ָ������'''
    pattern = re.compile(regex, re.DOTALL)
    matchs = pattern.finditer(content)
    return [match.group(group) for match in matchs if match]

def add_book_to_lebook(bookId):
    '''������ӵ��ͻ��ˣ�������Ҫ���ú�jd��cookie'''
    url = jd.get_addbook_url(bookId)
    return '"message":"�ɹ�"' in get_url_content(url, {"Cookie" : jd.cookie})

def crawl_book(bookId):
    '''ץȡ�����������Ϣ'''
    book = Shotbook(bookId)
    url = jd.get_book_url(bookId)
    content = get_url_content(url)
    
    book.bookName = regex_one(jd.namereg, content)
    book.author = regex_one(jd.authorreg, content)
    book.set_id_coverpath() # ������������������nid�ͷ���·��
    catearea = regex_one(jd.cateareareg, content)
    catelist = regex_all(jd.catereg, catearea)
    book.type = catelist[len(catelist) - 1].replace("/", "").replace("��", "")
    book.coverurl = regex_one(jd.coverimgreg, content)
    book.bookSize = int(float(regex_one(jd.sizereg, content)) * 1000)
    desc = regex_one(jd.descreg, content).replace("<br />"," ").replace("��","").replace(" ", "").strip()
    desc = re.sub("<.*?>", "", desc)
    book.description = desc
    chapterarea = regex_one(jd.chaptersreg, content)
    # �����½��еļ�����
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
    # �����½���Ϣ
    book.complete_chapter()
    
    # ���ط���
    cover_path = bookconfig.rootpath + time.strftime("%Y%m%d") + "/cover/" + book.coverImgPath
    # ���·�������ڣ����ȴ���·��
    if not os.path.exists(os.path.split(cover_path)[0]):
        os.makedirs(os.path.split(cover_path)[0])
    print "begin down cover: %s" % cover_path
    down_file(book.coverurl, cover_path)
    
    return book

def insert_book(book):
    '''book���ݲ������ݿ�'''
    print "crawl complete, insert db"
    bookorm.insert_book(book)
    bookorm.insert_chapter(book.chapters)

def crawl_insert_books(book_id):
    '''ץȡָ��ID����Ϣ���������ݿ⣬��������б�'''
    print "-"*10 + "\r\ncrawl id: %s" % book_id
    book = None
    try:
        if bookorm.exist_book(book_id):
            print "%s has exist, continue" % book_id
        else:
            print "begin crawl: %s" % book_id
            book = crawl_book(book_id)
            print "begin insert: %s %s %s" % (book_id, book.nid, book.bookName) 
            insert_book(book)
    except Exception:
        exstr = traceback.format_exc()
        print exstr
        book = None
    return book

if __name__ == '__main__':
    for bid in range(30022649,30022659):
        crawl_insert_books(str(bid))
        


