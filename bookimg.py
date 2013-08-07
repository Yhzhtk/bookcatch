# coding=utf-8
'''
Created on 2013-8-7
图片章节处理，打包上传等
@author: gudh
'''
import os,zipfile
import Image
import bookorm, bookconfig,bookshot

def unzip(src, dest):
    '''解压zip'''
    myzip=zipfile.ZipFile(src)
    filelist=myzip.namelist()
    for name in filelist:
        filename = os.path.join(dest, name)
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        f_handle = open(filename, "wb")
        f_handle.write(myzip.read(name))
        f_handle.close()
    myzip.close()
 
def zip_file(src, zip_file):
    '''打包一个文件'''
    f = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)
    f.write(src)
    f.close()

def zip_path(src, zip_file):
    '''把整个文件夹内的文件打包 '''
    f = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)
    os.chdir(src)
    for dirpath, dirnames, filenames in os.walk("."):
        dirnames = dirnames # 去掉该死的提示
        for filename in filenames:
            fn = os.path.join(dirpath,filename)
            f.write(fn)
            print "zip: %s" % fn
    f.close()

def get_move_chap_list(root, cid, start, end):
    '''获取将要移动章节的图片信息'''
    try:
        hsrc_path = (root + str(1) + "/") % "h"
        lsrc_path = (root + str(1) + "/") % "l"
        hdest_path = (root + str(cid) + "/") % "h"
        ldest_path = (root + str(cid) + "/") % "l"
        
        # 获取需要移动的文件对
        move_list = []
        for i in range(start, end):
            # 添加大图
            src = hsrc_path + str(i) + ".jpg"
            dest = hdest_path + str(i - start + 1) + ".jpg"
            if not os.path.exists(src):
                src = hsrc_path + str(i) + "_b.jpg"
            if not os.path.exists(src):
                raise Exception, "path: %d is not exist, move_chap error"
                return (False, None)
            move_list.append((src, dest))
            # 添加小图
            src = lsrc_path + str(i) + ".jpg"
            dest = ldest_path + str(i - start + 1) + ".jpg"
            if not os.path.exists(src):
                src = lsrc_path + str(i) + "_b.jpg"
            if not os.path.exists(src):
                raise Exception, "path: %d is not exist, move_chap error"
                return (False, None)
            move_list.append((src, dest))
        
        return (True, move_list)
    except Exception, e:
        print "move chap error: %s" % str(e)
        return (False, None)

def move_book_back(path):
    '''将所有图片移回去'''
    os.chdir(path)
    path1 = path + "1/"
    index = 1
    move_infos = []
    for i in range(1, len(os.listdir(path)) + 1):
        tpath = path + str(i) + "/"
        for j in range(1, len([s for s in os.listdir(tpath) if s.endswith(".jpg")]) + 1):
            f = tpath + str(j) + ".jpg"
            dest = path1 + str(index) + ".jpg"
            if os.path.exists(f):
                f = f
                #if bookshot.is_bold(Image.open(f), bookconfig.blod_para):
                    #dest = tpath + str(index) + "_b.jpg"
            else:
                f = tpath + str(j) + "_b.jpg"
                dest = path1 + str(index) + "_b.jpg"
            index += 1
            move_infos.append((f, dest))

    for m in move_infos:
        os.renames(m[0], m[1])
        print m[0], m[1]
          
def move_book(book):
    '''完善book的章节图片移动处理'''
    try:
        print "=" * 50
        print "begin move book chapter img", book.bookName, book.nid
        chapters = book.chapters
        nid = book.nid
        root_path = bookconfig.rootpath + book.createTime[0:10].replace("-", "")
        root_path = root_path + "/content/%s/" + nid[0:2] + "/" + nid[2:4] + "/" + nid[4:] + "/"
        start = 1
        all_move_list = []
        for chapter in chapters:
            end = start + chapter.imgCount
            res = get_move_chap_list(root_path, chapter.cid, start, end)
            start = end
            if res[0]:
                all_move_list.extend(res[1])
                print "get book %s cid %d chapter img info ok" % (book.nid, chapter.cid)
            else:
                print "get book %s cid %d chapter img info error" % (book.nid, chapter.cid)
                return False
        
        print "begin move, total length: %d" % len(all_move_list)
        for src_dest in all_move_list:
            os.renames(src_dest[0], src_dest[1])
            print "%s to %s" % (src_dest[0], src_dest[1])
        return True
    except Exception, e:
        print "error: %s" % str(e)
        return False

#zip_path(r"F:\ebook\20130807", r"F:\20130807.zip")
#unzip(r"F:\20130807.zip", "F:/xx/")
def complete_books():
    sql = "select * from shotbook where chapterok = 1 and nid = ''"
    books = bookorm.select_many(sql, True)
    for book in books:
        if move_book(book):
            book.chapterok = 2
            book.upTime()
            bookorm.save_book(book)

#complete_books()
move_book_back(r"F:\ebook\20130806\content\l\e1\8a\d7dfdb59aa985687ebe71220f6d5/")
