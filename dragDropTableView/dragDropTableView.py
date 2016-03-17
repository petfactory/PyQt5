import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTreeView, QTableWidget, QTableWidgetItem
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
                #print(event.pos())
                index = self.indexAt(event.pos())
                print(index.data())

    def dragMoveEvent(self, event):
        event.accept()

class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self):
        QtCore.QAbstractItemModel.__init__(self)
        self.nodes = ['node0', 'node1', 'node2']

    def index(self, row, column, parent):
        return self.createIndex(row, column, self.nodes[row])

    def parent(self, index):
        return QtCore.QModelIndex()

    def rowCount(self, index):
        if index.internalPointer() in self.nodes:
            return 0
        return len(self.nodes)

    def columnCount(self, index):
        return 1

    def data(self, index, role):
        if role == 0: 
            return index.internalPointer()
        else:
            return None

    def supportedDropActions(self): 
        return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction         

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | \
               QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled        

    def mimeTypes(self):
        return ['text/xml']

    def mimeData(self, indexes):
        mimedata = QtCore.QMimeData()
        mimedata.setData('text/xml', 'mimeData')
        return mimedata

    def dropMimeData(self, data, action, row, column, parent):
        print('dropMimeData %s %s %s %s' % (data.data('text/xml'), action, row, parent))
        return True



class BaseWin(QWidget):
    
    def __init__(self):
        super().__init__()
                
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Icon')
        #self.setWindowIcon(QtGui.QIcon('icon.png'))  

        vbox = QVBoxLayout(self)

        self.model = TreeModel()
        self.view = QTreeView()

        self.view.setModel(self.model)
        vbox.addWidget(self.view)
        self.view.setAcceptDrops(True)


        
    

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    win = BaseWin()
    win.show()
    sys.exit(app.exec_())  