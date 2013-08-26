#!/usr/bin/env python
# coding=utf-8
'''
Created on 2013-8-16
@author: gudh
'''

import os,zipfile,subprocess,time,traceback,sys

def unzip(src, dest_rep_from, dest_rep_to):
    '''unzip, dest replace from dest_rep_from to dest_rep_to'''
    try:
        start = time.clock()
        myzip = zipfile.ZipFile(src)
        filelist = myzip.namelist()
        for name in filelist:
            filename = name.replace(dest_rep_from, dest_rep_to)
            print filename
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
            f_handle = open(filename, "wb")
            f_handle.write(myzip.read(name))
            f_handle.close()
        myzip.close()
        end = time.clock()
        print start, end, "unzip file %s use time %ds" % (src, (end - start))
    except:
        traceback.print_exc() 

def get_jpg_count(path):
    '''get path file count'''
    handle = subprocess.Popen('find %s | grep .jpg | wc -l' % path, stdout=subprocess.PIPE, shell=True)
    res = handle.stdout.read()
    print "path jpg count: %s" % res
    return int(res)

def get_book_path(destpath, nid):
    '''get book high low cover path'''
    npath = "%s/%s/%s" % (nid[0:2], nid[2:4], nid[4:])
    hpath = "%scontent/%s/%s" % (destpath, "h", npath)
    lpath = "%scontent/%s/%s" % (destpath, "l", npath)
    cpath = "%scover/%s/%s" % (destpath, nid[0:2], nid[2:4])
    all_bookdir = "%s %s %s" % (hpath, lpath, cpath)
    print "GET JPG PATH: %s" % all_bookdir
    return all_bookdir

def write_file(filename, line):
    file = open(filename, "a")
    file.writelines(line)
    file.close()

def run_one_time(infile, outfile, destpath):
    '''through file get info, zip and write file'''
    file = open(infile, "r")
    lines = file.readlines()
    file.close()
    
    oklines = []
    faillines = []
    for i in range(len(lines)):
        line = lines[i]
        if line:
            infos = line.split("\t")
            print infos
            unzip(infos[0], "ebook/%s/" % infos[1], destpath)
            
            # verify unzip jpg count
            nid = os.path.basename(infos[0])[4:-4]
            bookdir = get_book_path(destpath, nid)
            if get_jpg_count(bookdir) == int(infos[2]):
                print "unzip ok %s" % infos[0]
                oklines.append(time.strftime("%Y-%m-%d %H:%M:%S") + "\t" + line)
                write_file(outfile, time.strftime("%Y-%m-%d %H:%M:%S") + "\t" + line)
            else:
                faillines.append(line)
                print "unzip fail"

    # write fail lines
    file = open(infile, "w")
    file.writelines(faillines)
    file.close()
    
def run(intxt, outtxt, destpath):
    '''run'''
    try:
        run_one_time(intxt, outtxt, destpath)
    except:
        traceback.print_exc()

if __name__ == '__main__':
    intxt = "/ftp/upload.txt"
    outtxt = "/ftp/download.txt"
    destpath = "/data/ebook/"
    
    if len(sys.argv) > 1 and sys.argv[1]:
        intxt = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2]:
        outtxt = sys.argv[2]
    if len(sys.argv) > 3 and sys.argv[3]:
        destpath = sys.argv[3]
        if not destpath.endswith("/"):
            destpath = destpath + "/"

    run(intxt, outtxt, destpath)
