# coding=utf-8
'''
Created on 2013-7-24
数据库操作类
@author: gudh
'''

import MySQLdb
import bookconfig
from bookmode import Shotbook,Chapter

# 连接池
con_pool = []

def insert_book(book):
    '''插入一本书的信息到数据库'''
    try:
        conn = get_conn()
        cur = conn.cursor()
        # 获取插入参数
        sp = get_insert_sql_and_paras(bookconfig.book_table_name, book, book.filter)
        
        conn.select_db(bookconfig.db_name)
        print sp[0]
        cur.execute(sp[0],sp[1])
        
        conn.commit()
        cur.close()
        re_conn(conn)
        
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        
def insert_chapter(chapters):
    '''插入一本书的所有章节信息到数据库'''
    if len(chapters) == 0:
        return
    try:
        conn = get_conn()
        cur = conn.cursor()
        conn.select_db(bookconfig.db_name)
        
        # 获取插入语句
        sql = get_insert_sql(bookconfig.chapter_table_name, chapters[0], chapters[0].filter)
        print sql
        
        for chapter in chapters:
            # 循环插入数据
            paras = get_insert_paras(chapter, chapter.filter)
            cur.execute(sql, paras)
        
        conn.commit()
        cur.close()
        re_conn(conn)
        
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False

def insert_book_chapter(book):
    '''插入一本书包括章节的信息到数据库'''
    try:
        conn = get_conn()
        cur = conn.cursor()
        # 获取插入参数
        sp = get_insert_sql_and_paras(bookconfig.book_table_name, book, book.filter)
        
        conn.select_db(bookconfig.db_name)
        print sp[0]
        cur.execute(sp[0],sp[1])
        
        chapters = book.chapters
        # 获取插入语句
        sql = get_insert_sql(bookconfig.chapter_table_name, chapters[0], chapters[0].filter)
        print sql
        
        for chapter in chapters:
            # 循环插入数据
            paras = get_insert_paras(chapter, chapter.filter)
            cur.execute(sql, paras)

        conn.commit()
        cur.close()
        re_conn(conn)
        
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False

def delete_book(nid, del_chap=False):
    '''删除书'''
    try:
        conn = get_conn()
        cur = conn.cursor()
        conn.select_db(bookconfig.db_name)
       
        sql = "delete from %s where nid = '%s'" % (bookconfig.book_table_name, nid)
        print sql
        cur.execute(sql)
        
        if del_chap:
            # 删除章节
            sql = "delete from %s where nid = '%s'" % (bookconfig.chapter_table_name, nid)
            cur.execute(sql)
            
        conn.commit()
        cur.close()
        re_conn(conn)
        
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return False

def delete_chapter(nid):
    '''删除章节'''
    try:
        conn = get_conn()
        cur = conn.cursor()
        conn.select_db(bookconfig.db_name)
       
        sql = "delete from %s where nid = '%s'" % (bookconfig.chapter_table_name, nid)
        print sql
        cur.execute(sql)
            
        conn.commit()
        cur.close()
        re_conn(conn)
        
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return False

def save_book(book):
    '''先删除，再插入书籍'''
    try:
        conn = get_conn()
        cur = conn.cursor()
        conn.select_db(bookconfig.db_name)
       
        sql = "delete from %s where nid = '%s'" % (bookconfig.book_table_name, book.nid)
        print sql
        cur.execute(sql)
        
        # 获取插入参数
        sp = get_insert_sql_and_paras(bookconfig.book_table_name, book, book.filter)
        print sp[0]
        cur.execute(sp[0],sp[1])
        
        conn.commit()
        cur.close()
        re_conn(conn)
        
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return False

def save_chapters(nid, chapters):
    '''先删除，再插入章节'''
    try:
        conn = get_conn()
        cur = conn.cursor()
        conn.select_db(bookconfig.db_name)
       
        sql = "delete from %s where nid = '%s'" % (bookconfig.chapter_table_name, nid)
        print sql
        cur.execute(sql)
        
        # 获取插入语句
        sql = get_insert_sql(bookconfig.chapter_table_name, chapters[0], chapters[0].filter)
        print sql
        
        for chapter in chapters:
            # 循环插入数据
            paras = get_insert_paras(chapter, chapter.filter)
            cur.execute(sql, paras)
        
        conn.commit()
        cur.close()
        re_conn(conn)
        
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return False

