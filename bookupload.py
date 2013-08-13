# encoding=utf-8
'''
Created on 2013-8-12
使用ftp上传文件
@author: gudh
'''
from ftplib import FTP
import os,re,traceback,httplib,urllib
import bookorm,bookmode

# FTP 参数
default_ftp_host = "ftp.bupt.edu.cn"
ftp_pool = {}
filesize = 0 # 文件大小
rlen = 0 # 记录上传下载的量
bsize = 1024 * 100 # 块大小
bnum = 0 # 块数量

# POST参数
book_post_url = "http://192.168.1.76:8080/NovelManager/addNovel"
chapter_post_url = "http://192.168.1.76:8080/NovelManager/AddChapter"


def get_ftp(host, user = "", pwd = ""):
    '''获取ftp连接'''
    if not host:
        host = default_ftp_host
    if ftp_pool.has_key(host):
        return ftp_pool.get(host)
    
    ftp = FTP()
    ftp.connect(host, 21, 30) # 连接FTP服务器
    if not user and not pwd:
        ftp.login()
    else:
        ftp.login(user, pwd) # 登录
    wel = ftp.getwelcome() # 获得欢迎信息 
    print "ftp welcome:", wel
    if wel.startswith("220"):
        ftp_pool[host] = ftp
        return ftp
    else:
        return None

def close_ftp():
    if len(ftp_pool) > 0:
        for host in ftp_pool.keys():
            ftp_pool[host].quit() # 退出FTP服务器

def list_ftp(host, path):
    '''在指定host列出路径所有文件'''
    ftp = get_ftp(host)
    ftp.cwd(path) # 设置FTP路径
    for name in ftp.nlst() :
        print ftp.retrlines('LIST %s' % name)

def upload_file(host, local_filename, ftp_filename):
    '''在指定host上传文件'''
    ftp = get_ftp(host)
    ftp.set_debuglevel(2) # 打开调试级别2，显示详细信息; 0为关闭调试信息 
    file_handler = open(local_filename, 'rb')
    ftp.cwd(os.path.dirname(ftp_filename))
    name = os.path.basename(ftp_filename)
    rlen = 0 # 记录上传下载的量
    bnum = 0 # 块数量
    filesize = os.path.getsize(local_filename)
    def callback(data):
        global rlen, bnum, filesize
        file_handler.write(data)
        rlen = rlen + len(data)
        if rlen / bsize >= bnum:
            bnum += 1
            print "up size: %d bytes / %d bytes" % rlen, filesize
    ftp.storbinary('STOR %s' % name, file_handler, callback=callback)# 上传FTP文件
    file_handler.close()
    ftp.set_debuglevel(0)

def download_file(host, ftp_filename, local_filename):
    '''在指定host下载文件'''
    ftp = get_ftp(host)
    ftp.set_debuglevel(2) # 打开调试级别2，显示详细信息; 0为关闭调试信息 
    ftp.cwd(os.path.dirname(ftp_filename))
    name = os.path.basename(ftp_filename)
    file_handler = open(local_filename, 'wb') #以写模式在本地打开文件
    global rlen, bnum, filesize
    rlen = 0 # 记录上传下载的量
    bnum = 0 # 块数量
    filesize = ftp.size(ftp_filename)
    def callback(data):
        global rlen, bnum, filesize
        file_handler.write(data)
        rlen = rlen + len(data)
        if rlen / bsize >= bnum:
            bnum += 1
            print "down size: %d bytes / %d bytes" % (rlen, filesize)
    ftp.retrbinary('RETR %s' % name, callback=callback) # 下载FTP上的文件
    file_handler.close()
    ftp.set_debuglevel(0)

def download_ftp_file(ftp_url, localname):
    '''下载ftp到文件'''
    try:
        host = re.compile("(ftp://.*?)/", re.DOTALL).search(ftp_url)
        if host:
            host = host.group(1)
            host = host[6:]
            name = ftp_url.replace(host, "")
        else:
            name = ftp_url
        print host, name
        download_file(host, name, localname)
        return True
    except:
        traceback.print_exc()
        return False

def upload_ftp_file(localname, ftp_url):
    '''上传文件至ftp'''
    try:
        host = re.compile("(ftp://.*?)/", re.DOTALL).search(ftp_url)
        if host:
            host = host.group(1)
            host = host[6:]
            name = ftp_url.replace(host, "")
        else:
            name = ftp_url
        print host, name
        upload_file(host, localname, name)
        return True
    except:
        traceback.print_exc()
        return False

def get_para_dict(obj, filter = None):
    '''获取发送的参数'''
    paras = {}
    if not filter:
        filter = obj.filter
    for (k,v) in obj.__dict__.items():
        if k in filter: # 判断是否是过滤的字段
            continue
        paras[k] = v
    return paras

def send_data(post_url, para_dict, headers = {"Content-Type" : "application/x-www-form-urlencoded"}):
    '''发送Post数据'''
    try:
        params = urllib.urlencode(para_dict)
        host_port, path = urllib.splithost(post_url.replace("http:", "").replace("https:", ""))
        host_port = host_port.split(":")
        if len(host_port) == 2:
            conn = httplib.HTTPConnection(host_port[0], host_port[1])
        else:
            conn = httplib.HTTPConnection(host_port[0])
        conn._send_request("POST", path, params, headers)
        response = conn.getresponse()
        print response.status
        res = False
        rstr = response.read()
        print rstr
        if rstr == "1":
            res = True
        conn.close()
        return res
    except:
        traceback.print_exc()
        return False

def send_data_retry(post_url, obj, headers = {}, retry = 3):
    '''带重试发送'''
    para_dict = get_para_dict(obj)
    isbook = True
    if para_dict.has_key("cid"):
        isbook = False
    for i in range(retry):
        if send_data(chapter_post_url, para_dict):
            if isbook:
                print "send book ok", obj.nid
            else:
                print "send chapter ok", obj.nid, obj.cid
            return True
        else:
            if isbook:
                print "send book fail", obj.nid, "retry", i
            else:
                print "send chapter fail", obj.nid, obj.cid, "retry", i
    return False

def push_bookinfo(book):
    '''发送书籍信息'''
    chapters = book.chapters
    for chapter in chapters:
        if not send_data_retry(chapter_post_url, chapter):
            print "send chapter fail, return Flase"
            return False
    print "send all chapter ok", book.nid
    
    if not send_data_retry(book_post_url, book):
        print "send book fail, return Flase", book.nid
        return False
    
    return True

if __name__ == '__main__':
#    list_ftp(None, "/pub/mirror/CPAN/")
#     ftp_url = "/pub/Linux_Movie/Revolution_OS_With_gbSUB/ZZ.jpg"
#     localname = "d:/m.jpg"
#     upload_ftp_file(localname, ftp_url)
#     close_ftp()
#     nid = "7738afd367cac04d3d52489a2a3e584e"
#     book = bookorm.get_book(nid, True)
#     print push_bookinfo(book)
    url = "http://passport.yicha.cn/user/login.do?op=login"
    para = {"username":"apple@163.com", "password":"mail."}
    send_data(url, para)

    