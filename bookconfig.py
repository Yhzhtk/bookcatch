# coding=gbk
'''
Created on 2013-7-26
��������
@author: gudh
'''

# Ĭ������ͷ
default_header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.84 Safari/537.22' }

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

# �ļ����ظ�·��
rootpath = "F:/ebook/"

# ����������Ϣ
fhsj_pos_sleep = (109, 74, 1) # �������λ��
wdcd_pos_sleep = (118, 202, 1) # �ҵĳ���λ��
sx_pos_sleep = (339, 79, 1) # ˢ��
zxcd_first_pos_sleep = (492, 171, 1) # ���߳�����һ������λ��
dect = (158, 175, 607, 928) # ��ͼ����
next_pos_sleep = (666, 568, 0.2) # ��һҳλ�ã���ʱ