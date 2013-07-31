# coding=gbk
'''
Created on 2013-7-24
ʵ����
@author: gudh
'''
import md5
import time

def getmd5(string):
    '''��ȡ�ַ�����MD5'''
    m = md5.new(string)
    m.digest()
    return m.hexdigest()

class Shotbook():
    '''����'''
    
    db_field_seq=("nid","jdid","bookName","author","coverImgPath","description","type","chapterList","chapterCount","imgCount","state","createTime","updateTime","chapterok","isok")
    
    def __init__(self, jdid=""):
        # ���ݿ��ֶ�
        self.nid = "" #'С˵id',
        self.jdid = jdid #������ID
        self.bookName = "" # 'С˵����',
        self.author = "" # 'С˵����',
        self.coverImgPath = "" #'С˵����ͼƬ��ַ',
        self.description = "" #'С˵���',
        self.type = "" # 'С˵����',
        self.chapterList = "" # '�½��б�',
        self.chapterCount = 0 # '�½�����',
        self.imgCount = 0 #ͼƬ����
        self.state = 1 # 'С˵״̬ 0��Ϊ���أ�1Ϊ���'��Ĭ�����
        self.createTime = time.strftime("%Y-%m-%d %H:%M:%S") # ����ʱ��
        self.updateTime = time.strftime("%Y-%m-%d %H:%M:%S") # '����ʱ��'
        self.chapterok = 0 # �����Ƿ���ɣ�0û�У�1���
        self.isok = 0 #'�Ƿ񽨵�������ȥ��0Ϊû�У�1Ϊ�Ѿ�����',
        #�����ݿ��ֶ�
        self.coverurl = "" #����ͼƬUrl
        self.chapters = [] #�½��б������½����ƺ�����
        self.bookSize = 500
        #��Ҫ���˵��ֶ�
        self.filter = ["coverurl", "chapters", "bookSize", "filter"]
        
    def set_id_coverpath(self):
        '''���������������������ID'''
        key = self.bookName + "#" + self.author
        md5 = getmd5(key)
        self.nid = md5
        coverpath = md5[0:2] + "/" + md5[2:4] + "/" + md5[4:] + ".jpg"
        self.coverImgPath = coverpath
    
    def complete_chapter(self):
        '''�����½���Ϣ'''
        self.chapterList = '$-$'.join([c.cid + "#-#" + c.cTitle for c in self.chapters])
        self.chapterCount = len(self.chapters)
    
    def upTime(self):
        '''����ʱ��'''
        self.updateTime = time.strftime("%Y-%m-%d %H:%M:%S") # '����ʱ��',
    
    def str(self):
        '''��ӡ��ǰ�����Ϣ'''
        for (a, b) in self.__dict__.items():
            if isinstance(b, list):
                print "-"*10
                for l in b:
                    if isinstance(l, Chapter):
                        l.str()
                        print "-"*10
                    else:
                        print l
            else:
                print ":".join((a,str(b)))

class Chapter():
    '''�½���'''
    db_field_seq=("nid","cid","cTitle","bookName","author","imgCount")
    
    def __init__(self, nid = "", cid = "", cTitle = "", bookName = "", author="", imgCount = 0):
        self.nid = nid
        self.cid = cid
        self.cTitle = cTitle
        self.bookName = bookName
        self.author = author
        self.imgCount = imgCount
        #��Ҫ���˵��ֶ�
        self.filter = ["filter"]

    def str(self):
        '''��ӡ��ǰ�����Ϣ'''
        for (a, b) in self.__dict__.items():
            print ":".join((a,str(b)))