def exist_book(book_id):
    try:
        conn = get_conn()
        cur = conn.cursor()
        conn.select_db(bookconfig.db_name)
        # 判断Nid是否存在
        sql = "select count(*) from " + bookconfig.book_table_name + " where jdid = %s" 
        cur.execute(sql, book_id)
        result = cur.fetchone()
        
        conn.commit()
        cur.close()
        re_conn(conn)
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return result[0] != 0

def select_one(sql, get_chap=False):
    '''查询数据库'''
    try:
        conn = get_conn()
        cur = conn.cursor()
        conn.select_db(bookconfig.db_name)
        count = cur.execute(sql)
        print '%s # count: %d' % (sql,count)
        result = cur.fetchone()
        conn.commit()
        cur.close()
        re_conn(conn)
        
        return get_mode_from_result(result, get_chap)
    
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def select_many(sql, get_chap=False, start = 0, count = -1):
    '''查询数据库, count=-1表示有多少取多少，为正数则为取的个数'''
    try:
        conn = get_conn()
        cur = conn.cursor()
        conn.select_db(bookconfig.db_name)
        co = cur.execute(sql)
        print '%s # count: %d' % (sql,co)

        if start > 0:
            cur.scroll(0,mode='absolute')
            
        if count == -1:
            results=cur.fetchall()
        elif count > 0:
            results=cur.fetchmany(count)
        else:
            raise Exception,"count need -1 or > 0"
        
        modes = []
        for r in results:
            modes.append(get_mode_from_result(r, get_chap))

        conn.commit()
        cur.close()
        re_conn(conn)
        
        return modes
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def get_book(nid, get_chap=False):
    '''根据nid获取一本书'''
    sql = "select * from %s where nid= '%s'" % (bookconfig.book_table_name, nid)
    return select_one(sql, get_chap)

def get_all_book(get_chap=False):
    '''以配置文件sql获取所有书籍'''
    sql = bookconfig.all_sql
    return select_many(sql, get_chap)

def get_chapter(nid):
    '''根据nid获取一本书的所有章节'''
    sql = "select * from %s where nid= '%s'" % (bookconfig.chapter_table_name, nid)
    return select_many(sql, False)

def get_conn():
    '''返回数据库连接，可以在此实现连接池'''
    tcon = None
    
    for (con, use) in con_pool:
        if not use:
            tcon = con
            break
    
    if not tcon:
        tcon = MySQLdb.Connect(host=bookconfig.host,
                           user=bookconfig.user,
                           passwd=bookconfig.passwd,
                           port=bookconfig.port,
                           charset=bookconfig.charset)
        tcon.autocommit(False)
        con_pool.append([tcon, True])
    return tcon

def re_conn(conn):
    '''释放连接放入连接池'''
    i = 0
    for [con, use] in con_pool:
        use = use # 去掉该死的提示
        if conn == con:
            con_pool[i][1] = False
            return 
        i += 1

def get_mode_from_result(result, get_chap):
    '''从数据库查出来放如mode'''
    mode = None
    if not result:
        return mode
    if len(result) == 16:
        mode = Shotbook()
        # 利用反射赋值
        for (i,m) in enumerate(Shotbook.db_field_seq):
            setattr(mode, m, result[i])
        # 如果是书的信息默认获取所有章节
        if get_chap:
            sql = "select * from " + bookconfig.chapter_table_name + " where nid='%s'" % mode.nid
            mode.chapters = select_many(sql)
    elif len(result) == 6:
        mode = Chapter()
        for (i,m) in enumerate(Chapter.db_field_seq):
            setattr(mode, m, result[i])
    return mode

def get_insert_paras(obj, filter=[]):
    '''获取指定对象的插入参数'''
    paras = []
    for (k,v) in obj.__dict__.items():
        if k in filter: # 判断是否是过滤的字段
            continue
        if type(v) is int:
            paras.append(v)
        else:
            paras.append(get_code_str(v))
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
            paras.append(get_code_str(v))
            
    # 去除最后的逗号
    if len(sql_part1) > 1:
        sql_part1 = sql_part1[:-1]
        sql_part2 = sql_part2[:-1]
    # 得到最后的sql语句
    sql = sql % (sql_part1,sql_part2)
    
    # 返回sql和参数
    return (sql, paras)

def get_code_str(s, ts="gbk", cs="utf-8"):
    '''获取指定编码'''
    return s #str(s).decode(ts).encode(cs)

