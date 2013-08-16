# coding=utf-8
'''
Created on 2013-7-25
一键完成流程
@author: gudh
'''
import bookrun, bookorm

def new_shot():
    '''抓新书'''
    args = []
    args.append(["http://e.jd.com/products/5272-5287-5507-1-%d.html", 1, 5])
    args.append(["http://e.jd.com/products/5272-5287-5507-1-%d.html", 5, 10])
    for arg in args:
        bookrun.shot_cates(arg)

def old_shot():
    '''补充书'''
    id_seq_file = "d:/id_seq.txt"
    bookrun.shot_no_success(id_seq_file)

def online():
    sql = "select * from shotbook where dohost = 'A1' and chapterok = 1 order by createTime limit 2"
    books = bookorm.select_many(sql, True)
    for book in books:
        if bookrun.move_zip_book(book):
            print "OnLine Ok %s %s" % (book.nid, book.bookName)
        else:
            print "OnLine Fail %s %s" % (book.nid, book.bookName)

if __name__ == '__main__':
    # 抓取新数据
    #new_shot()
    
    # 抓取没有成功的数据
    #old_shot()
    
    online()

