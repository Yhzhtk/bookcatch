# coding=gbk
'''
Created on 2013-7-24
���ݿ������
@author: gudh
'''

import MySQLdb

# ���ݿ����Ӳ���
host="localhost"
port=3306
user="root"
passwd="314"
charset="utf8"

# ��ϸ���ݿ���Ϣ
db_name = "ebook"
book_table_name = "shotbook"
chapter_table_name = "chapter"

def insert_book(book):
    '''����һ�������Ϣ�����ݿ�'''
    try:
        conn = get_conn()
        cur = conn.cursor()
        # ��ȡ�������
        sp = get_insert_sql_and_paras(book_table_name, book, book.filter)
        
        conn.select_db(db_name)
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
        conn.select_db(db_name)
        
        # ��ȡ�������
        sql = get_insert_sql(chapter_table_name, chapters[0], chapters[0].filter)
        
        for chapter in chapters:
            # ѭ����������
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
        # �ж�Nid�Ƿ����
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
    '''��ѯ���ݿ�'''
    try:
        conn=MySQLdb.Connect(host='localhost',user='root',passwd='314',port=3306,charset='utf8')
        cur=conn.cursor()
        conn.select_db('python')
        cur.execute('update test set info="' + 'ȥ'.encode("utf8") + '" where id=3')
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
    '''�������ݿ����ӣ������ڴ�ʵ�����ӳ�'''
    return MySQLdb.Connect(host=host,user=user,passwd=passwd,port=port,charset=charset)

def get_insert_paras(obj, filter=[]):
    '''��ȡָ������Ĳ������'''
    paras = []
    for (k,v) in obj.__dict__.items():
        if k in filter: # �ж��Ƿ��ǹ��˵��ֶ�
            continue
        if type(v) is int:
            paras.append(v)
        else:
            paras.append(str(v).encode(charset))
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
            paras.append(str(v).encode(charset))
            
    # ȥ�����Ķ���
    if len(sql_part1) > 1:
        sql_part1 = sql_part1[:-1]
        sql_part2 = sql_part2[:-1]
    # �õ�����sql���
    sql = sql % (sql_part1,sql_part2)
    
    # ����sql�Ͳ���
    return (sql, paras)
