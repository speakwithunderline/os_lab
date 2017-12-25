# -*- coding: utf-8 -*-
__author__ = "gwyang@yahoo.com"

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal, QThreadPool, QRunnable

import time

from wfm_ui import *
# import wfm

class WFMShelf(QMainWindow, Ui_WFM):

    def __init(self, title="", content="", *args, **kwargs):
        super(WFMs, self).__init__(*args, **kwargs)
        self.selectedFile = None
        self.activated = False
        self.setupUi(self)
        self.setTitle(title).setContent(content)

    def set_file_list(self):
        # TODO files = wfm.get_file_list()
        files = [
            ['f1.py', u'未下载', '3.3KB', '2017-01-01'],
            ['f1.cpp', u'未下载', '2.7KB', '2017-02-01']
        ]
        for item in files:
            curItem = QtWidgets.QTreeWidgetItem(self.fileList)
            curItem.setText(0, item[0])
            curItem.setText(1, item[1])
            curItem.setText(2, item[2])
            curItem.setText(3, item[3])
            self.fileList.addTopLevelItem(curItem)

    def set_server_list(self):
        servers = ['192.168.0.1', '192.168.1.182', '202.118.228.101']
        for item in servers:
            self.serverList.addItem(item)

    def setTitle(self, title):
        if title:
            self.labelTitle.setText(title)
        return self

    def setContent(self, content):
        if content:
            self.labelContent.setText(content)
        return self

    def change_file_item(self, item, num):
        self.selectedFile = item

    def file_download(self):
        if self.selectedFile is not None:
            fileName =  self.selectedFile.text(0)
            fileStatus = self.selectedFile.text(1)
            if fileStatus == u"已下载":
                self.statusBar().showMessage('Downloaded!')
            elif not self.activated:
                self.activated = True
                # TODO status = wfm.file_download(text)
                thd = DownloadTask(self, self.selectedFile)
                QThreadPool.globalInstance().start(thd)
                self.statusBar().showMessage('Downloading')

    def download_succeed(self, item, status={'msg': 'succeed'}):
        if status['msg'] == 'succeed':
            # item = status['file_status']
            item.setText(1, u'已下载')
            
            self.statusBar().showMessage('Succeed')
        else:
            self.statusBar().showMessage(status['msg'])

        self.activated = False

    def file_export(self):
        if self.selectedFile is not None:
            fileName =  self.selectedFile.text(0)
            fileStatus = self.selectedFile.text(1)

            if fileStatus == u"已下载":
                file_path, ok2 = QFileDialog.getSaveFileName(self,
                                                             "文件保存",
                                                             "~",
                                                             "All Files (*)")
                # wfm.export(fileName, file_path)
                self.statusBar().showMessage(file_path)
            else:
                self.statusBar().showMessage('not downloaded')

    def file_upload(self, a):
        text = self.filePath.text()
        self.statusBar().showMessage('uploading '+ text)

        if not self.activated:
            self.activated = True
            # TODO status = wfm.file_upload(text)
            thd = UploadTask(self)
            QThreadPool.globalInstance().start(thd)

    def upload_succeed(self, status = {'msg': 'succeed', 'file_status': ['cc', 'dd', 'ee', 'ff']}):
        if status['msg'] == 'succeed':
            item = status['file_status']
            curItem = QtWidgets.QTreeWidgetItem(self.fileList)
            curItem.setText(0, item[0])
            curItem.setText(1, item[1])
            curItem.setText(2, item[2])
            curItem.setText(3, item[3])
            self.fileList.addTopLevelItem(curItem)
            self.statusBar().showMessage('Accepted')
        else:
            self.statusBar().showMessage(status['msg'])

        self.activated = False

    def file_select(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,
                                    "选取文件",
                                    "~",
                                    "All Files (*);;Text Files (*.txt)")
        self.filePath.setText(fileName1)

class UploadTask(QRunnable):
    def __init__(self, wmf):
        super(QRunnable,self).__init__()
        self.wmf = wmf
    def run(self):
        time.sleep(5)
        self.wmf.upload_succeed()

class DownloadTask(QRunnable):
    def __init__(self, wmf, item):
        super(QRunnable, self).__init__()
        self.wmf = wmf
        self.item = item
    def run(self):
        time.sleep(5)
        self.wmf.download_succeed(self.item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wfm_shelf = WFMShelf()
    #wfm.setupUi(mainWindow)
    wfm_shelf.setupUi(wfm_shelf)
    wfm_shelf.show()
    # mainWindow.show()
    sys.exit(app.exec_())
