import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5 import QtGui, QtCore

class MyTable(QTableWidget):

    def __init__(self, rows, columns, parent):
        super(MyTable, self).__init__(rows, columns, parent)
        self.setAcceptDrops(True)
        self.root_dir = '/Users/johan/Desktop/apa'

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

                new_name = '{}_{}'.format(self.item(row, 0).text(), self.item(row, 1).text())
                copy_to_folder(links[0], self.root_dir, '{}.pdf'.format(new_name))
                

    def dragMoveEvent(self, event):
        index = self.indexAt(event.pos())
        self.selectRow(index.row())
        event.accept()

def copy_to_folder(source_file, root_dir, new_name):

    dest_file = os.path.join(root_dir, new_name)

    if os.path.isfile(dest_file):
        print('File exists. Overwrite?')

    shutil.copy(source_file, dest_file)

class BaseWin(QWidget):
    
    def __init__(self):
        super().__init__()
        
        #self.root_dir = '/Users/johan/Desktop/apa'

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

        for x in range(9):
            self.table.setItem(x, 0, QTableWidgetItem('2015 12 0{}'.format(x)))
            self.table.setItem(x, 1, QTableWidgetItem('Apple invoice {}'.format(x)))

        
    

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    win = BaseWin()
    win.show()
    sys.exit(app.exec_())  