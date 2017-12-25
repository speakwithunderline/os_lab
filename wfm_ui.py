# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wfm.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WFM(object):
    def setupUi(self, WFM):
        WFM.setObjectName("WFM")
        WFM.resize(896, 525)
        self.centralwidget = QtWidgets.QWidget(WFM)
        self.centralwidget.setObjectName("centralwidget")
        self.download = QtWidgets.QPushButton(self.centralwidget)
        self.download.setGeometry(QtCore.QRect(420, 360, 91, 41))
        self.download.setObjectName("download")
        self.fileExport = QtWidgets.QPushButton(self.centralwidget)
        self.fileExport.setGeometry(QtCore.QRect(510, 360, 91, 41))
        self.fileExport.setObjectName("fileExport")
        self.fileList = QtWidgets.QTreeWidget(self.centralwidget)
        self.fileList.setGeometry(QtCore.QRect(0, 10, 601, 341))
        self.fileList.setObjectName("fileList")
        self.fileUpload = QtWidgets.QPushButton(self.centralwidget)
        self.fileUpload.setGeometry(QtCore.QRect(490, 420, 111, 41))
        self.fileUpload.setObjectName("fileUpload")
        self.filePath = QtWidgets.QLineEdit(self.centralwidget)
        self.filePath.setGeometry(QtCore.QRect(0, 420, 451, 41))
        self.filePath.setObjectName("filePath")
        self.addFile = QtWidgets.QPushButton(self.centralwidget)
        self.addFile.setGeometry(QtCore.QRect(450, 420, 41, 41))
        self.addFile.setObjectName("addFile")
        self.serverList = QtWidgets.QListWidget(self.centralwidget)
        self.serverList.setGeometry(QtCore.QRect(640, 10, 241, 451))
        self.serverList.setObjectName("serverList")
        # self.downloadProgress = QtWidgets.QProgressBar(self.centralwidget)
        # self.downloadProgress.setGeometry(QtCore.QRect(30, 370, 361, 23))
        # self.downloadProgress.setProperty("value", 24)
        # self.downloadProgress.setObjectName("downloadProgress")
        WFM.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(WFM)
        self.statusbar.setObjectName("statusbar")
        WFM.setStatusBar(self.statusbar)

        self.set_file_list()
        self.set_server_list()
        self.selectedFile = None
        self.activated = False

        self.retranslateUi(WFM)
        self.download.clicked.connect(WFM.file_download)
        self.fileExport.clicked.connect(WFM.file_export)
        self.addFile.clicked.connect(WFM.file_select)
        self.fileUpload.clicked.connect(WFM.file_upload)
        self.fileList.itemActivated['QTreeWidgetItem*','int'].connect(self.change_file_item)
        QtCore.QMetaObject.connectSlotsByName(WFM)

    def retranslateUi(self, WFM):
        _translate = QtCore.QCoreApplication.translate
        WFM.setWindowTitle(_translate("WFM", "MainWindow"))
        self.download.setText(_translate("WFM", "下载"))
        self.fileExport.setText(_translate("WFM", "导出"))
        self.fileList.headerItem().setText(0, _translate("WFM", "名称"))
        self.fileList.headerItem().setText(1, _translate("WFM", "已下载"))
        self.fileList.headerItem().setText(2, _translate("WFM", "大小"))
        self.fileList.headerItem().setText(3, _translate("WFM", "日期"))
        self.fileUpload.setText(_translate("WFM", "上传"))
        self.addFile.setText(_translate("WFM", "+"))

