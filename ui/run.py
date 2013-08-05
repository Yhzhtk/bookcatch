# coding=utf-8
from PyQt4 import QtGui
import BookMain


if __name__ == "__main__":
    # 设置默认编码
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    
    print u"正在启动，请稍后。。"
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = BookMain.BookMain()
    ui.show()
    print u"启动成功"
    sys.exit(app.exec_())
