# coding=gbk
'''
Created on 2013-7-25
һ���������
@author: gudh
'''

import bookcrawl,bookshot

if __name__ == '__main__':
    bookId = "30128501"
    if bookcrawl.add_book_to_lebook(bookId):
        print "add new book ok: " + bookId
        book = bookcrawl.crawl_book(bookId)
        if book != None:
            print "crawl book ok: %s %s %s" % (bookId, book.nid, book.bookName) 
            bookcrawl.insert_book(book)
            print "begin shot book"
            down_time = book.bookSize / 50 # �����ļ���С��������ʱ�䣬ÿ��50k
            bookshot.shot_first_book(book.nid, down_time)
        else:
            print "crawl book fail: %s %s %s" % (bookId, "", "") 
    else:
        print "add new book fail: " + bookId
