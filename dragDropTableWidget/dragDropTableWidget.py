import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5 import QtGui, QtCore

class MyTable(QTableWidget):

    def __init__(self, rows, columns, parent):
        super(MyTable, self).__init__(rows, columns, parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                
                links.append(str(url.toLocalFile()))
                print(links[0])
                index = self.indexAt(event.pos())
                row = index.row()

                for col in range(2):
                    item = self.item(row, col)
                    item.setBackground(QtGui.QBrush(QtGui.QColor(125,125,125)))

                #print(index.data())
                #item = self.itemAt(event.pos())
                #print(item)
                

    def dragMoveEvent(self, event):
        index = self.indexAt(event.pos())
        self.selectRow(index.row())
        event.accept()

class BaseWin(QWidget):
    
    def __init__(self):
        super().__init__()
                
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Icon')
        #self.setWindowIcon(QtGui.QIcon('icon.png'))  

        vbox = QVBoxLayout(self)


        self.table = MyTable(10,2,self)
        self.table.setAcceptDrops(True)
        self.table.setDragEnabled(True)
        self.table.horizontalHeader().setStretchLastSection(True)

        #self.table.setStyleSheet(
        '''QTableView::item:hover { background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #FAFBFE, stop: 1 #DCDEF1);}'''
        #)

        vbox.addWidget(self.table)

        for x in range(10):
            self.table.setItem(x, 0, QTableWidgetItem('Item {}'.format(x)))
            self.table.setItem(x, 1, QTableWidgetItem('Data {}'.format(x)))

        
    

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    win = BaseWin()
    win.show()
    sys.exit(app.exec_())  