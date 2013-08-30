# coding=utf-8
'''
Created on 2013-8-27
@author: gudh
'''

import Image
import traceback, os, time, sys, stat
import retask

log_file = "run.log"
lock_file = "l.lock"

intxt = "/ftp/upload.txt"
outtxt = "/ftp/download.txt"
destpath = "/data/ebook/"

def zoom_cover(cover_path):
    try:
        img = Image.open(cover_path)
        size = os.path.getsize(cover_path) / 1024
        qua = 70
        if size > 20:
            qua = 5
        elif size > 15:
            qua = 10
        elif size > 10:
            qua = 20
        elif size > 5:
            qua = 30
        img.save(cover_path, 'JPEG', quality = qua)
    except:
        traceback.print_exc()

def deal_cover(path):
    for root, dirs, files in os.walk(path): 
        for f in files:
            if f.endswith(".jpg"):
                fname = os.path.join(root, f)
                print "deal cover %s" % fname
                zoom_cover(fname)

def write_log(log):
    log = time.strftime("%Y-%m-%d %H:%M:%S") + "\t" + log + "\n"
    print log
    file = open(log_file, "a")
    file.write(log)
    file.close()

def run_retask():
    try:
        write_log("==========================")
        if os.path.exists(lock_file):
            write_log("other retask is runing, quit this")
            return
        
        write_log("run retask start")
        open(lock_file, "w").close()
        # run task
        retask.run(intxt, outtxt, destpath)
        write_log("run retask end")
    except Exception, e:
        traceback.print_exc()
        write_log(str(e))
    if os.path.exists(lock_file):
        os.remove(lock_file)

def move_daily():
    '''move log daily'''
    write_log("==========================")
    if os.path.exists(intxt):
        dest = "/ftp/tool/log/upload%s.txt" % time.strftime("%y%m%d%H%M%S")
        write_log("move %s to %s" % (intxt, dest))
        os.rename(intxt, dest)
    if os.path.exists(outtxt):
        dest = "/ftp/tool/log/download%s.txt" % time.strftime("%y%m%d%H%M%S")
        write_log("move %s to %s" % (outtxt, dest))
        os.rename(outtxt, dest)
    open(intxt, "w").close()
    os.chmod(intxt, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
        
if __name__ == '__main__':
    #deal_cover("")
    print sys.argv
    if sys.argv[1] == "run":
        run_retask()
    elif sys.argv[1] == "move":
        move_daily()

