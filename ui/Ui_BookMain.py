# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\eclipse4.2\BookClient\BookMain.ui'
#
# Created: Tue Jul 30 17:00:49 2013
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
        MainWindow.resize(930, 799)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.splitter = QtGui.QSplitter(self.centralWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pBtn1 = QtGui.QPushButton(self.widget)
        self.pBtn1.setObjectName(_fromUtf8("pBtn1"))
        self.horizontalLayout.addWidget(self.pBtn1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.bookListWidget = QtGui.QListWidget(self.widget)
        self.bookListWidget.setBaseSize(QtCore.QSize(60, 0))
        self.bookListWidget.setObjectName(_fromUtf8("bookListWidget"))
        self.verticalLayout.addWidget(self.bookListWidget)
        self.widget1 = QtGui.QWidget(self.splitter)
        self.widget1.setObjectName(_fromUtf8("widget1"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget1)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pBtn2 = QtGui.QPushButton(self.widget1)
        self.pBtn2.setObjectName(_fromUtf8("pBtn2"))
        self.horizontalLayout_2.addWidget(self.pBtn2)
        self.pBtn3 = QtGui.QPushButton(self.widget1)
        self.pBtn3.setObjectName(_fromUtf8("pBtn3"))
        self.horizontalLayout_2.addWidget(self.pBtn3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.chapListWidget = QtGui.QListWidget(self.widget1)
        self.chapListWidget.setBaseSize(QtCore.QSize(60, 0))
        self.chapListWidget.setObjectName(_fromUtf8("chapListWidget"))
        self.verticalLayout_2.addWidget(self.chapListWidget)
        self.imgTableWidget = QtGui.QTableWidget(self.splitter)
        self.imgTableWidget.setBaseSize(QtCore.QSize(500, 0))
        self.imgTableWidget.setObjectName(_fromUtf8("imgTableWidget"))
        self.imgTableWidget.setColumnCount(0)
        self.imgTableWidget.setRowCount(0)
        self.verticalLayout_3.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pBtn1.setText(_translate("MainWindow", "Refresh", None))
        self.pBtn2.setText(_translate("MainWindow", "Save", None))
        self.pBtn3.setText(_translate("MainWindow", "Clear", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

