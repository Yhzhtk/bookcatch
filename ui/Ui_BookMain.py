# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\eclipse4.2\BookClient\BookMain.ui'
#
# Created: Wed Aug 21 15:16:09 2013
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(934, 799)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.splitter_2 = QtGui.QSplitter(self.centralWidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.layoutWidget = QtGui.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.booksLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.booksLayout.setMargin(0)
        self.booksLayout.setObjectName(_fromUtf8("booksLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.refreshBookBtn = QtGui.QPushButton(self.layoutWidget)
        self.refreshBookBtn.setObjectName(_fromUtf8("refreshBookBtn"))
        self.horizontalLayout.addWidget(self.refreshBookBtn)
        self.booksLayout.addLayout(self.horizontalLayout)
        self.bookListWidget = QtGui.QListWidget(self.layoutWidget)
        self.bookListWidget.setBaseSize(QtCore.QSize(60, 0))
        self.bookListWidget.setObjectName(_fromUtf8("bookListWidget"))
        self.booksLayout.addWidget(self.bookListWidget)
        self.widget = QtGui.QWidget(self.splitter_2)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_15 = QtGui.QHBoxLayout()
        self.horizontalLayout_15.setObjectName(_fromUtf8("horizontalLayout_15"))
        self.saveBookInfoBtn = QtGui.QPushButton(self.widget)
        self.saveBookInfoBtn.setObjectName(_fromUtf8("saveBookInfoBtn"))
        self.horizontalLayout_15.addWidget(self.saveBookInfoBtn)
        self.refreshCoverBtn = QtGui.QPushButton(self.widget)
        self.refreshCoverBtn.setObjectName(_fromUtf8("refreshCoverBtn"))
        self.horizontalLayout_15.addWidget(self.refreshCoverBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_15)
        self.coverImgLabel = QtGui.QLabel(self.widget)
        self.coverImgLabel.setObjectName(_fromUtf8("coverImgLabel"))
        self.verticalLayout.addWidget(self.coverImgLabel)
        self.horizontalLayout_14 = QtGui.QHBoxLayout()
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        self.upCoverBtn = QtGui.QPushButton(self.widget)
        self.upCoverBtn.setObjectName(_fromUtf8("upCoverBtn"))
        self.horizontalLayout_14.addWidget(self.upCoverBtn)
        self.dealCoverBtn = QtGui.QPushButton(self.widget)
        self.dealCoverBtn.setObjectName(_fromUtf8("dealCoverBtn"))
        self.horizontalLayout_14.addWidget(self.dealCoverBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.label_6 = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_8.addWidget(self.label_6)
        self.nidEdit = QtGui.QLineEdit(self.widget)
        self.nidEdit.setObjectName(_fromUtf8("nidEdit"))
        self.horizontalLayout_8.addWidget(self.nidEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.bookNameEdit = QtGui.QLineEdit(self.widget)
        self.bookNameEdit.setObjectName(_fromUtf8("bookNameEdit"))
        self.horizontalLayout_3.addWidget(self.bookNameEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_2 = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_4.addWidget(self.label_2)
        self.authorEdit = QtGui.QLineEdit(self.widget)
        self.authorEdit.setObjectName(_fromUtf8("authorEdit"))
        self.horizontalLayout_4.addWidget(self.authorEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_3 = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_5.addWidget(self.label_3)
        self.typeEdit = QtGui.QLineEdit(self.widget)
        self.typeEdit.setObjectName(_fromUtf8("typeEdit"))
        self.horizontalLayout_5.addWidget(self.typeEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_4 = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_6.addWidget(self.label_4)
        self.createTimeEdit = QtGui.QLineEdit(self.widget)
        self.createTimeEdit.setObjectName(_fromUtf8("createTimeEdit"))
        self.horizontalLayout_6.addWidget(self.createTimeEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_5 = QtGui.QLabel(self.widget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_7.addWidget(self.label_5)
        self.descriptionEdit = QtGui.QTextEdit(self.widget)
        self.descriptionEdit.setObjectName(_fromUtf8("descriptionEdit"))
        self.horizontalLayout_7.addWidget(self.descriptionEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.layoutWidget1 = QtGui.QWidget(self.splitter_2)
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.saveChapterBtn = QtGui.QPushButton(self.layoutWidget1)
        self.saveChapterBtn.setObjectName(_fromUtf8("saveChapterBtn"))
        self.horizontalLayout_2.addWidget(self.saveChapterBtn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.label_7 = QtGui.QLabel(self.layoutWidget1)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_9.addWidget(self.label_7)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.nowPageLabel = QtGui.QLabel(self.layoutWidget1)
        self.nowPageLabel.setObjectName(_fromUtf8("nowPageLabel"))
        self.verticalLayout_2.addWidget(self.nowPageLabel)
        self.allPageLabel = QtGui.QLabel(self.layoutWidget1)
        self.allPageLabel.setObjectName(_fromUtf8("allPageLabel"))
        self.verticalLayout_2.addWidget(self.allPageLabel)
        self.horizontalLayout_9.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.pageEdit = QtGui.QLineEdit(self.layoutWidget1)
        self.pageEdit.setObjectName(_fromUtf8("pageEdit"))
        self.horizontalLayout_11.addWidget(self.pageEdit)
        self.pageBtn = QtGui.QPushButton(self.layoutWidget1)
        self.pageBtn.setObjectName(_fromUtf8("pageBtn"))
        self.horizontalLayout_11.addWidget(self.pageBtn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.previousBtn = QtGui.QPushButton(self.layoutWidget1)
        self.previousBtn.setObjectName(_fromUtf8("previousBtn"))
        self.horizontalLayout_10.addWidget(self.previousBtn)
        self.nextBtn = QtGui.QPushButton(self.layoutWidget1)
        self.nextBtn.setObjectName(_fromUtf8("nextBtn"))
        self.horizontalLayout_10.addWidget(self.nextBtn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.refreshChapterBtn = QtGui.QPushButton(self.layoutWidget1)
        self.refreshChapterBtn.setObjectName(_fromUtf8("refreshChapterBtn"))
        self.horizontalLayout_12.addWidget(self.refreshChapterBtn)
        self.clearBtn = QtGui.QPushButton(self.layoutWidget1)
        self.clearBtn.setObjectName(_fromUtf8("clearBtn"))
        self.horizontalLayout_12.addWidget(self.clearBtn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.chapNumEdit = QtGui.QLineEdit(self.layoutWidget1)
        self.chapNumEdit.setObjectName(_fromUtf8("chapNumEdit"))
        self.horizontalLayout_13.addWidget(self.chapNumEdit)
        self.autoSplitBtn = QtGui.QPushButton(self.layoutWidget1)
        self.autoSplitBtn.setObjectName(_fromUtf8("autoSplitBtn"))
        self.horizontalLayout_13.addWidget(self.autoSplitBtn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_13)
        self.splitter = QtGui.QSplitter(self.layoutWidget1)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.completeListWidget = QtGui.QListWidget(self.splitter)
        self.completeListWidget.setObjectName(_fromUtf8("completeListWidget"))
        self.chapListWidget = QtGui.QListWidget(self.splitter)
        self.chapListWidget.setBaseSize(QtCore.QSize(60, 0))
        self.chapListWidget.setObjectName(_fromUtf8("chapListWidget"))
        self.verticalLayout_3.addWidget(self.splitter)
        self.imgTableWidget = QtGui.QTableWidget(self.splitter_2)
        self.imgTableWidget.setBaseSize(QtCore.QSize(500, 0))
        self.imgTableWidget.setObjectName(_fromUtf8("imgTableWidget"))
        self.imgTableWidget.setColumnCount(0)
        self.imgTableWidget.setRowCount(0)
        self.verticalLayout_4.addWidget(self.splitter_2)
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "ChapterSplit - Bookshot", None))
        self.refreshBookBtn.setText(_translate("MainWindow", "Refresh Book", None))
        self.saveBookInfoBtn.setText(_translate("MainWindow", "Save Book Info", None))
        self.refreshCoverBtn.setText(_translate("MainWindow", "Refresh Book", None))
        self.coverImgLabel.setText(_translate("MainWindow", "TextLabel", None))
        self.upCoverBtn.setText(_translate("MainWindow", "Update Cover", None))
        self.dealCoverBtn.setText(_translate("MainWindow", "Deal Cover", None))
        self.label_6.setText(_translate("MainWindow", "nid", None))
        self.label.setText(_translate("MainWindow", "bookName", None))
        self.label_2.setText(_translate("MainWindow", "author", None))
        self.label_3.setText(_translate("MainWindow", "type", None))
        self.label_4.setText(_translate("MainWindow", "createTime", None))
        self.label_5.setText(_translate("MainWindow", "desc", None))
        self.saveChapterBtn.setText(_translate("MainWindow", "Save Chapter Info", None))
        self.label_7.setText(_translate("MainWindow", "Page Now/All", None))
        self.nowPageLabel.setText(_translate("MainWindow", "0", None))
        self.allPageLabel.setText(_translate("MainWindow", "0", None))
        self.pageEdit.setText(_translate("MainWindow", "1", None))
        self.pageBtn.setText(_translate("MainWindow", "Go", None))
        self.previousBtn.setText(_translate("MainWindow", "Previous", None))
        self.nextBtn.setText(_translate("MainWindow", " Next", None))
        self.refreshChapterBtn.setText(_translate("MainWindow", "Refresh Page", None))
        self.clearBtn.setText(_translate("MainWindow", "Clear", None))
        self.chapNumEdit.setText(_translate("MainWindow", "12", None))
        self.autoSplitBtn.setText(_translate("MainWindow", "AutoSplit", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

