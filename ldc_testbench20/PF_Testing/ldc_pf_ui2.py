# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ldc_ccup_pf.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1009, 784)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame_Testing = QtWidgets.QFrame(self.centralwidget)
        self.frame_Testing.setEnabled(False)
        self.frame_Testing.setGeometry(QtCore.QRect(70, 230, 871, 501))
        self.frame_Testing.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_Testing.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_Testing.setObjectName("frame_Testing")
        self.textBrowser = QtWidgets.QTextBrowser(self.frame_Testing)
        self.textBrowser.setGeometry(QtCore.QRect(130, 30, 631, 201))
        self.textBrowser.setObjectName("textBrowser")
        self.frame = QtWidgets.QFrame(self.frame_Testing)
        self.frame.setGeometry(QtCore.QRect(390, 260, 441, 141))
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pb_logpres = QtWidgets.QPushButton(self.frame)
        self.pb_logpres.setGeometry(QtCore.QRect(150, 100, 141, 41))
        self.pb_logpres.setObjectName("pb_logpres")
        self.layoutWidget = QtWidgets.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 441, 71))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.lcdNumber_minpres = QtWidgets.QLCDNumber(self.layoutWidget)
        self.lcdNumber_minpres.setObjectName("lcdNumber_minpres")
        self.verticalLayout_2.addWidget(self.lcdNumber_minpres)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.lcdNumber_maxpres = QtWidgets.QLCDNumber(self.layoutWidget)
        self.lcdNumber_maxpres.setObjectName("lcdNumber_maxpres")
        self.verticalLayout_3.addWidget(self.lcdNumber_maxpres)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_4.addWidget(self.label_5)
        self.lcdNumber_abspres = QtWidgets.QLCDNumber(self.layoutWidget)
        self.lcdNumber_abspres.setObjectName("lcdNumber_abspres")
        self.verticalLayout_4.addWidget(self.lcdNumber_abspres)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.frame_3 = QtWidgets.QFrame(self.frame_Testing)
        self.frame_3.setGeometry(QtCore.QRect(39, 260, 171, 141))
        self.frame_3.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label_8 = QtWidgets.QLabel(self.frame_3)
        self.label_8.setGeometry(QtCore.QRect(10, 50, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.spinBox_testlevel = QtWidgets.QSpinBox(self.frame_3)
        self.spinBox_testlevel.setGeometry(QtCore.QRect(110, 50, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.spinBox_testlevel.setFont(font)
        self.spinBox_testlevel.setObjectName("spinBox_testlevel")
        self.frame_2 = QtWidgets.QFrame(self.frame_Testing)
        self.frame_2.setGeometry(QtCore.QRect(219, 260, 161, 141))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.pb_logfreq = QtWidgets.QPushButton(self.frame_2)
        self.pb_logfreq.setGeometry(QtCore.QRect(10, 100, 141, 41))
        self.pb_logfreq.setObjectName("pb_logfreq")
        self.layoutWidget1 = QtWidgets.QWidget(self.frame_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 0, 141, 71))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_5.addWidget(self.label_6)
        self.lcdNumber_avgfreq = QtWidgets.QLCDNumber(self.layoutWidget1)
        self.lcdNumber_avgfreq.setObjectName("lcdNumber_avgfreq")
        self.verticalLayout_5.addWidget(self.lcdNumber_avgfreq)
        self.label_teststatus = QtWidgets.QLabel(self.frame_Testing)
        self.label_teststatus.setEnabled(False)
        self.label_teststatus.setGeometry(QtCore.QRect(10, 0, 101, 21))
        self.label_teststatus.setObjectName("label_teststatus")
        self.pb_logandinc = QtWidgets.QPushButton(self.frame_Testing)
        self.pb_logandinc.setGeometry(QtCore.QRect(260, 410, 331, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pb_logandinc.setFont(font)
        self.pb_logandinc.setObjectName("pb_logandinc")
        self.frame_4 = QtWidgets.QFrame(self.centralwidget)
        self.frame_4.setGeometry(QtCore.QRect(70, 30, 491, 191))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.label_2 = QtWidgets.QLabel(self.frame_4)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 158, 31))
        self.label_2.setObjectName("label_2")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame_4)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 100, 101, 51))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout.addWidget(self.radioButton_2)
        self.layoutWidget2 = QtWidgets.QWidget(self.frame_4)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 10, 311, 22))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget2)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_deviceid = QtWidgets.QLineEdit(self.layoutWidget2)
        self.lineEdit_deviceid.setObjectName("lineEdit_deviceid")
        self.horizontalLayout.addWidget(self.lineEdit_deviceid)
        self.layoutWidget_5 = QtWidgets.QWidget(self.frame_4)
        self.layoutWidget_5.setGeometry(QtCore.QRect(10, 40, 311, 22))
        self.layoutWidget_5.setObjectName("layoutWidget_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget_5)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_13 = QtWidgets.QLabel(self.layoutWidget_5)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_4.addWidget(self.label_13)
        self.lineEdit_deviceid_2 = QtWidgets.QLineEdit(self.layoutWidget_5)
        self.lineEdit_deviceid_2.setObjectName("lineEdit_deviceid_2")
        self.horizontalLayout_4.addWidget(self.lineEdit_deviceid_2)
        self.widget = QtWidgets.QWidget(self.frame_4)
        self.widget.setGeometry(QtCore.QRect(10, 160, 221, 22))
        self.widget.setObjectName("widget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_9 = QtWidgets.QLabel(self.widget)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_3.addWidget(self.label_9)
        self.lineEdit_deviceid_3 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_deviceid_3.setEnabled(False)
        self.lineEdit_deviceid_3.setObjectName("lineEdit_deviceid_3")
        self.horizontalLayout_3.addWidget(self.lineEdit_deviceid_3)
        self.pb_enabletest = QtWidgets.QPushButton(self.centralwidget)
        self.pb_enabletest.setGeometry(QtCore.QRect(630, 90, 201, 61))
        self.pb_enabletest.setCheckable(True)
        self.pb_enabletest.setChecked(False)
        self.pb_enabletest.setObjectName("pb_enabletest")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(70, 0, 671, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1009, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Log</p></body></html>"))
        self.pb_logpres.setText(_translate("MainWindow", "Log Pressure Sample"))
        self.label_3.setText(_translate("MainWindow", " MIN [PSI]"))
        self.label_4.setText(_translate("MainWindow", "MAX [PSI]"))
        self.label_5.setText(_translate("MainWindow", "ABSOLUTE [PSI]"))
        self.label_8.setText(_translate("MainWindow", "Test Level"))
        self.pb_logfreq.setText(_translate("MainWindow", "Log Frequency Sample"))
        self.label_6.setText(_translate("MainWindow", "FREQUENCY AVG [Hz]"))
        self.label_teststatus.setText(_translate("MainWindow", "Test Disabled"))
        self.pb_logandinc.setText(_translate("MainWindow", "LOG F/P.. AND INCREMENT TEST LEVEL"))
        self.label_2.setText(_translate("MainWindow", "Select Test Method"))
        self.radioButton.setText(_translate("MainWindow", "Hand Puck"))
        self.radioButton_2.setText(_translate("MainWindow", "Fixture"))
        self.label.setText(_translate("MainWindow", "Test Device ID:"))
        self.lineEdit_deviceid.setText(_translate("MainWindow", "Enter Device Name"))
        self.label_13.setText(_translate("MainWindow", "Device Info:     "))
        self.lineEdit_deviceid_2.setText(_translate("MainWindow", "Enter Important Device Info"))
        self.label_9.setText(_translate("MainWindow", "Sensor:     "))
        self.lineEdit_deviceid_3.setText(_translate("MainWindow", "Panasonic P101A"))
        self.pb_enabletest.setText(_translate("MainWindow", "ENABLE TESTING"))
        self.label_7.setText(_translate("MainWindow", "Lora Dicarlo C-Cup Pressure and Frequency Testing"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())