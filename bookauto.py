# coding=gbk
'''
Created on 2013-7-25
һ���������
@author: gudh
'''

import bookcrawl,bookshot

if __name__ == '__main__':
    book_ids = ["30057405","30069437"]
    for book_id in book_ids:
        print "=" * 50
        print "BEGIN BOOK_ID : %s" % book_id
        if bookcrawl.add_book_to_lebook(book_id):
            print "add new book ok: " + book_id
            book = bookcrawl.crawl_insert_books(book_id)
            if book != None:
                print "begin shot book: %s" % book_id
                d_t = book.bookSize / 50 # �����ļ���С��������ʱ�䣬ÿ��50k
                bookshot.shot_first_book(book.nid, down_time=d_t)
            else:
                print "crawl_insert_books book fail: %s %s %s" % (book_id, "", "") 
        else:
            print "add new book fail: " + book_id
