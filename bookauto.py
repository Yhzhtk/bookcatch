# coding=utf-8
'''
Created on 2013-7-25
一键完成流程
@author: gudh
'''

import bookcrawl,bookshot,bookorm

def get_book_ids(urls=["http://e.jd.com/ebook.html"]):
    idss = []
    for url in urls:
        content = bookcrawl.get_url_content(url)
        ids = bookcrawl.regex_all('''href="http://e.jd.com/(\d{5,10}).html"''', content, 1)
        print ids
        idss.append(ids)
    return ids

if __name__ == '__main__':
    urls = []
    for i in range(1, 5):
        urls.append("http://e.jd.com/products/5272-5287-5507-1-%d.html" % i)
    book_ids = get_book_ids(urls)
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
                    bookshot.shot_first_book(book.nid, down_time=d_t)
                else:
                    print "insert book fail: %s" % book_id
            else:
                print "add book to lebook fail: " + book_id
        else:
            print "crawl book fail: " + book_id
