from PyQt4 import QtGui
import BookMain

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = BookMain.BookMain()
    ui.show()
    sys.exit(app.exec_())
