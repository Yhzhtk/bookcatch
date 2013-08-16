# coding=utf-8
'''
Created on 2013-8-16
@author: gudh
'''

import os,zipfile,subprocess,time,traceback

def unzip(src, dest_rep_from, dest_rep_to):
    '''unzip, dest replace from dest_rep_from to dest_rep_to'''
    start = time.clock()
    myzip=zipfile.ZipFile(src)
    filelist=myzip.namelist()
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

def get_jpg_count(path):
    '''get path file count'''
    handle = subprocess.Popen('find %s | grep .jpg | wc -l' % path, stdout=subprocess.PIPE, shell=True)
    res = handle.stdout.read()
    print "path jpg count: %s" % res
    return int(res)

def run_one_time(infile, outfile):
    '''through file get info, zip and write file'''
    file = open(infile, "r")
    lines = file.readlines()
    file.close()
    
    oklines = []
    for i in range(len(lines)):
        line = lines[i]
        if line:
            infos = line.split("\t")
            print infos
            unzip(infos[0], "ebook/%s/" % infos[1], "/ftp/temp/")
            if get_jpg_count("/ftp/temp/") == int(infos[2]):
                print "unzip ok %s" % infos[0]
                oklines.append(lines[i])
                del lines[i]
            else:
                print "unzip fail"
    
    # write outfile ok info
    file = open(outfile, "w")
    file.writelines(oklines)
    file.close()            
    
    # write infile
    file = open(infile, "w")
    file.writelines(lines)
    file.close()
    
def run():
    '''run'''
    try:
        run_one_time("/ftp/upload.txt", "/ftp/download.txt")
    except:
        traceback.print_exc()

run()
