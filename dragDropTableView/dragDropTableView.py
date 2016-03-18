#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QMainWindow, QFrame, QTableView, QVBoxLayout, QAbstractItemView
from PyQt5 import QtGui, QtCore


class MyTableView(QTableView):

    def dragMoveEvent(self, event):
        index = self.indexAt(event.pos())
        self.selectRow(index.row())
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
                    if not index.isValid():
                        return

                    row = index.row()
                    item = self.model().item(row, 0)
                    print(index.data())


                    item.setIcon(QtGui.QIcon('checkmark.png'))
                    #self.clearSelection()

                    for col in range(self.model().columnCount()):

                        self.model().item(row, col).setBackground(QtGui.QBrush(QtGui.QColor(128, 218, 112)))

                    self.clearSelection()

                    #new_name = '{}_{}'.format(self.item(row, 0).text(), self.item(row, 1).text())
                    #copy_to_folder(links[0], self.root_dir, '{}.pdf'.format(new_name))


class MyModel(QtGui.QStandardItemModel):

    def supportedDragActions(self):
        return Qt.LinkAction | Qt.CopyAction

    def canDropMimeData(self, *args):
        return True

class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        #self.resize(300, 400)
        #self.center()
        self.setGeometry(200, 200, 300, 400)
        
        
        main_frame = QFrame()
        self.setCentralWidget(main_frame)
        vbox = QVBoxLayout(main_frame)

        #self.tableview = QTableView()
        self.tableview = MyTableView()
        self.tableview.setDropIndicatorShown(True)
        self.tableview.setDragEnabled(True)
        self.tableview.setAcceptDrops(True)
        self.tableview.setDragDropMode(QTableView.DragDrop)
        self.tableview.setDefaultDropAction(QtCore.Qt.LinkAction)
        self.tableview.setDropIndicatorShown(True)


        vbox.addWidget(self.tableview)

        #self.model = QtGui.QStandardItemModel()
        self.model = MyModel()
        self.tableview.setModel(self.model)

        for i in range(10):
        
            item = QtGui.QStandardItem('Item {}'.format(i))
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled)
            self.model.setItem(i,0,item)

            item = QtGui.QStandardItem('Some info {}'.format(i))
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled)
            self.model.setItem(i,1,item)


        self.setWindowTitle('Center')    
        self.show()
        
        
    def center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_()) 