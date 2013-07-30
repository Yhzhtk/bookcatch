# -*- coding: utf-8 -*-

"""
Module implementing BookMain.
"""

from PyQt4.QtGui import QMainWindow,QListWidgetItem,QTableWidgetItem,QPixmap
from PyQt4.QtCore import pyqtSignature,Qt

from Ui_BookMain import Ui_MainWindow

# yh.book指上级目录，包就没放进来了
from yh.book import bookorm

root_path = "D:/dd/mm/low/" # 测试使用路径
cc = 5 # 默认选图列数

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
        self.showMaximized()
        
    def __get_r_c(self, col_num, index):
        '''根据index获取所在行列'''
        r = (index - 1) / col_num * 2
        c = (index - 1) % col_num
        return (r, c)

    def __get_index(self, col_num, r, c):
        '''根据r和c获取index'''
        index = r / 2 * col_num + c
        return index
        
    @pyqtSignature("")
    def on_pBtn1_clicked(self):
        """刷新"""
        self.bookListWidget.clear()
        books = bookorm.get_all_book()
        for book in books:
            line = book.bookName.ljust(30) + "#" + book.nid
            print line
            self.bookListWidget.addItem(QListWidgetItem(line))
    
    @pyqtSignature("")
    def on_pBtn2_clicked(self):
        """保存"""
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSignature("QModelIndex")
    def on_bookListWidget_doubleClicked(self, index):
        """选择书"""
        self.chapListWidget.clear()
        self.imgTableWidget.clear()
        
        select_nid = self.bookListWidget.currentItem().text().split("#")[1]
        book = bookorm.get_book(select_nid, True)
        chapters = book.chapters
        i = 0
        for chap in chapters:
            i += 1
            line = chap.cTitle.ljust(30) + "#" + str(chap.cid)
            print line
            self.chapListWidget.addItem(QListWidgetItem(str(i) + "。".decode("utf-8") + line))
        
        # 处理tableWidget
        rc = (book.imgCount - 1)/cc + 1 # 行数
        w = 200
        h = 333
        self.imgTableWidget.setColumnCount(5)
        self.imgTableWidget.setRowCount(rc * 2)
        
        for i in range(1, book.imgCount):
            path = root_path + "%d.jpg" % i
            (r, c) = self.__get_r_c(cc, i)
            tr = r + 1
            self.imgTableWidget.setColumnWidth(c,w)
            self.imgTableWidget.setRowHeight(r,h)
            self.imgTableWidget.setRowHeight(tr,20)
            
            item = QTableWidgetItem(str(i))
            item.setData(1, QPixmap(path).scaled(w, h))
            item.setTextAlignment(Qt.AlignBottom)
            self.imgTableWidget.setItem(r, c, item)
            
            self.imgTableWidget.setItem(tr, c, QTableWidgetItem(str(i)))
    
    @pyqtSignature("QModelIndex")
    def on_chapListWidget_doubleClicked(self, index):
        """选择章节"""
        select_text = unicode(self.chapListWidget.currentItem().text(),'gbk','ignore')
        chap_name = select_text.split("#")[0].split("。".decode("utf-8"))[1].strip()
        select_img = self.imgTableWidget.currentItem()
        if not select_img:
            return
        img_no = int(select_img.text())
        (r, c) = self.__get_r_c(cc, img_no)
        if r % 2 == 0:
            r += 1
        self.imgTableWidget.item(r, c).setText(chap_name)


