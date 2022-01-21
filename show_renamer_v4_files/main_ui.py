# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(387, 520)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(387, 520))
        MainWindow.setMaximumSize(QtCore.QSize(387, 520))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(11)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setGeometry(QtCore.QRect(30, 20, 321, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(28)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("")
        self.title_label.setObjectName("title_label")
        self.Internet_rdobtn = QtWidgets.QRadioButton(self.centralwidget)
        self.Internet_rdobtn.setGeometry(QtCore.QRect(20, 110, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(11)
        self.Internet_rdobtn.setFont(font)
        self.Internet_rdobtn.setChecked(True)
        self.Internet_rdobtn.setObjectName("Internet_rdobtn")
        self.method_label = QtWidgets.QLabel(self.centralwidget)
        self.method_label.setGeometry(QtCore.QRect(20, 90, 61, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.method_label.setFont(font)
        self.method_label.setObjectName("method_label")
        self.reformat_rdobtn = QtWidgets.QRadioButton(self.centralwidget)
        self.reformat_rdobtn.setGeometry(QtCore.QRect(20, 140, 231, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(11)
        self.reformat_rdobtn.setFont(font)
        self.reformat_rdobtn.setChecked(False)
        self.reformat_rdobtn.setObjectName("reformat_rdobtn")
        self.reformat2_rdobtn = QtWidgets.QRadioButton(self.centralwidget)
        self.reformat2_rdobtn.setGeometry(QtCore.QRect(20, 170, 361, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(11)
        self.reformat2_rdobtn.setFont(font)
        self.reformat2_rdobtn.setChecked(False)
        self.reformat2_rdobtn.setObjectName("reformat2_rdobtn")
        self.directory_label = QtWidgets.QLabel(self.centralwidget)
        self.directory_label.setGeometry(QtCore.QRect(20, 210, 161, 21))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.directory_label.setFont(font)
        self.directory_label.setObjectName("directory_label")
        self.directory_textedit = QtWidgets.QTextEdit(self.centralwidget)
        self.directory_textedit.setGeometry(QtCore.QRect(20, 240, 251, 22))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(11)
        self.directory_textedit.setFont(font)
        self.directory_textedit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.directory_textedit.setObjectName("directory_textedit")
        self.episodes_preceeding_label = QtWidgets.QLabel(self.centralwidget)
        self.episodes_preceeding_label.setGeometry(QtCore.QRect(20, 280, 311, 21))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.episodes_preceeding_label.setFont(font)
        self.episodes_preceeding_label.setObjectName("episodes_preceeding_label")
        self.episode_text = QtWidgets.QTextEdit(self.centralwidget)
        self.episode_text.setGeometry(QtCore.QRect(20, 310, 351, 22))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(11)
        self.episode_text.setFont(font)
        self.episode_text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.episode_text.setObjectName("episode_text")
        self.renameShows_btn = QtWidgets.QPushButton(self.centralwidget)
        self.renameShows_btn.setGeometry(QtCore.QRect(200, 430, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(11)
        self.renameShows_btn.setFont(font)
        self.renameShows_btn.setObjectName("renameShows_btn")
        self.author_label = QtWidgets.QLabel(self.centralwidget)
        self.author_label.setGeometry(QtCore.QRect(170, 60, 181, 20))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(11)
        font.setItalic(True)
        self.author_label.setFont(font)
        self.author_label.setObjectName("author_label")
        self.browse_btn = QtWidgets.QPushButton(self.centralwidget)
        self.browse_btn.setGeometry(QtCore.QRect(280, 239, 91, 24))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(10)
        self.browse_btn.setFont(font)
        self.browse_btn.setObjectName("browse_btn")
        self.Show_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.Show_comboBox.setGeometry(QtCore.QRect(20, 380, 351, 22))
        self.Show_comboBox.setEditable(False)
        self.Show_comboBox.setCurrentText("")
        self.Show_comboBox.setObjectName("Show_comboBox")
        self.show_select_label = QtWidgets.QLabel(self.centralwidget)
        self.show_select_label.setGeometry(QtCore.QRect(20, 350, 291, 21))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.show_select_label.setFont(font)
        self.show_select_label.setObjectName("show_select_label")
        self.confirmation_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.confirmation_checkBox.setGeometry(QtCore.QRect(20, 410, 181, 21))
        self.confirmation_checkBox.setObjectName("confirmation_checkBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 387, 22))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuChange_theme = QtWidgets.QMenu(self.menuMenu)
        self.menuChange_theme.setObjectName("menuChange_theme")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionLight_theme = QtWidgets.QAction(MainWindow)
        self.actionLight_theme.setObjectName("actionLight_theme")
        self.actionDark_theme = QtWidgets.QAction(MainWindow)
        self.actionDark_theme.setObjectName("actionDark_theme")
        self.actionClassic_theme = QtWidgets.QAction(MainWindow)
        self.actionClassic_theme.setObjectName("actionClassic_theme")
        self.menuChange_theme.addAction(self.actionClassic_theme)
        self.menuChange_theme.addAction(self.actionLight_theme)
        self.menuChange_theme.addAction(self.actionDark_theme)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionAbout)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.menuChange_theme.menuAction())
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionClose)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TV Show Renamer"))
        self.title_label.setText(_translate("MainWindow", "TV Show Renamer"))
        self.Internet_rdobtn.setText(_translate("MainWindow", "Retrieve from Internet"))
        self.method_label.setText(_translate("MainWindow", "Method"))
        self.reformat_rdobtn.setText(_translate("MainWindow", "Reformat Names - Ep_No.Ep_Name"))
        self.reformat2_rdobtn.setText(_translate("MainWindow", "Retrieve from Internet - Series - [SxEE] - Ep_Name"))
        self.directory_label.setText(_translate("MainWindow", "Select Directory"))
        self.episodes_preceeding_label.setText(_translate("MainWindow", "Number of episodes in the preceding Season"))
        self.renameShows_btn.setText(_translate("MainWindow", "Rename Shows"))
        self.author_label.setText(_translate("MainWindow", "Developed by Thomas Alex"))
        self.browse_btn.setText(_translate("MainWindow", "Browse"))
        self.show_select_label.setText(_translate("MainWindow", "Select TV Shows from The Show List"))
        self.confirmation_checkBox.setText(_translate("MainWindow", "Require Confirmation"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.menuChange_theme.setTitle(_translate("MainWindow", "Change theme"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionLight_theme.setText(_translate("MainWindow", "Light theme"))
        self.actionDark_theme.setText(_translate("MainWindow", "Dark theme"))
        self.actionClassic_theme.setText(_translate("MainWindow", "Classic theme"))
