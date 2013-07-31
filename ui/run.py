# coding=utf-8
from PyQt4 import QtGui
import BookMain

if __name__ == "__main__":
    print "正在启动，请稍后。。".decode("utf-8")
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = BookMain.BookMain()
    ui.show()
    print "启动成功".decode("utf-8")
    sys.exit(app.exec_())
