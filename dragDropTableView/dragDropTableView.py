#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QMainWindow, QFrame, QTableView, QVBoxLayout, QAbstractItemView, QFileDialog, QAction, QMessageBox
from PyQt5 import QtGui, QtCore
import csv
import shutil
import re
import unicodedata
import pprint
import codecs

class MyTableView(QTableView):

    def __init__(self, main_win=None, parent=None):
        super(MyTableView, self).__init__(parent)
        self.main_win = main_win

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
                    #print(index.data())

                    self.clearSelection()

                    if self.main_win.root_dir is None:
                        QMessageBox.information(self, 'Message', "No valid root directory is set")
                        print('No valid root directory is set')
                        return

                    if not os.path.isdir(self.main_win.root_dir):
                        QMessageBox.information(self, 'Message', "No valid root directory is set")
                        print('No valid root directory is set')
                        return

                    item.setIcon(QtGui.QIcon('checkmark.png'))
                    #self.clearSelection()

                    for col in range(self.model().columnCount()):

                        self.model().item(row, col).setBackground(QtGui.QBrush(QtGui.QColor(128, 218, 112)))

                    

                    new_name = '{} {}'.format(self.model().item(row, 0).text(), self.model().item(row, 1).text())
                    self.main_win.copy_to_folder(links[0],'{}.pdf'.format(new_name))
                    #print(self.main_win)


class MyModel(QtGui.QStandardItemModel):

    def supportedDragActions(self):
        return QtCore.Qt.LinkAction | QtCore.Qt.CopyAction

    def canDropMimeData(self, *args):
        return True

class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.root_dir = None
        #self.root_dir = '/Users/johan/Desktop/apa'
        self.ext = '.pdf'

        #self.resize(300, 400)
        #self.center()
        self.setGeometry(5, 50, 500, 400)
        
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        file_menu = menubar.addMenu('&File')

        open_action = QAction(QtGui.QIcon(self.resource_path('open.png')), '&Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open File')
        open_action.triggered.connect(self.read_csv)
        file_menu.addAction(open_action)

        delete_action = QAction('Delete', self)
        delete_action.triggered.connect(self.delete_selected_rows)
        file_menu.addAction(delete_action)

        set_root_dir_action = QAction('Set Root Directory', self)
        set_root_dir_action.triggered.connect(self.set_root_dir)
        file_menu.addAction(set_root_dir_action)

        match_action = QAction('Match', self)
        match_action.triggered.connect(self.match_files)
        file_menu.addAction(match_action)


        main_frame = QFrame()
        self.setCentralWidget(main_frame)
        vbox = QVBoxLayout(main_frame)

        #self.tableview = QTableView()
        self.tableview = MyTableView(main_win=self)

        self.tableview.setDropIndicatorShown(True)
        self.tableview.setDragEnabled(True)
        self.tableview.setAcceptDrops(True)
        self.tableview.setDragDropMode(QTableView.DragDrop)
        self.tableview.setDefaultDropAction(QtCore.Qt.LinkAction)
        self.tableview.setDropIndicatorShown(True)
        vbox.addWidget(self.tableview)

        self.model = MyModel()
        self.tableview.setModel(self.model)

        self.setWindowTitle('Center')

        #self.read_csv()
        #self.match_files()

        self.show()


    def match_files(self):

        if self.root_dir is None:
            QMessageBox.information(self, 'Message', "No valid root directory is set")
            print('No valid root directory is set')
            return

        if not os.path.isdir(self.root_dir):
            QMessageBox.information(self, 'Message', "No valid root directory is set")
            print('No valid root directory is set')
            return

        file_list = [p for p in os.listdir(self.root_dir) if os.path.isfile(os.path.join(self.root_dir, p)) and os.path.splitext(p)[1] == self.ext]
        
        num_rows = self.model.rowCount()

        match_list = []

        for file in file_list:

            print(file)
            for row in range(num_rows):
                date = self.model.index(row, 0).data()
                desc = unicodedata.normalize('NFC', self.model.index(row, 1).data())

                name = r'{} {}'.format(date, desc)
                
                file_name = unicodedata.normalize('NFC', file)
                
                if file_name.startswith(name):
                    match_list.append(file_name)
                #if re.search(name, file_name):
                    #match_list.append(file_name)

                    for col in range(self.model.columnCount()):
                        self.model.item(row, col).setBackground(QtGui.QBrush(QtGui.QColor(128, 218, 112)))
                    
        pprint.pprint(match_list)



    def set_root_dir(self):
        
        sel_dir = QFileDialog.getExistingDirectory()
        print(sel_dir)
        if sel_dir:
            self.root_dir = sel_dir

    def delete_selected_rows(self):

        reply = QMessageBox.question(self, 'Message', "Delete selected rows?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        selected_indexes =  self.tableview.selectionModel().selectedRows()
 
        sel_rows = []
        for index in selected_indexes:
            sel_rows.append(index.row())

        sel_rows.sort()
        num_rows = len(sel_rows)

        for i in range(num_rows):
            self.model.removeRow(sel_rows[num_rows-i-1])


    def populate_model(self, header_labels, data_list):

        self.model.clear()
        # set the first 3 headers, by slicing the off
        self.model.setHorizontalHeaderLabels(header_labels[:3])

        for row, data in enumerate(data_list):

            date_item = QtGui.QStandardItem(data[0])
            date_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled)
            self.model.setItem(row,0,date_item)

            desc = '{}'.format(unicodedata.normalize('NFC', data[1]))
            desc_item = QtGui.QStandardItem(desc)
            desc_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled)
            self.model.setItem(row,1,desc_item)

            amount_item = QtGui.QStandardItem(data[2])
            amount_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled)
            self.model.setItem(row,2,amount_item)

        self.tableview.horizontalHeader().setStretchLastSection(True)
        self.tableview.resizeColumnsToContents()
        

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


    def center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    

    def copy_to_folder(self, source_file, new_name):

        if self.root_dir is None:
            QMessageBox.information(self, 'Message', "No valid root directory is set")
            print('No valid root directory is set')
            return

        if not os.path.isdir(self.root_dir):
            QMessageBox.information(self, 'Message', "No valid root directory is set")
            print('No valid root directory is set')
            return

        dest_file = os.path.join(self.root_dir, new_name)

        if os.path.isfile(dest_file):
            reply = QMessageBox.question(self, 'Message', "File exists, overwrite?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return

        shutil.copy(source_file, dest_file)

    def read_csv(self):

        file_name, selected_filter = QFileDialog.getOpenFileName(None, 'Load csv file', None, filter='CSV (*.csv)')
        #file_name = '/Users/johan/Desktop/test.csv'

        if file_name:

            data_list = []
            header_list = None

            with open(file_name, encoding='utf-8') as csvfile:    
                dialect = csv.Sniffer().sniff(csvfile.read(1024))
                csvfile.seek(0)
                reader = csv.reader(csvfile, dialect)

                for row_index, row in enumerate(reader):

                    if row_index == 0:
                        header_list = row
                    else:
                        data_list.append(row)

            self.populate_model(header_list, data_list)



if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
    


