# -*- coding: utf-8 -*-

"""
Module implementing BookMain.
"""

from PyQt4.QtGui import QMainWindow,QListWidgetItem,QTableWidgetItem,QPixmap,QLabel
from PyQt4.QtCore import pyqtSignature

from Ui_BookMain import Ui_MainWindow

# yh.book指上级目录，包就没放进来了
from yh.book import bookorm

root_path = "D:/dd/mm/low/" # 测试使用路径
cc = 5 # 默认选图列数
w = 200 # 默认图像宽度
h = 333 # 默认图像高度

class BookMain(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        # 添加状态栏
        self.statusLabel = QLabel(self.decode("就绪"))
        self.statusBar.addWidget(self.statusLabel)
        self.showMaximized()
        
    def __get_r_c(self, col_num, index):
        '''根据index获取所在行列'''
        r = (index - 1) / col_num * 2
        c = (index - 1) % col_num
        return (r, c)

    def __get_index(self, col_num, r, c):
        '''根据r和c获取index'''
        if r % 2 == 1:
            r -= 1
        index = r / 2 * col_num + c
        return index + 1
    
    def __get_current_tr_c(self):
        '''获取当前文本所在的行列'''
        item = self.imgTableWidget.currentIndex()
        if not item:
            return (-1, -1)
        (r, c) = (item.row(),item.column())
        if r % 2 == 0:
            r += 1
        return (r, c)
    
    def decode(self, str):
        return str.decode("utf-8")
    
    def show_status(self, msg):
        '''状态栏显示消息'''
        self.statusLabel.setText(msg)
        
    @pyqtSignature("")
    def on_pBtn1_clicked(self):
        """刷新"""
        self.show_status(self.decode("正在加载所有书，请稍后。"))
        self.bookListWidget.clear()
        books = bookorm.get_all_book()
        for book in books:
            line = book.bookName.ljust(30) + "#" + book.nid
            self.bookListWidget.addItem(QListWidgetItem(line))
        self.show_status(self.decode("加载图书数量: %s") % len(books))
    
    @pyqtSignature("")
    def on_pBtn2_clicked(self):
        """保存"""
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSignature("")
    def on_pBtn3_clicked(self):
        """清除分章"""
        (tr, c) = self.__get_current_tr_c()
        if (tr, c) != (-1, -1):
            ss = str(self.__get_index(cc, tr - 1, c))
            self.imgTableWidget.item(tr, c).setText(ss)
            self.show_status(self.decode("清除分章: %s") % (ss))
        else:
            self.show_status(self.decode("请选择一张图片进行操作"))
    
    @pyqtSignature("QModelIndex")
    def on_bookListWidget_doubleClicked(self, index):
        """选择书"""
        self.chapListWidget.clear()
        self.imgTableWidget.clear()
        
        select_nid = self.bookListWidget.currentItem().text().split("#")[1]
        self.show_status(self.decode("正在加载书籍 %s 的所有章节，这需要一定时间，请稍后。") % select_nid)
        book = bookorm.get_book(select_nid, True)
        chapters = book.chapters
        i = 0
        for chap in chapters:
            i += 1
            line = chap.cTitle.ljust(30) + "#" + str(chap.cid)
            self.chapListWidget.addItem(QListWidgetItem(str(i) + self.decode("。") + line))
        
        # 处理tableWidget
        rc = (book.imgCount - 1)/cc + 1 # 行数

        self.imgTableWidget.setColumnCount(5)
        self.imgTableWidget.setRowCount(rc * 2)
        
        for i in range(1, book.imgCount + 1):
            path = root_path + "%d.jpg" % i
            (r, c) = self.__get_r_c(cc, i)
            tr = r + 1
            self.imgTableWidget.setColumnWidth(c,w)
            self.imgTableWidget.setRowHeight(r,h)
            self.imgTableWidget.setRowHeight(tr,20)
            
            # 设置图片和下临文字
            item = QTableWidgetItem(str(i))
            item.setData(1, QPixmap(path).scaled(w, h))
            self.imgTableWidget.setItem(r, c, item)
            self.imgTableWidget.setItem(tr, c, QTableWidgetItem(str(i)))
        self.show_status(self.decode("加载成功。"))
    
    @pyqtSignature("QModelIndex")
    def on_chapListWidget_doubleClicked(self, index):
        """选择章节"""
        select_text = unicode(self.chapListWidget.currentItem().text())
        chap_name = select_text.split("#")[0].split(self.decode("。"))[1].strip()
        (tr, c) = self.__get_current_tr_c()
        if (tr, c) != (-1, -1):
            self.imgTableWidget.item(tr, c).setText(chap_name)
            self.show_status(self.decode("设定分章 %d : %s") % (self.__get_index(cc, tr, c), chap_name))
        else:
            self.show_status(self.decode("请选择一张图片进行操作"))


