# coding=utf-8
'''
Created on 2013-7-25
一键完成流程
@author: gudh
'''
import bookrun, bookorm, bookupload, bookshot
import os

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

def move_zip():
    '''移动章节打包'''
    sql = "select * from shotbook where dohost = 'A1' and chapterok = 1 order by createTime limit 2"
    books = bookorm.select_many(sql, True)
    for book in books:
        if bookrun.move_zip_book(book):
            print "OnLine Ok %s %s" % (book.nid, book.bookName)
        else:
            print "OnLine Fail %s %s" % (book.nid, book.bookName)

def get_upload_back():
    '''获取上传解压信息反馈，并更新数据库'''
    ftp_url = "download.txt"
    print "begin update upload book"
    bookupload.update_upload_book(ftp_url)
    print "update upload end"

def post_data():
    '''发送书籍信息'''
    sql = "select * from shotbook where dohost = 'A1' and chapterok = 3 order by createTime"
    books = bookorm.select_many(sql, True)
    for book in books:
        if bookupload.push_update_book(book):
            print "PostInfo Ok %s %s" % (book.nid, book.bookName)
        else:
            print "PostInfo Fail %s %s" % (book.nid, book.bookName)

def deal_cover():
    path = "d:/img"
    for root, dirs, files in os.walk(path): 
        for f in files:
            if f.endswith(".jpg"):
                fname = os.path.join(root, f)
                print "deal cover %s" % fname
                bookshot.zoom_cover(fname)

if __name__ == '__main__':
    # 抓取新数据
    #new_shot()
    
    # 抓取没有成功的数据
    old_shot()
    
    # 打包
    #move_zip()
    
    # 获取上传解压信息反馈
    # get_upload_back()
    
    # 发送书籍信息
    # post_data()
    
    # 处理封面
    # deal_cover()
