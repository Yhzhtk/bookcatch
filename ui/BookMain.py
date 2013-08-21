# -*- coding: utf-8 -*-

"""
Module implementing BookMain.
"""

from PyQt4.QtGui import QMainWindow,QListWidgetItem,QTableWidgetItem,QPixmap,QFont,QBrush,QProgressBar,QLabel,QMessageBox,QColor
from PyQt4.QtCore import pyqtSignature,Qt
from Ui_BookMain import Ui_MainWindow
import os 
# yh.book指上级目录，包就没放进来了
from yh.book import bookmode,bookorm,bookconfig,bookcrawl

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
        
        self.statusLabel = QLabel(self.decode_file("就绪"))
        self.statusBar.addWidget(self.statusLabel, 1)
        self.progressBar = QProgressBar()
        self.progressBar.setAlignment(Qt.AlignRight)
        self.statusBar.addWidget(self.progressBar, 1)
        
        self.split_chap_infos = {}
        # 是否已保存
        self.is_save = True
        self.__set_save(True)
        
    def __set_save(self, is_save):
        self.is_save = is_save
        self.saveChapterBtn.setEnabled(not is_save)
        
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
    
    def __get_selects_tr_c(self):
        '''获取选中的多个item'''
        indexs = self.imgTableWidget.selectedIndexes()
        if not indexs or len(indexs) == 0:
            return None
        rcs = [(item.row(),item.column()) for item in indexs]
        res = []
        for (r, c) in rcs:
            if r % 2 == 0:
                r += 1
            res.append((r, c))
        return res
    
    def __show_bookinfo(self, book):
        '''显示书的信息'''
        self.nidEdit.setText(book.nid)
        self.nidEdit.setEnabled(False)
        date = book.createTime[0:10].replace("-", "")
        cover_path = day_path % date + "cover/" + book.nid[0:2] + "/" + book.nid[2:4] + "/" + book.nid[4:] + ".jpg"
        self.coverImgLabel.setText(cover_path)
        if os.path.exists(cover_path):
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
            last_index = int(self.decode_text(self.completeListWidget.item(update_index - 1).text()).split(self.decode_file("。"))[1])
        infos = self.decode_text(self.completeListWidget.item(update_index).text()).split(self.decode_file("。"))
        index = int(infos[1])
        chap_name = infos[3]
        self.completeListWidget.item(update_index).setText(str(update_index)  + self.decode_file("。") + str(index) + self.decode_file("。(") + str(index - last_index) + self.decode_file(")。")+ chap_name)
    
    def __add_split_info(self, index, chap_name):
        '''添加一条分章信息'''
        now_chap_count = self.completeListWidget.count()
        loc = 0
        last_index = 0
        is_add = False
        if now_chap_count > 0:
            for i in range(now_chap_count):
                i_index = int(self.decode_text(self.completeListWidget.item(i).text()).split(self.decode_file("。"))[1])
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
        self.completeListWidget.insertItem(loc, QListWidgetItem(str(loc)  + self.decode_file("。") + str(index) + self.decode_file("。(") + str(index - last_index) + self.decode_file(")。")+ chap_name))
        if is_add:
            self.__refresh_chap_count(loc + 1)
    
    def __add_all_split_info(self):
        '''添加所有分章信息'''
        indexs = [ int(k) for k, v in self.split_chap_infos.items() if v != None]
        indexs.sort()
        self.completeListWidget.clear()
        for index in indexs:
            v = self.split_chap_infos[str(index)]
            self.__add_split_info(index, v)
    
    def __del_split_info(self, index):
        '''删除分章信息'''
        for i in range(self.completeListWidget.count()):
            i_index = int(self.decode_text(self.completeListWidget.item(i).text()).split(self.decode_file("。"))[1])
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
        
        self.show_status(self.decode_file("加载书籍 %s 第 %d 页  图片数 %d， 由于网络加载需要一定时间，请等待。。") % (book.bookName, page + 1, imgCount))
        
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
        book_path = day_path % date + "content/l/" + book.nid[0:2] + "/" + book.nid[2:4] + "/" + book.nid[4:] + "/1/%s.jpg"
        
        # 进度条最大值
        self.progressBar.setMaximum(imgCount)
        
        for i in range(start + 1, end + 1):
            self.progressBar.setValue(i - start)
            
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
                        # 判断是否人工删除置为了None
                        item.setText(chap_name)
                        self.__set_font(item, True)
                else:
                    # 没有分章信息设置分章信息
                    item.setText(self.decode_file("识别分章"))
                    self.__add_split_info(i, self.decode_text(item.text()))
                    self.__set_font(item, True)
            # 行间分颜色
            self.__set_background(item, tr)
            self.imgTableWidget.setItem(tr, c, item)
        else:
            # 移除最后一点数据
            for lc in range(c + 1, col_num):
                if page == 0:
                    item = QTableWidgetItem("blank")
                    self.__set_font(item, False)
                    self.imgTableWidget.setItem(r, lc, item)
                    item = QTableWidgetItem("blank")
                    self.__set_font(item, False)
                    self.imgTableWidget.setItem(tr, lc, item)
                else:
                    item = self.imgTableWidget.item(r, lc)
                    item.setText("")
                    item.setData(1, None)
                    item = self.imgTableWidget.item(tr, lc)
                    item.setText("")
                    self.__set_font(item, False)
        
        # 设置当前分页
        self.nowPageLabel.setText(str(page + 1))
        
        # 设置翻页是否可用
        all_page = int(self.decode_text(self.allPageLabel.text()))
        if page <= 0:
            self.previousBtn.setEnabled(False)
        else:
            self.previousBtn.setEnabled(True)
        if page >= all_page - 1:
            self.nextBtn.setEnabled(False)
        else:
            self.nextBtn.setEnabled(True)
        
        # 刷新显示分章
        self.__deal_now_page_split_chap()
        
        # 翻页后置顶
        self.__move_table_scroll((self.imgTableWidget.verticalScrollBar().minimumHeight()))
        self.show_status(self.decode_file("加载书籍 %s 第 %d 页图片成功，共有图片数 %d") % (book.bookName, page + 1, imgCount))
    
    def __get_start_index(self):
        '''获取基准的index从开始，别忘了加1'''
        return (int(self.decode_text(self.nowPageLabel.text())) - 1) * page_count
    
    def __deal_now_page_split_chap(self):
        '''保存当前页的分章信息，保存当前页的章节更改信息'''
        c = self.imgTableWidget.columnCount()
        r = self.imgTableWidget.rowCount()
        start_index = self.__get_start_index()
        for x in range(1, r, 2):
            for y in range(c):
                index = start_index + self.__get_index(col_num, x, y)
                item = self.imgTableWidget.item(x, y)
                if item.font().pointSize() == 12:
                    # 根据字体大小判断是否分章
                    chap_name = self.decode_text(self.imgTableWidget.item(x, y).text())
                    self.__add_split_info(index, chap_name)
                    # print u"识别分章", index, chap_name
        self.show_status(u"刷新分章信息 ok")
    
    def __move_table_scroll(self, value, maxinum = None):
        '''设置图片table垂直滚动条位置'''
        self.imgTableWidget.verticalScrollBar().setValue(value)
        if maxinum:
            self.imgTableWidget.verticalScrollBar().setMaximum(maxinum)
        
    def __set_background(self, item, tr):
        '''设置背景颜色'''
        if (tr - 1) % 6 == 0:
            item.setBackgroundColor(QColor(255,255,180))
        elif (tr - 1) % 6 == 2:
            item.setBackgroundColor(QColor(150,255,170))
        else:
            item.setBackgroundColor(QColor(255,185,255))
    
    def __set_font(self, item, is_split = False):
        '''设置字体'''
        if is_split:
            item.setFont(QFont("黑体", 12, QFont.Bold))
            item.setForeground(QBrush(Qt.red))
        else:
            item.setFont(QFont())
            item.setForeground(QBrush(Qt.black))
    
    def decode_file(self, string):
        '''编码'''
        return string.decode("utf-8")
    
    def decode_text(self, string):
        '''编码'''
        return unicode(string)
    
    def show_status(self, msg):
        '''状态栏显示消息'''
        print msg
        self.statusLabel.setText(msg)
        
    @pyqtSignature("")
    def on_refreshBookBtn_clicked(self):
        """刷新"""
        self.show_status(self.decode_file("正在加载所有书，请稍后。"))
        self.bookListWidget.clear()
        books = bookorm.get_all_book()
        for book in books:
            line = (book.bookName + "  (" + str(book.imgCount) +")").ljust(30) + "#" + book.nid
            self.bookListWidget.addItem(QListWidgetItem(line))
        self.show_status(self.decode_file("加载需要分章的图书数量: %s") % len(books))
    
    @pyqtSignature("")
    def on_saveChapterBtn_clicked(self):
        """保存分章信息"""
        # 保存当前页的分章信息
        res = QMessageBox.question(None, u"确认保存吗？", u"保存之后再修改分章信息会很麻烦。\r\n请确定保存之前的所有分章任务已完成，不会在修改。确认保存吗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if res == QMessageBox.No:
            '''取消的话直接退出'''
            return
        
        self.__deal_now_page_split_chap()
        
        count = self.completeListWidget.count()
        
        if count < 1:
            self.show_status(self.decode_file("没有分章不能保存，请确认分章信息正确后保存，保存好原始分章书籍就没有了。"))
            return
        
        try:
            nid = self.decode_text(self.nidEdit.text())
            book = bookorm.get_book(nid, False)
            chapters = []
            # cinfos 存储章节信息
            cinfos = []
            for i in range(count):
                index_chapname = self.decode_text(self.completeListWidget.item(i).text()).split(self.decode_file("。"))
                cinfos.append((int(index_chapname[1]), str(index_chapname[3])))
                
            # 解析分章信息
            cid = 1
            for i in range(1, count + 1):
                chapter = bookmode.Chapter()
                chapter.author = book.author
                chapter.bookName = book.bookName
                chapter.cid = cid
                cid += 1
                chapter.cTitle = cinfos[i - 1][1]
                if i == count:
                    # 最后一章用书的总数量计算
                    chapter.imgCount = book.imgCount - cinfos[i - 1][0] + 1
                else:
                    chapter.imgCount = cinfos[i][0] - cinfos[i - 1][0]
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
            
            self.__set_save(True)
            self.show_status(self.decode_file("保存分章信息成功：%s %s 章节数： %d") % (nid, book.bookName, len(chapters)))
        except Exception, e:
            print self.decode_file("保存出错了：%s" % str(e))
            self.show_status(self.decode_file("保存出错了：%s" % str(e)))
    
    @pyqtSignature("")
    def on_clearBtn_clicked(self):
        """清除分章"""
        indexs = self.__get_selects_tr_c()
        if indexs == None:
            self.show_status(self.decode_file("请选择一张图片进行操作"))
            return
        
        for (tr, c) in indexs:
            if (tr, c) != (-1, -1):
                index = self.__get_start_index() + self.__get_index(col_num, tr - 1, c)
                item = self.imgTableWidget.item(tr, c)
                item.setText(str(index))
                self.__set_font(item, False)
                # 删除包括界面和内存
                self.__del_split_info(index)
                self.show_status(self.decode_file("清除分章: %s") % str(index))
                self.__set_save(False)
            
            
    @pyqtSignature("")
    def on_upCoverBtn_clicked(self):
        '''修改封面图片'''
        date = self.decode_text(self.createTimeEdit.text())[0:10].replace("-", "")
        nid = self.decode_text(self.nidEdit.text())
        cover_path = day_path % date + "cover/" + nid[0:2] + "/" + nid[2:4] + "/"
        os.startfile(cover_path)

    @pyqtSignature("")
    def on_saveBookInfoBtn_clicked(self):
        """保存书籍信息"""
        try:
            nid = self.decode_text(self.nidEdit.text())
            book = bookorm.get_book(nid, False)
            bookName = self.decode_text(self.bookNameEdit.text())
            if bookName:
                book.bookName = bookName
            author = self.decode_text(self.authorEdit.text())
            if author:
                book.author = author
            btype = self.decode_text(self.typeEdit.text())
            if btype:
                book.type = btype
            desc = self.decode_text(self.descriptionEdit.toPlainText())
            if desc:
                book.description = desc
            book.str()
            # 先删除在插入
            bookorm.save_book(book)
            
            self.show_status(self.decode_file("修改书籍信息成功: %s %s" % (nid, bookName)))
        except Exception, e:
            print self.decode_file("保存出错了：%s" % str(e))
            self.show_status(self.decode_file("保存出错了：%s" % str(e)))
    
    @pyqtSignature("")
    def on_dealCoverBtn_clicked(self):
        """deal书籍信息"""
        try:
            nid = self.decode_text(self.nidEdit.text())
            date = self.decode_text(self.createTimeEdit.text())[0:10].replace("-", "")
            cover_path = day_path % date + "cover/" + nid[0:2] + "/" + nid[2:4] + "/"
            print "cover path:", cover_path
            res = bookcrawl.supply_cover_img(cover_path)
            self.show_status(self.decode_file("处理封面信息" + res))
        except Exception, e:
            self.show_status(self.decode_file("处理封面信息失败：" + str(e)))
    
    @pyqtSignature("")
    def on_refreshCoverBtn_clicked(self):
        """刷新书籍信息"""
        try:
            nid = self.decode_text(self.nidEdit.text())
            book = bookorm.get_book(nid)
            self.__show_bookinfo(book)
        except Exception, e:
            self.show_status(self.decode_file("处理封面信息失败：" + str(e)))
    
    @pyqtSignature("")
    def on_previousBtn_clicked(self):
        """上一页"""
        # 保存当前页的分章信息
        self.__deal_now_page_split_chap()
        nowPage = int(self.decode_text(self.nowPageLabel.text())) - 1
        if nowPage > 0:
            nowPage -= 1
            nid = self.decode_text(self.nidEdit.text())
            book = bookorm.get_book(nid, False)
            self.__show_imgs(book, nowPage)
    
    @pyqtSignature("")
    def on_nextBtn_clicked(self):
        """下一页"""
        # 保存当前页的分章信息
        self.__deal_now_page_split_chap()
        
        allPage = int(self.decode_text(self.allPageLabel.text()))
        nowPage = int(self.decode_text(self.nowPageLabel.text())) - 1
        if nowPage < allPage - 1:
            nowPage += 1
            nid = self.decode_text(self.nidEdit.text())
            book = bookorm.get_book(nid, False)
            self.__show_imgs(book, nowPage)
    
    @pyqtSignature("")
    def on_pageBtn_clicked(self):
        '''指定翻页'''
        try:
            page = int(self.decode_text(self.pageEdit.text()))
            if page < 1 or page > int(self.decode_text(self.allPageLabel.text())):
                self.show_status(self.decode_file("页码超出范围，请输入正确的页码"))
                return
            nid = self.decode_text(self.nidEdit.text())
            book = bookorm.get_book(nid, True)
            # 显示指定页图片数据
            self.__show_imgs(book, page - 1)
        except:
            self.show_status(self.decode_file("输入页码错误，请检查。"))
        
    @pyqtSignature("")
    def on_refreshChapterBtn_clicked(self):
        """刷新章节"""
        self.__deal_now_page_split_chap()
        
    @pyqtSignature("")
    def on_autoSplitBtn_clicked(self):
        """按给定章节数量自动编章"""
        if len(self.split_chap_infos) < 1:
            self.show_status(u"至少有一个分章才能操作。")
            return
        try:
            chap_size = int(self.decode_text(self.chapNumEdit.text()))
            if chap_size < 1 or chap_size > 20:
                self.show_status(u"自动分章数量需在1到20之间， 请重新输入")
                return
        except:
            self.show_status(u"请输入正确的章节数量。")
        
        # 刷新显示分章
        self.__deal_now_page_split_chap()
        
        # 获取书的信息
        book = bookorm.get_book(self.decode_text(self.nidEdit.text()), False)
        
        print "\n".join([ "before split: " + key + " " + str(value) for key, value in self.split_chap_infos.items()])
        
        # 所有的删除的数据
        nones = [(key, value) for key, value in self.split_chap_infos.items() if not value]
        # 按顺序获取每章的图片数
        keys = [int(key) for key in self.split_chap_infos.keys() if self.split_chap_infos[key]]
        keys.sort()
        # chinfo 存储分章信息和章节数量
        chinfo = []
        for i in range(1, len(keys)):
            ki = keys[i - 1]
            c = keys[i] - keys[i - 1]
            cname = self.split_chap_infos[str(keys[i - 1])]
            chinfo.append([ki, c, cname])
        # 对最后一章单独处理
        li = len(keys) - 1
        ki = keys[li]
        c = book.imgCount - keys[li]
        cname = self.split_chap_infos[str(keys[li])]
        chinfo.append([ki, c, cname])
        
        # 新建新对象存储自动分章
        new_chap_infos = {}
        new_chap_infos.update(nones)
        
        for [index, count, value] in chinfo:
            num = (count - 1) / chap_size + 1
            if num == 1:
                new_chap_infos[str(index)] = value
                print "auto split:", index, value
            else:
                for n in range(0, num):
                    k = str(index + n * chap_size)
                    v = u"%s（%d）" % (value, n + 1)
                    new_chap_infos[k] = v
                    print "auto split:", k, v
        
        # 将新对象赋给原始对象
        self.split_chap_infos = new_chap_infos
        self.__set_save(False)
        
        # 添加所有分章信息
        self.__add_all_split_info()
        # 从新显示当前页
        self.__show_imgs(book, int(self.decode_text(self.nowPageLabel.text())) - 1)
    
    @pyqtSignature("QModelIndex")
    def on_bookListWidget_doubleClicked(self, index):
        """选择书"""
        if not self.is_save:
            res = QMessageBox.question(None, u"之前的编辑没保存，确认任何吗？", u"如果不保存，则此次编辑数据将丢失，确认切换到下一本吗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if res == QMessageBox.No:
                return
        
        # 清除上一本书的信息
        self.chapListWidget.clear()
        self.imgTableWidget.clear()
        self.split_chap_infos = {}
        self.completeListWidget.clear()
        self.__set_save(True)
        
        select_nid = self.decode_text(self.bookListWidget.currentItem().text()).split("#")[1]
        self.show_status(self.decode_file("正在加载书籍 %s 的所有章节和图片，这需要一定时间，请稍后。") % select_nid)
        book = bookorm.get_book(select_nid, True)
        chapters = book.chapters
        
        # 最前面加上书籍名称
        self.chapListWidget.addItem(QListWidgetItem(self.decode_file("0。%s#0") % book.bookName.ljust(30)))
        i = 0
        for chap in chapters:
            i += 1
            line = chap.cTitle.ljust(30) + "#" + str(chap.cid)
            self.chapListWidget.addItem(QListWidgetItem(str(i) + self.decode_file("。") + line))
        
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
        indexs = self.__get_selects_tr_c()
        if indexs == None:
            self.show_status(self.decode_file("请选择一张图片进行操作"))
            return
        
        index = self.chapListWidget.currentIndex().row()
        for (tr, c) in indexs:
            if (tr, c) != (-1, -1):
                select_text = self.decode_text(self.chapListWidget.item(index).text())
                chap_name = select_text.split("#")[0].split(self.decode_file("。"))[1].strip()
                
                item = self.imgTableWidget.item(tr, c)
                item.setText(chap_name)
                self.__set_font(item, True)
                self.show_status(self.decode_file("设定分章 %d : %s") % (self.__get_index(col_num, tr, c), chap_name))
                
                start_index = self.__get_start_index()
                self.__add_split_info(start_index + self.__get_index(col_num, tr, c), chap_name)
                self.__set_save(False)
                
                # 依次类推
                index += 1
                if index >= self.chapListWidget.count():
                    self.show_status(u"章节数不够。")
                    break
            
    @pyqtSignature("QModelIndex")
    def on_completeListWidget_doubleClicked(self, index):
        '''双击已添加章节信息，调到指定图片位置'''
        sel_text = self.completeListWidget.item(index.row()).text()
        sel_index = int(sel_text.split(u"。")[1]) - 1
        print u"跳到指定位置 %d" % sel_index
        
        now_page = int(self.nowPageLabel.text()) - 1
        page = sel_index / page_count
        if page != now_page:
            nid = self.nidEdit.text()
            book = bookorm.get_book(nid)
            self.__show_imgs(book, page)
        
        loc = sel_index % page_count
        loc = loc / col_num * 2
        self.__move_table_scroll(loc, self.imgTableWidget.rowCount())
        
    @pyqtSignature("QModelIndex")
    def on_imgTableWidget_doubleClicked(self, index):
        """打开大图"""
        (r, c) = self.__get_current_r_c()
        if (r, c) != (-1, -1) and r % 2 == 0:
            img_path = self.decode_text(self.imgTableWidget.item(r, c).text())
            os.startfile(img_path)
            