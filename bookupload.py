# encoding=utf-8
'''
Created on 2013-8-12
使用ftp上传文件,使用Post发送信息
@author: gudh
'''
from ftplib import FTP
import os,re,traceback,httplib,urllib,time
import bookorm

# FTP 参数
default_ftp_host = "43.253.150.171"
ftp_pool = {}
filesize = 0 # 文件大小
rlen = 0 # 记录上传下载的量
bsize = 1024 * 100 # 块大小
bnum = 0 # 块数量

# POST参数
http_con_pool = {} # http连接池
post_host = "122.49.34.20:18111"
book_post_url = "http://%s/ShotBook/addNovel" % post_host
chapter_post_url = "http://%s/ShotBook/addChapter" % post_host

def get_ftp(host, user = "book_ftp", pwd = "3$book@yicha#2013#"):
    '''获取ftp连接，单线程的连接池'''
    if not host:
        host = default_ftp_host
    if ftp_pool.has_key(host):
        return ftp_pool.get(host)
    
    ftp = FTP()
    ftp.connect(host, 21, 30) # 连接FTP服务器
    if not user and not pwd:
        ftp.login()
    else:
        ftp.login(user, pwd[2:-1].replace("#", "_")) # 登录
    # python的默认ftplib启用passive（被动模式），因为被动模式会启用1024之后的端口，所以就会出现问题error: [Errno 10060]
    ftp.set_pasv(False)
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
    global rlen, bnum, filesize
    rlen = 0 # 记录上传下载的量
    bnum = 0 # 块数量
    filesize = os.path.getsize(local_filename)
    def callback(data):
        global rlen, bnum, filesize
        rlen = rlen + len(data)
        if rlen / bsize >= bnum:
            bnum += 1
            print "up size: %d bytes / %d bytes" % (rlen, filesize)
    ftp.storbinary('STOR %s' % name, file_handler, callback=callback)# 上传FTP文件
    file_handler.close()
    ftp.set_debuglevel(0)

def upload_ftp_file(localname, ftp_url):
    '''上传文件至ftp'''
    try:
        start = time.clock()
        host = re.compile("(ftp://.*?)/", re.DOTALL).search(ftp_url)
        if host:
            host = host.group(1)
            host = host[6:]
            name = ftp_url.replace(host, "")
        else:
            name = ftp_url
        print host, name
        upload_file(host, localname, name)
        end = time.clock()
        print u"use time: %d" % (end - start)
        return True
    except:
        traceback.print_exc()
        return False

def upload_update_book(book, zip_file, ftp_url):
    '''上传打包文件到ftp，更新数据库'''
    if upload_ftp_file(zip_file, ftp_url):
        book.chapterok = 3
        book.upTime()
        bookorm.save_book(book)
        return True
    return False

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

def get_http(host_port):
    '''获取http连接，单线程的连接池'''
    host = host_port[0] + ":" + host_port[1]
    if http_con_pool.has_key(host):
        conn = http_con_pool[host]
        print "use conn pool"
        return conn
    
    print "use new conn"
    conn = None
    if len(host_port) == 2:
        conn = httplib.HTTPConnection(host_port[0], host_port[1], timeout=20)
    else:
        conn = httplib.HTTPConnection(host_port[0], timeout=20)
    
    if conn:
        http_con_pool[host] = conn
    return conn

def remove_http(host_port):
    host = host_port[0] + ":" + host_port[1]
    if http_con_pool.has_key(host):
        del http_con_pool[host] 

def close_http():
    if len(http_con_pool) > 0:
        for host in http_con_pool.keys():
            try:
                http_con_pool[host].close()
            except:
                traceback.print_exc()
    http_con_pool = {}

def get_para_dict(obj, filter = None):
    '''获取发送的参数'''
    paras = {}
    if not filter:
        filter = obj.filter
    for (k,v) in obj.__dict__.items():
        if k in filter: # 判断是否是过滤的字段
            continue
        paras[k] = unicode(v).encode("utf-8")
    return paras

