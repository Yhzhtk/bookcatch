# coding=utf-8
'''
Created on 2013-8-30
拍书，新书或者已添加的书
@author: gudh
'''

import bookauto

if __name__ == '__main__':
    # 抓取新数据
    #args = []
    #args.append(["http://e.jd.com/products/5272-5287-5507-1-%d.html", 1, 5])
    #args.append(["http://e.jd.com/products/5272-5287-5507-1-%d.html", 5, 10])
    #bookauto.new_shot(args)
    
    # 抓取没有成功的数据
    id_seq_file = "d:/id_seq_file.txt"
    bookauto.old_shot(id_seq_file)
    