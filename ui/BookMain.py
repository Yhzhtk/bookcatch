# -*- coding: utf-8 -*-

"""
Module implementing BookMain.
"""

from PyQt4.QtGui import QMainWindow,QListWidgetItem,QTableWidgetItem,QPixmap,QFont,QBrush,QProgressBar,QLabel
from PyQt4.QtCore import pyqtSignature,Qt
from Ui_BookMain import Ui_MainWindow
import os
# yh.book指上级目录，包就没放进来了
from yh.book import bookmode,bookorm,bookconfig

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
        
        self.split_chap_infos = {}
        
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
    
    def __refresh_chap_count(self, update_index):
        '''更新章节数量'''
        now_chap_count = self.completeListWidget.count()
        if update_index >= now_chap_count or update_index < 0:
            return
        last_index = 0
        if update_index > 0:
            last_index = int(self.completeListWidget.item(update_index - 1).text().split(self.decode("。"))[1])
        infos = self.completeListWidget.item(update_index).text().split(self.decode("。"))
        index = int(infos[1])
        chap_name = infos[3]
        self.completeListWidget.item(update_index).setText(str(update_index)  + self.decode("。") + str(index) + self.decode("。(") + str(index - last_index) + self.decode(")。")+ chap_name)
    
    def __add_split_info(self, index, chap_name):
        '''添加一条分章信息'''
        now_chap_count = self.completeListWidget.count()
        loc = 0
        last_index = 0
        is_add = False
        if now_chap_count > 0:
            for i in range(now_chap_count):
                i_index = int(self.completeListWidget.item(i).text().split(self.decode("。"))[1])
                if index < i_index:
                    loc = i
                    is_add = True
                    break
                elif index == i_index:
                    self.completeListWidget.takeItem(i)
                    loc = i
                    is_add = False
                    break
                last_index = i_index
            else:
                loc = now_chap_count
        self.split_chap_infos[str(index)] = chap_name
        self.completeListWidget.insertItem(loc, QListWidgetItem(str(loc)  + self.decode("。") + str(index) + self.decode("。(") + str(index - last_index) + self.decode(")。")+ chap_name))
        if is_add:
            self.__refresh_chap_count(loc + 1)
        
    def __del_split_info(self, index):
        '''删除分章信息'''
        for i in range(self.completeListWidget.count()):
            i_index = int(self.completeListWidget.item(i).text().split(self.decode("。"))[1])
            if index == i_index:
                self.completeListWidget.takeItem(i)
                self.split_chap_infos[str(index)] = None
                self.__refresh_chap_count(i)
                return
    
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
            # 路径判断是否分章
            if not os.path.exists(path):
                path = book_path % (str(i) + "_b")
                if os.path.exists(path):
                    split = True
            # 内存判断是否分章
            if self.split_chap_infos.has_key(str(i)):
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
                if self.split_chap_infos.has_key(str(i)):
                    # 已有分章信息
                    chap_name = self.split_chap_infos[str(i)] 
                    if chap_name:
                        item.setText(chap_name)
                        item.setFont(QFont("黑体", 12, QFont.Bold))
                        item.setForeground(QBrush(Qt.red))
                else:
                    # 没有分章信息设置分章信息
                    item.setText(self.decode("识别分章"))
                    self.__add_split_info(i, item.text())
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
    
    def __get_start_index(self):
        '''获取基准的index从开始，别忘了加1'''
        return (int(self.nowPageLabel.text()) - 1) * page_count
    
    def __deal_now_page_split_chap(self):
        '''保存当前页的分章信息'''
        c = self.imgTableWidget.columnCount()
        r = self.imgTableWidget.rowCount()
        start_index = self.__get_start_index()
        for x in range(1, r, 2):
            for y in range(c):
                index = start_index + self.__get_index(col_num, x, y)
                item = self.imgTableWidget.item(x, y)
                font = item.font()
                size = font.pointSize()
                if item.font().pointSize() == 12:
                    # 根据字体大小判断是否分章
                    chap_name = self.imgTableWidget.item(x, y).text()
                    self.__add_split_info(index, chap_name)
                    print "识别分章", index, chap_name
    
    def decode(self, string):
        '''编码'''
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
        """保存分章信息"""
        # 保存当前页的分章信息
        self.__deal_now_page_split_chap()
        
        count = self.completeListWidget.count()
        
        if count < 1:
            self.show_status(self.decode("没有分章不能保存，请确认分章信息正确后保存，保存好原始分章书籍就没有了。"))
            return
        
        try:
            nid = str(self.nidEdit.text())
            book = bookorm.get_book(nid, False)
            chapters = []
            # 解析分章信息
            cid = 1
            pcount = 0
            for i in range(count):
                index_chapname = str(self.completeListWidget.item(i).text()).split(self.decode("。"))
                index_chapname[1] = int(index_chapname[1])
                chapter = bookmode.Chapter()
                chapter.author = book.author
                chapter.bookName = book.bookName
                chapter.cid = cid
                cid += 1
                chapter.cTitle = str(index_chapname[3])
                chapter.imgCount = int(index_chapname[1] - pcount)
                pcount = index_chapname[1]
                chapter.nid = book.nid
                chapters.append(chapter)
            
            # 保存
            book.chapters = chapters
            bookorm.save_chapters(nid, chapters)
            
            # 更新书籍信息
            book.complete_chapter()
            book.upTime()
            book.chapterok = 1
            bookorm.save_book(book)
            
            self.show_status(self.decode("保存分章信息成功：%s %s 章节数： %d") % (nid, book.bookName, len(chapters)))
        except Exception, e:
            print self.decode("保存出错了：%s" % str(e))
            self.show_status(self.decode("保存出错了：%s" % str(e)))
    
    @pyqtSignature("")
    def on_pBtn3_clicked(self):
        """清除分章"""
        (tr, c) = self.__get_current_tr_c()
        if (tr, c) != (-1, -1):
            index = self.__get_start_index() + self.__get_index(col_num, tr - 1, c)
            self.imgTableWidget.setItem(tr, c, QTableWidgetItem(str(index)))
            self.show_status(self.decode("清除分章: %s") % str(index))
            
            self.__del_split_info(index)
        else:
            self.show_status(self.decode("请选择一张图片进行操作"))
            
    @pyqtSignature("")
    def on_upCoverBtn_clicked(self):
        '''修改封面图片'''
        date = self.createTimeEdit.text()[0:10].replace("-", "")
        nid = self.nidEdit.text()
        cover_path = day_path % date + "cover/" + nid[0:2] + "/" + nid[2:4] + "/"
        os.startfile(cover_path)

    @pyqtSignature("")
    def on_saveBookInfoBtn_clicked(self):
        """保存书籍信息"""
        try:
            nid = self.nidEdit.text()
            book = bookorm.get_book(nid, False)
            bookName = str(self.bookNameEdit.text())
            if bookName:
                book.bookName = bookName
            author = str(self.authorEdit.text())
            if author:
                book.author = author
            btype = str(self.typeEdit.text())
            if btype:
                book.type = btype
            desc = str(self.descriptionEdit.toPlainText())
            if desc:
                book.description = desc
            book.str()
            # 先删除在插入
            bookorm.save_book(book)
            
            self.show_status(self.decode("修改书籍信息成功: %s %s" % (nid, bookName)))
        except Exception, e:
            print self.decode("保存出错了：%s" % str(e))
            self.show_status(self.decode("保存出错了：%s" % str(e)))
    
    @pyqtSignature("")
    def on_previousBtn_clicked(self):
        """上一页"""
        # 保存当前页的分章信息
        self.__deal_now_page_split_chap()
        nowPage = int(self.nowPageLabel.text()) - 1
        if nowPage > 0:
            nowPage -= 1
            nid = self.nidEdit.text()
            book = bookorm.get_book(nid, False)
            self.__show_imgs(book, nowPage)
    
    @pyqtSignature("")
    def on_nextBtn_clicked(self):
        """下一页"""
        # 保存当前页的分章信息
        self.__deal_now_page_split_chap()
        
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
        # 清除上一本书的信息
        self.chapListWidget.clear()
        self.imgTableWidget.clear()
        self.split_chap_infos = {}
        self.completeListWidget.clear()
        
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
            
            start_index = self.__get_start_index()
            self.__add_split_info(start_index + self.__get_index(col_num, tr, c), chap_name)
        else:
            self.show_status(self.decode("请选择一张图片进行操作"))
            
    @pyqtSignature("QModelIndex")
    def on_imgTableWidget_doubleClicked(self, index):
        """打开大图"""
        (r, c) = self.__get_current_r_c()
        if (r, c) != (-1, -1) and r % 2 == 0:
            img_path = self.imgTableWidget.item(r, c).text()
            os.startfile(img_path)
