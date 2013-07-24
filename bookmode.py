# coding=gbk
'''
Created on 2013-7-24
ʵ����
@author: gudh
'''
import md5

def getmd5(string):
    '''��ȡ�ַ�����MD5'''
    m = md5.new(string)
    m.digest()
    return m.hexdigest()

class Shotbook():
    '''����'''
    def __init__(self, jdid=""):
        # ���ݿ��ֶ�
        self.nid = "" #'С˵id',
        self.bookName = "" # 'С˵����',
        self.author = "" # 'С˵����',
        self.coverImgPath = "" #'С˵����ͼƬ��ַ',
        self.description = "" #'С˵���',
        self.type = "" # 'С˵����',
        self.chapterList = "" # '�½��б�',
        self.chapterCount = 0 # '�½�����',
        self.state = 1 # 'С˵״̬ 0��Ϊ���أ�1Ϊ���'��Ĭ�����
        self.updateTime = "" # '����ʱ��',
        self.isok = 0 #'�Ƿ񽨵�������ȥ��0Ϊû�У�1Ϊ�Ѿ�����',
        #�����ݿ��ֶ�
        self.jdid = jdid #������ID
        self.coverurl = "" #����ͼƬUrl
        self.chapters = [] #�½��б��������½����ƺ�����
        #��Ҫ���˵��ֶ�
        self.filter = ['jdid', "coverurl", "chapters", "filter"]
        
    def setnid(self):
        '''���������������������ID'''
        key = self.bookName + "#" + self.author
        self.nid = getmd5(key)
    
    def complete_chapter(self):
        '''�����½���Ϣ'''
        self.chapterList = '$-$'.join([c.cid + "#-#" + c.cTitle for c in self.chapters])
        self.chapterCount = len(self.chapters)
    
    def str(self):
        '''��ӡ��ǰ�����Ϣ'''
        for (a, b) in self.__dict__.items():
            if isinstance(b, list):
                print "-"*10
                for l in b:
                    l.str()
                    print "-"*10
            else:
                print ":".join((a,str(b)))

class Chapter():
    '''�½���'''
    def __init__(self, nid = "", cid = "", cTitle = "", bookName = "", author="", imgCount = 0):
        self.nid = nid
        self.cid = cid
        self.cTitle = cTitle
        self.bookName = bookName
        self.author = author
        self.imgCount = imgCount

    def str(self):
        '''��ӡ��ǰ�����Ϣ'''
        for (a, b) in self.__dict__.items():
            print ":".join((a,str(b)))

