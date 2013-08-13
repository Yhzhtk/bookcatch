# encoding=utf-8
'''
Created on 2013-8-12
使用ftp上传文件
@author: gudh
'''
from ftplib import FTP
import os,re

default_host = "ftp.bupt.edu.cn"
ftp_pool = {}

filesize = 0 # 文件大小
rlen = 0 # 记录上传下载的量
bsize = 1024 * 100 # 块大小
bnum = 0 # 块数量

def get_ftp(host, user = "", pwd = ""):
    '''获取ftp连接'''
    if not host:
        host = default_host
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
    host = re.compile("(ftp://.*?)/", re.DOTALL).search(ftp_url)
    if host:
        host = host.group(1)
        host = host[6:]
        name = ftp_url.replace(host, "")
    else:
        name = ftp_url
    print host, name
    download_file(host, name, localname)

def upload_ftp_file(localname, ftp_url):
    '''上传文件至ftp'''
    host = re.compile("(ftp://.*?)/", re.DOTALL).search(ftp_url)
    if host:
        host = host.group(1)
        host = host[6:]
        name = ftp_url.replace(host, "")
    else:
        name = ftp_url
    print host, name
    upload_file(host, localname, name)

if __name__ == '__main__':
    #list_ftp(None, "/pub/mirror/CPAN/")
    ftp_url = "/pub/Linux_Movie/Revolution_OS_With_gbSUB/ZZ.jpg"
    localname = "d:/m.jpg"
    upload_ftp_file(localname, ftp_url)
    close_ftp()
