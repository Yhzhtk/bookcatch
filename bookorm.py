# coding=gbk
'''
Created on 2013-7-24
数据库操作类
@author: gudh
'''

import MySQLdb

# 数据库连接参数
host="localhost"
port=3306
user="root"
passwd="314"
charset="utf8"

# 详细数据库信息
db_name = "ebook"
book_table_name = "shotbook"
chapter_table_name = "chapter"

def insert_book(book):
    '''插入一本书的信息到数据库'''
    try:
        conn = get_conn()
        cur = conn.cursor()
        # 获取插入参数
        sp = get_insert_sql_and_paras(book_table_name, book, book.filter)
        
        conn.select_db(db_name)
        cur.execute(sp[0],sp[1])
        
        conn.commit()
        cur.close()
        conn.close()
        
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        
def insert_chapter(chapters):
    '''插入一本书的所有章节信息到数据库'''
    if len(chapters) == 0:
        return
    try:
        conn = get_conn()
        cur = conn.cursor()
        conn.select_db(db_name)
        
        # 获取插入语句
        sql = get_insert_sql(chapter_table_name, chapters[0], chapters[0].filter)
        
        for chapter in chapters:
            # 循环插入数据
            paras = get_insert_paras(chapter, chapter.filter)
            cur.execute(sql, paras)
        
        conn.commit()
        cur.close()
        conn.close()
        
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def exist_book(book_id):
    try:
        conn = get_conn()
        cur = conn.cursor()
        conn.select_db(db_name)
        # 判断Nid是否存在
        sql = "select count(*) from " + book_table_name + " where jdid = %s" 
        cur.execute(sql, book_id)
        result = cur.fetchone()
        
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return result[0] != 0

def select():
    '''查询数据库'''
    try:
        conn=MySQLdb.Connect(host='localhost',user='root',passwd='314',port=3306,charset='utf8')
        cur=conn.cursor()
        conn.select_db('python')
        cur.execute('update test set info="' + '去'.encode("utf8") + '" where id=3')
        count=cur.execute('select * from test')
        print 'there has %s rows record' % count

        result=cur.fetchone()
        print result
        print 'ID: %s info %s' % result

        results=cur.fetchmany(5)
        for r in results:
            print r

        print '=='*10
        cur.scroll(0,mode='absolute')

        results=cur.fetchall()
        for r in results:
            print r[1]

        conn.commit()
        cur.close()
        conn.close()

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


def get_conn():
    '''返回数据库连接，可以在此实现连接池'''
    return MySQLdb.Connect(host=host,user=user,passwd=passwd,port=port,charset=charset)

def get_insert_paras(obj, filter=[]):
    '''获取指定对象的插入参数'''
    paras = []
    for (k,v) in obj.__dict__.items():
        if k in filter: # 判断是否是过滤的字段
            continue
        if type(v) is int:
            paras.append(v)
        else:
            paras.append(str(v).encode(charset))
    # 返回参数
    return paras

def get_insert_sql(table_name, obj, filter=[]):
    '''获取指定对象的sql插入语句'''
    sql = "insert into " + table_name + "(%s) values (%s)"
    sql_part1 = ""
    sql_part2 = ""
    for (k,v) in obj.__dict__.items():
        if k in filter: # 判断是否是过滤的字段
            continue
        sql_part1 += k + ","
        
        # The format string is not really a normal Python format string. You must always use %s for all fields.
        # 这个问题困扰了好久，原来这个转换和Python的转换不一样，所有都要用%s，不用%d
        if type(v) is int:
            sql_part2 += "%s," # 如果是int则使用 %d
        else:
            sql_part2 += "%s," # 否则都当成是字符串
            
    # 去除最后的逗号
    if len(sql_part1) > 1:
        sql_part1 = sql_part1[:-1]
        sql_part2 = sql_part2[:-1]
    # 得到最后的sql语句
    sql = sql % (sql_part1,sql_part2)
    
    # 返回sql和参数
    return sql

def get_insert_sql_and_paras(table_name, obj, filter=[]):
    '''获取指定对象的sql插入语句和参数'''
    sql = "insert into " + table_name + "(%s) values (%s)"
    sql_part1 = ""
    sql_part2 = ""
    paras = []
    for (k,v) in obj.__dict__.items():
        if k in filter: # 判断是否是过滤的字段
            continue
        sql_part1 += k + ","
        
        # The format string is not really a normal Python format string. You must always use %s for all fields.
        # 这个问题困扰了好久，原来这个转换和Python的转换不一样，所有都要用%s，不用%d
        if type(v) is int:
            sql_part2 += "%s," # 如果是int则使用 %d
            paras.append(v)
        else:
            sql_part2 += "%s," # 否则都当成是字符串
            paras.append(str(v).encode(charset))
            
    # 去除最后的逗号
    if len(sql_part1) > 1:
        sql_part1 = sql_part1[:-1]
        sql_part2 = sql_part2[:-1]
    # 得到最后的sql语句
    sql = sql % (sql_part1,sql_part2)
    
    # 返回sql和参数
    return (sql, paras)