def send_data(post_url, para_dict, headers = {"Content-Type" : "application/x-www-form-urlencoded"}):
    '''发送Post数据'''
    try:
        params = urllib.urlencode(para_dict)
        host_port, path = urllib.splithost(post_url.replace("http:", "").replace("https:", ""))
        host_port = host_port.split(":")
        conn = get_http(host_port)
        conn.request("POST", path, params, headers)
        response = conn.getresponse()
        res = False
        rstr = response.read()
        print response.status, rstr
        if rstr == "1":
            res = True
        return res
    except:
        traceback.print_exc()
        remove_http(host_port)
        print "sleep 6 seconds"
        time.sleep(6)
        return False

def send_data_retry(post_url, obj, headers = {}, retry = 3):
    '''带重试发送'''
    para_dict = get_para_dict(obj)
    isbook = True
    if para_dict.has_key("cid"):
        isbook = False
    for i in range(retry):
        if send_data(post_url, para_dict):
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
    print "=" * 50
    chapters = book.chapters
    for chapter in chapters:
        print "-" * 50
        if not send_data_retry(chapter_post_url, chapter):
            print "send chapter fail, return Flase"
            return False
        #time.sleep(0.2)
    print "send all chapter ok", book.nid
    
    if not send_data_retry(book_post_url, book):
        print "send book fail, return Flase", book.nid
        return False
    
    return True

def push_update_book(book):
    '''发送数据信息，并更新数据库'''
    if push_bookinfo(book):
        book.chapterok = 4
        book.upTime()
        bookorm.save_book(book)
        return True
    return False

def upload_upload_file(ftp_url, upload_file):
    '''上传upload.txt文件，获取源文件是否有数据，有的话先拼接'''
    localname = "c:/down/upload%s.txt" % time.strftime("%y%m%d_%H%M%S")
    try:
        print u"开始下载数据"
        if download_ftp_file(ftp_url, localname):
            # 拼接数据
            print u"开始合并数据"
            df = open(localname, "r")
            datas = df.readlines()
            datas = [l for l in datas if l.strip() != ""]
            df.close()
            uf = open(upload_file, "r")
            t_datas = uf.readlines()
            uf.close()
            
            # 合并去重
            datas.extend(t_datas)
            datas = set(datas)
            upfile = open(upload_file, "w")
            for data in datas:
                upfile.write(data)
                print u"行%s" % data 
            upfile.close()
            print u"共有数据条数：%d" % len(datas) 
            
            # 上传upload.txt
            if upload_ftp_file(upload_file, ftp_url):
                print u"上传upload成功"
            else:
                print u"上传失败，请联系管理员"
        else:
            print u"下载书籍失败，请联系管理员"
    except:
        traceback.print_exc()
        print u"上传失败，请联系管理员"

def update_upload_book(ftp_url):
    localname = "c:/down/download%s.txt" % time.strftime("%y%m%d_%H%M%S")
    if download_ftp_file(ftp_url, localname):
        datas = open(localname, "r").readlines()
        for data in datas:
            infos = data.split("\t")
            print "=" * 50, "\n", infos
            if len(infos) == 4:
                nid = os.path.basename(infos[1])[4:-4]
                book = bookorm.get_book(nid)
                if book.chapterok == 2:
                    book.chapterok = 3
                    book.upTime()
                    bookorm.save_book(book)
                    print "ok %s %s for update_upload_book" % (nid, book.bookName)
                else:
                    print "book chapterok is not 2, pass"

if __name__ == '__main__':
#     list_ftp(None, "/")
#     ftp_url = "/ebook/z.jpg"
#     localname = "d:/m.jpg"
#     upload_ftp_file(localname, ftp_url)
#     close_ftp()

    nid = "7738afd367cac04d3d52489a2a3e584e"
    book = bookorm.get_book(nid, True)
    print push_bookinfo(book)
