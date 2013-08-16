# coding=utf-8
'''
Created on 2013-8-15
流程协调
@author: gudh
'''

import traceback,os
import bookcrawl,bookshot,bookorm,bookconfig,bookimg,bookupload

def get_book_ids(urls=["http://e.jd.com/ebook.html"]):
    '''获取一个页面内的所有id'''
    idss = []
    for url in urls:
        content = bookcrawl.get_url_content(url)
        ids = bookcrawl.regex_all('''href="http://e.jd.com/(\d{5,10}).html"''', content, 1)
        print ids
        idss.extend(ids)
    return set(idss)

def shot_cates(args):
    '''抓取一个分类里面指定页数内的所有书籍'''
    urls = []
    # 获取所有id
    for i in range(args[1], args[2]):
        urls.append(args[0] % i)
    book_ids = get_book_ids(urls)
    err_num = 0
    # 循环拍书
    for book_id in book_ids:
        print "=" * 50
        # 如果存在则跳过
        if bookorm.exist_book(book_id):
            print "%s has exist, continue" % book_id
            continue
        # 开始抓取
        print "begin crawl : %s" % book_id
        book = bookcrawl.crawl_book(book_id)
        if book != None:
            print book.bookName
            if bookcrawl.add_book_to_lebook(book_id):
                print "add book to lebook ok: " + book_id
                if bookorm.insert_book_chapter(book):
                    print "insert book ok: %s" % book_id
                    d_t = book.bookSize / 50 # 根据文件大小计算下载时间，每秒50k
                    if d_t < 15:
                        d_t = 15
                    if not bookshot.shot_first_book(book, down_time=d_t):
                        err_num += 1
                        if err_num >= 5:
                            print "连续失败书过多，结束拍书"
                            return
                else:
                    print "insert book fail: %s" % book_id
            else:
                print "add book to lebook fail: " + book_id
        else:
            print "crawl book fail: " + book_id
            
def shot_no_success(id_seq_file):
    '''抓取已经添加但没成功的书籍'''
    lines = open(id_seq_file, "r").read().split("\n")
    infos = [line.split("\t") for line in lines if line]
    for info in infos:
        try:
            mode = bookorm.get_book(info[0])
            loc = int(info[1])
            print "=" * 50
            print mode.bookName
            print "shot point book nid: " + mode.nid + " loc:" + str(loc)
            bookshot.shot_point_book(mode, loc)
        except Exception, e:
            traceback.print_exc()
            print e

def complete(id_seq_file):
    '''数据库删除的数据补充，临时用'''
    lines = open(id_seq_file, "r").read().split("\n")
    infos = [line.split("\t") for line in lines if line]
    for info in infos:
        book_id = info[3][:-1]
        book = bookcrawl.crawl_book(book_id)
        print book.bookName
        book.createTime = "2013-08-10 00:00:00"
        nid = book.nid
        path = bookconfig.rootpath + "20130810/content/l/" + nid[0:2] + "/" + nid[2:4] + "/" + nid[4:] + "/1/"
        ll = [p for p in os.listdir(path) if p.endswith(".jpg")]
        print "get imgCount", len(ll)
        book.imgCount = int(len(ll))
        book.upTime()
        bookorm.insert_book_chapter(book)

def move_zip_book(book):
    '''上线书籍'''
    print "=" * 50
    print u"%s %s" % (book.nid, book.bookName)
    print u"1、开始分章移动更新"
    if bookimg.move_update_book(book):
        print u"分章移动更新更新成功"
        zip_file = "nid_%s.zip" % book.nid
        print u"2、开始打包zip： %s" % zip_file
        if bookimg.zip_book(book, zip_file):
            print u"打包书籍成功"
            line = "/ftp/ebook_zip/%s\t%s\t%d\n" % (zip_file, book.createTime[0:10].replace("-", ""), (2 * book.imgCount + 1))
            file = open(bookconfig.uploadfile, "a")
            file.write(line)
            file.close()
            return True
        else:
            print u"打包书籍失败"
    else:
        print "分章移动更新失败"
    return False

def upload_ftp_book(book):
    '''上传到ftp'''
    zip_file = bookconfig.rootpath + book.createTime[0:10].replace("-", "") + ("nid_%s.zip" % book.nid)
    ftp_url = "/ebook_zip/%s" % zip_file
    print u"3、开始上传到ftp: %s" % ftp_url
    if bookupload.upload_update_book(book, zip_file, ftp_url):
        print u"上传ftp成功"
        print u"3、开始发送书籍信息: %s" % ftp_url
        if bookupload.push_update_book(book):
            print u"发送书籍信息成功"
            return True
        else:
            print u"发送数据信息失败"
    else:
        print u"上传ftp失败"
    return False