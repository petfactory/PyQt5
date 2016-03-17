import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5 import QtGui, QtCore


class Button(QPushButton):
  
    def __init__(self, title, parent):
        super(Button, self).__init__(title, parent)
        
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        #if e.mimeData().hasFormat('text/plain'):
        #    e.accept()
        #else:
        #    e.ignore()
        event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                
                links.append(str(url.toLocalFile()))
                print(links[0])

        else:
            event.ignore()


class BaseWin(QWidget):
    
    def __init__(self):
        super().__init__()
                
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Icon')
        #self.setWindowIcon(QtGui.QIcon('icon.png'))  

        vbox = QVBoxLayout(self)
        #button = QPushButton('Button')
        button = Button('Test', self)
        vbox.addWidget(button)
    

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    win = BaseWin()
    win.show()
    sys.exit(app.exec_())  