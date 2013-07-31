# coding=gbk
'''
Created on 2013-7-26
所有配置
@author: gudh
'''

import yaml,os

# 默认请求头
default_header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.84 Safari/537.22' }

# 数据库连接参数
host=""
port=3306
user="root"
passwd="314"
charset="utf8"
# 详细数据库信息
db_name = "ebook"
book_table_name = "shotbook"
chapter_table_name = "chapter"

# 文件下载根路径
rootpath = "F:/ebook/"

# 所有坐标信息
fhsj_pos_sleep = (109, 74, 1) # 返回书架位置
wdcd_pos_sleep = (118, 202, 1) # 我的畅读位置
sx_pos_sleep = (339, 79, 1) # 刷新
zxcd_first_pos_sleep = (492, 171, 1) # 在线畅读第一本数的位置
dect = (158, 175, 607, 928) # 截图区域
next_pos_sleep = (666, 568, 0.2) # 下一页位置，延时

def load_yaml(yaml_file):
    '''加载yaml配置参数'''
    stream = file(yaml_file, 'r')
    config = yaml.load(stream)
    
    for field in globals():
        if field in config:
            globals()[field] = config[field]

# 加载配置文件
yaml_file = r'config.yaml'
if not os.path.exists(yaml_file):
    yaml_file = "../" + yaml_file
load_yaml(yaml_file)
    