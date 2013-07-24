# coding=gbk
'''
Created on 2013-7-24
实体类
@author: gudh
'''
import md5

def getmd5(string):
    '''获取字符串的MD5'''
    m = md5.new(string)
    m.digest()
    return m.hexdigest()

class Shotbook():
    '''书类'''
    def __init__(self, jdid=""):
        # 数据库字段
        self.nid = "" #'小说id',
        self.bookName = "" # '小说名称',
        self.author = "" # '小说作者',
        self.coverImgPath = "" #'小说封面图片地址',
        self.description = "" #'小说简介',
        self.type = "" # '小说类型',
        self.chapterList = "" # '章节列表',
        self.chapterCount = 0 # '章节总数',
        self.state = 1 # '小说状态 0，为连载，1为完结'，默认完结
        self.updateTime = "" # '更新时间',
        self.isok = 0 #'是否建到索引中去，0为没有，1为已经建了',
        #非数据库字段
        self.jdid = jdid #京东的ID
        self.coverurl = "" #封面图片Url
        self.chapters = [] #章节列表，包括章节名称和数量
        #需要过滤的字段
        self.filter = ['jdid', "coverurl", "chapters", "filter"]
        
    def setnid(self):
        '''根据书名和作者设置书的ID'''
        key = self.bookName + "#" + self.author
        self.nid = getmd5(key)
    
    def complete_chapter(self):
        '''完善章节信息'''
        self.chapterList = '$-$'.join([c.cid + "#-#" + c.cTitle for c in self.chapters])
        self.chapterCount = len(self.chapters)
    
    def str(self):
        '''打印当前类的信息'''
        for (a, b) in self.__dict__.items():
            if isinstance(b, list):
                print "-"*10
                for l in b:
                    l.str()
                    print "-"*10
            else:
                print ":".join((a,str(b)))

class Chapter():
    '''章节类'''
    def __init__(self, nid = "", cid = "", cTitle = "", bookName = "", author="", imgCount = 0):
        self.nid = nid
        self.cid = cid
        self.cTitle = cTitle
        self.bookName = bookName
        self.author = author
        self.imgCount = imgCount

    def str(self):
        '''打印当前类的信息'''
        for (a, b) in self.__dict__.items():
            print ":".join((a,str(b)))


