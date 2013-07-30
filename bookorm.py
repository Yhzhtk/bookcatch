# coding=gbk
'''
Created on 2013-7-24
���ݿ������
@author: gudh
'''

import MySQLdb
import bookconfig
from bookmode import Shotbook,Chapter

def insert_book(book):
    '''����һ�������Ϣ�����ݿ�'''
    try:
        conn = get_conn()
        cur = conn.cursor()
        # ��ȡ�������
        sp = get_insert_sql_and_paras(bookconfig.book_table_name, book, book.filter)
        
        conn.select_db(bookconfig.db_name)
        cur.execute(sp[0],sp[1])
        
        conn.commit()
        cur.close()
        conn.close()
        
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        
def insert_chapter(chapters):
    '''����һ����������½���Ϣ�����ݿ�'''
    if len(chapters) == 0:
        return
    try:
        conn = get_conn()
        cur = conn.cursor()
        conn.select_db(bookconfig.db_name)
        
        # ��ȡ�������
        sql = get_insert_sql(bookconfig.chapter_table_name, chapters[0], chapters[0].filter)
        
        for chapter in chapters:
            # ѭ����������
            paras = get_insert_paras(chapter, chapter.filter)
            cur.execute(sql, paras)
        
        conn.commit()
        cur.close()
        conn.close()
        
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def delete_book(nid, del_chap=False):
    '''ɾ����'''
    try:
        conn = get_conn()
        cur = conn.cursor()
        conn.select_db(bookconfig.db_name)
       
        sql = "delete from %s where nid = '%s'" % (bookconfig.book_table_name, nid)
        cur.execute(sql)
        
        if del_chap:
            # ɾ���½�
            sql = "delete from %s where nid = '%s'" % (bookconfig.chapter_table_name, nid)
            cur.execute(sql)
            
        conn.commit()
        cur.close()
        conn.close()
        
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return False

def delete_chapter(nid):
    '''ɾ���½�'''
    try:
        conn = get_conn()
        cur = conn.cursor()
        conn.select_db(bookconfig.db_name)
       
        sql = "delete from %s where nid = '%s'" % (bookconfig.chapter_table_name, nid)
        cur.execute(sql)
            
        conn.commit()
        cur.close()
        conn.close()
        
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return False

def exist_book(book_id):
    try:
        conn = get_conn()
        cur = conn.cursor()
        conn.select_db(bookconfig.db_name)
        # �ж�Nid�Ƿ����
        sql = "select count(*) from " + bookconfig.book_table_name + " where jdid = %s" 
        cur.execute(sql, book_id)
        result = cur.fetchone()
        
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return result[0] != 0

def select_one(sql, get_chap=False):
    '''��ѯ���ݿ�'''
    try:
        conn = get_conn()
        cur = conn.cursor()
        conn.select_db(bookconfig.db_name)
        count = cur.execute(sql)
        print '%s # count: %d' % (sql,count)
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        return get_mode_from_result(result, get_chap)
    
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def select_many(sql, get_chap=False, start = 0, count = -1):
    '''��ѯ���ݿ�, count=-1��ʾ�ж���ȡ���٣�Ϊ������Ϊȡ�ĸ���'''
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
        conn.close()
        
        return modes
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def get_book(nid, get_chap=False):
    '''����nid��ȡһ����'''
    sql = "select * from %s where nid= '%s'" % (bookconfig.book_table_name, nid)
    return select_one(sql, get_chap)

def get_all_book(get_chap=False):
    '''��ȡ�����鼮'''
    sql = "select * from " + bookconfig.book_table_name
    return select_many(sql, get_chap)

def get_chapter(nid):
    '''����nid��ȡһ����������½�'''
    sql = "select * from %s where nid= '%s'" % (bookconfig.chapter_table_name, nid)
    return select_many(sql, False)

def get_conn():
    '''�������ݿ����ӣ������ڴ�ʵ�����ӳ�'''
    return MySQLdb.Connect(host=bookconfig.host,
                           user=bookconfig.user,
                           passwd=bookconfig.passwd,
                           port=bookconfig.port,
                           charset=bookconfig.charset)

def get_mode_from_result(result, get_chap):
    '''�����ݿ���������mode'''
    mode = None
    if len(result) == 13:
        mode = Shotbook()
        # ���÷��丳ֵ
        for (i,m) in enumerate(Shotbook.db_field_seq):
            setattr(mode, m, result[i])
        # ����������ϢĬ�ϻ�ȡ�����½�
        if get_chap:
            sql = "select * from " + bookconfig.chapter_table_name + " where nid='%s'" % mode.nid
            mode.chapters = select_many(sql)
    elif len(result) == 6:
        mode = Chapter()
        for (i,m) in enumerate(Chapter.db_field_seq):
            setattr(mode, m, result[i])
    return mode

def get_insert_paras(obj, filter=[]):
    '''��ȡָ������Ĳ������'''
    paras = []
    for (k,v) in obj.__dict__.items():
        if k in filter: # �ж��Ƿ��ǹ��˵��ֶ�
            continue
        if type(v) is int:
            paras.append(v)
        else:
            paras.append(get_code_str(v))
    # ���ز���
    return paras

def get_insert_sql(table_name, obj, filter=[]):
    '''��ȡָ�������sql�������'''
    sql = "insert into " + table_name + "(%s) values (%s)"
    sql_part1 = ""
    sql_part2 = ""
    for (k,v) in obj.__dict__.items():
        if k in filter: # �ж��Ƿ��ǹ��˵��ֶ�
            continue
        sql_part1 += k + ","
        
        # The format string is not really a normal Python format string. You must always use %s for all fields.
        # ������������˺þã�ԭ�����ת����Python��ת����һ�������ж�Ҫ��%s������%d
        if type(v) is int:
            sql_part2 += "%s," # �����int��ʹ�� %d
        else:
            sql_part2 += "%s," # ���򶼵������ַ���
            
    # ȥ�����Ķ���
    if len(sql_part1) > 1:
        sql_part1 = sql_part1[:-1]
        sql_part2 = sql_part2[:-1]
    # �õ�����sql���
    sql = sql % (sql_part1,sql_part2)
    
    # ����sql�Ͳ���
    return sql

def get_insert_sql_and_paras(table_name, obj, filter=[]):
    '''��ȡָ�������sql�������Ͳ���'''
    sql = "insert into " + table_name + "(%s) values (%s)"
    sql_part1 = ""
    sql_part2 = ""
    paras = []
    for (k,v) in obj.__dict__.items():
        if k in filter: # �ж��Ƿ��ǹ��˵��ֶ�
            continue
        sql_part1 += k + ","
        
        # The format string is not really a normal Python format string. You must always use %s for all fields.
        # ������������˺þã�ԭ�����ת����Python��ת����һ�������ж�Ҫ��%s������%d
        if type(v) is int:
            sql_part2 += "%s," # �����int��ʹ�� %d
            paras.append(v)
        else:
            sql_part2 += "%s," # ���򶼵������ַ���
            paras.append(get_code_str(v))
            
    # ȥ�����Ķ���
    if len(sql_part1) > 1:
        sql_part1 = sql_part1[:-1]
        sql_part2 = sql_part2[:-1]
    # �õ�����sql���
    sql = sql % (sql_part1,sql_part2)
    
    # ����sql�Ͳ���
    return (sql, paras)

def get_code_str(s, ts="gbk", cs="utf-8"):
    '''��ȡָ������'''
    return str(s).decode(ts).encode(cs)

