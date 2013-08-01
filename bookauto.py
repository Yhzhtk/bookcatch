# coding=utf-8
'''
Created on 2013-7-25
一键完成流程
@author: gudh
'''

import bookcrawl,bookshot

def get_book_ids(url="http://e.jd.com/ebook.html"):
    content = bookcrawl.get_url_content(url)
    ids = bookcrawl.regex_all('''href="http://e.jd.com/(\d{5,10}).html"''', content, 1)
    print ids
    return ids

if __name__ == '__main__':
    book_ids = get_book_ids()
    for book_id in book_ids:
        print "=" * 50
        print "BEGIN BOOK_ID : %s" % book_id
        if bookcrawl.add_book_to_lebook(book_id):
            print "add new book ok: " + book_id
            book = bookcrawl.crawl_insert_books(book_id)
            if book != None:
                print "begin shot book: %s" % book_id
                d_t = book.bookSize / 50 # 根据文件大小计算下载时间，每秒50k
                bookshot.shot_first_book(book.nid, down_time=d_t)
            else:
                print "crawl_insert_books book fail: %s %s %s" % (book_id, "", "") 
        else:
            print "add new book fail: " + book_id
