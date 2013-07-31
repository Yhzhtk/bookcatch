# -*- coding: utf-8 -*-

"""
Module implementing BookMain.
"""

from PyQt4.QtGui import QMainWindow,QListWidgetItem,QTableWidgetItem,QPixmap,QFont,QBrush,QProgressBar,QLabel
from PyQt4.QtCore import pyqtSignature,Qt
from Ui_BookMain import Ui_MainWindow
import os
# yh.book指上级目录，包就没放进来了
from yh.book import bookorm,bookconfig

day_path = bookconfig.rootpath + "%s/"  # 测试使用路径
col_num = bookconfig.col_num # 默认选图列数
page_count = bookconfig.page_count # 每页图片数
img_width = bookconfig.img_width # 默认图像宽度
img_height = bookconfig.img_height # 默认图像高度

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
        
        self.statusLabel = QLabel(self.decode("就绪"))
        self.statusBar.addWidget(self.statusLabel, 1)
        self.progressBar = QProgressBar()
        self.progressBar.setAlignment(Qt.AlignRight)
        self.statusBar.addWidget(self.progressBar, 1)
        
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
    
    def __get_current_r_c(self):
        '''获取当前文本所在的行列'''
        item = self.imgTableWidget.currentIndex()
        if not item:
            return (-1, -1)
        (r, c) = (item.row(),item.column())
        return (r, c)
    
    def __get_current_tr_c(self):
        '''获取当前文本所在的行列的文本列'''
        item = self.imgTableWidget.currentIndex()
        if not item:
            return (-1, -1)
        (r, c) = (item.row(),item.column())
        if r % 2 == 0:
            r += 1
        return (r, c)
    
    def __show_bookinfo(self, book):
        '''显示书的信息'''
        self.nidEdit.setText(book.nid)
        self.nidEdit.setEnabled(False)
        date = book.createTime[0:10].replace("-", "")
        cover_path = day_path % date + "cover/" + book.nid[0:2] + "/" + book.nid[2:4] + "/" + book.nid[4:] + ".jpg"
        self.coverImgLabel.setPixmap(QPixmap(cover_path))
        self.bookNameEdit.setText(book.bookName)
        self.authorEdit.setText(book.author)
        self.typeEdit.setText(book.type)
        self.descriptionEdit.setText(book.description)
        self.createTimeEdit.setText(book.createTime)
        self.createTimeEdit.setEnabled(False)
    
    def __show_imgs(self, book, page):
        '''显示指定分页的图片'''
        start = page * page_count
        end = start + page_count
        if end > book.imgCount:
            end = book.imgCount
        
        imgCount = end - start
        rc = (imgCount - 1)/col_num + 1 # 行数
        
        # 设置行列数
        self.imgTableWidget.setColumnCount(col_num)
        self.imgTableWidget.setRowCount(rc * 2)
        
        # 设置行列的宽度
        for c in range(col_num):
            self.imgTableWidget.setColumnWidth(c,img_width)
        for r in range (rc):
            self.imgTableWidget.setRowHeight(r * 2,img_height)
            self.imgTableWidget.setRowHeight(r * 2 + 1,20)
        
        # 获取书的基本路径
        date = book.createTime[0:10].replace("-", "")
        book_path = day_path % date + "content/low/" + book.nid[0:2] + "/" + book.nid[2:4] + "/" + book.nid[4:] + "/1/%s.jpg"
        
        # 进度条最大值
        self.progressBar.setMaximum(imgCount)
        
        for i in range(start + 1, end + 1):
            self.progressBar.setValue(i)
            
            # split 表示是否识别为大图
            split = False
            path = book_path % str(i)
            if not os.path.exists(path):
                path = book_path % (str(i) + "_b")
                split = True
            (r, c) = self.__get_r_c(col_num, i - start)
            tr = r + 1
            
            # 设置图片，文字为路径
            item = QTableWidgetItem(path)
            if os.path.exists(path):
                item.setData(1, QPixmap(path).scaled(img_width, img_height))
            self.imgTableWidget.setItem(r, c, item)
            # 设置显示文字，章节名或者编号
            item = QTableWidgetItem(str(i))
            if split:
                item.setText(str(i) + self.decode(" 识别分章"))
                item.setFont(QFont("黑体", 12, QFont.Bold))
                item.setForeground(QBrush(Qt.red))
            self.imgTableWidget.setItem(tr, c, item)
        
        # 设置当前分页
        self.nowPageLabel.setText(str(page + 1))
        
        # 设置翻页是否可用
        all_page = int(self.allPageLabel.text())
        if page <= 0:
            self.previousBtn.setEnabled(False)
        else:
            self.previousBtn.setEnabled(True)
        if page >= all_page - 1:
            self.nextBtn.setEnabled(False)
        else:
            self.nextBtn.setEnabled(True)
        
        self.show_status(self.decode("加载书籍 %s 章节图片成功，共有图片数 %d") % (book.bookName, imgCount))
    
    def decode(self, string):
        return string.decode("utf-8")
    
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
        self.show_status(self.decode("加载需要分章的图书数量: %s") % len(books))
    
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
            ss = str(self.__get_index(col_num, tr - 1, c))
            self.imgTableWidget.setItem(tr, c, QTableWidgetItem(ss))
            self.show_status(self.decode("清除分章: %s") % (ss))
        else:
            self.show_status(self.decode("请选择一张图片进行操作"))

    @pyqtSignature("")
    def on_saveBookInfoBtn_clicked(self):
        """保存"""
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSignature("")
    def on_previousBtn_clicked(self):
        """上一页"""
        nowPage = int(self.nowPageLabel.text()) - 1
        if nowPage > 0:
            nowPage -= 1
            nid = self.nidEdit.text()
            book = bookorm.get_book(nid, False)
            self.__show_imgs(book, nowPage)
    
    @pyqtSignature("")
    def on_nextBtn_clicked(self):
        """下一页"""
        allPage = int(self.allPageLabel.text())
        nowPage = int(self.nowPageLabel.text()) - 1
        if nowPage < allPage - 1:
            nowPage += 1
            nid = self.nidEdit.text()
            book = bookorm.get_book(nid, False)
            self.__show_imgs(book, nowPage)
    
    
    @pyqtSignature("QModelIndex")
    def on_bookListWidget_doubleClicked(self, index):
        """选择书"""
        self.chapListWidget.clear()
        self.imgTableWidget.clear()
        
        select_nid = self.bookListWidget.currentItem().text().split("#")[1]
        self.show_status(self.decode("正在加载书籍 %s 的所有章节和图片，这需要一定时间，请稍后。") % select_nid)
        book = bookorm.get_book(select_nid, True)
        chapters = book.chapters
        i = 0
        for chap in chapters:
            i += 1
            line = chap.cTitle.ljust(30) + "#" + str(chap.cid)
            self.chapListWidget.addItem(QListWidgetItem(str(i) + self.decode("。") + line))
        
        # 显示书籍信息
        self.__show_bookinfo(book)
        
        # 设置页数
        nowPage = 0
        # 显示时加1
        allPage = (book.imgCount - 1) / page_count + 1
        self.allPageLabel.setText(str(allPage))
        
        # 显示图片数据
        self.__show_imgs(book, nowPage)
        
    
    @pyqtSignature("QModelIndex")
    def on_chapListWidget_doubleClicked(self, index):
        """选择章节"""
        select_text = unicode(self.chapListWidget.currentItem().text())
        chap_name = select_text.split("#")[0].split(self.decode("。"))[1].strip()
        (tr, c) = self.__get_current_tr_c()
        if (tr, c) != (-1, -1):
            item = QTableWidgetItem(chap_name)
            item.setFont(QFont("黑体", 12, QFont.Bold))
            item.setForeground(QBrush(Qt.red))
            self.imgTableWidget.setItem(tr, c, item)
            self.show_status(self.decode("设定分章 %d : %s") % (self.__get_index(col_num, tr, c), chap_name))
        else:
            self.show_status(self.decode("请选择一张图片进行操作"))
            
    @pyqtSignature("QModelIndex")
    def on_imgTableWidget_doubleClicked(self, index):
        """打开大图"""
        (r, c) = self.__get_current_r_c()
        if (r, c) != (-1, -1) and r % 2 == 0:
            img_path = self.imgTableWidget.item(r, c).text()
            os.startfile(img_path)
