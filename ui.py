# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont


class Ui(object):
    def setupUi(self, Dialog, QComboBox):
        Dialog.setObjectName("TimeFlo+")
        Dialog.resize(400, 350)
        self.start_timer = QtWidgets.QPushButton(Dialog)
        self.start_timer.setGeometry(QtCore.QRect(40, 220, 150, 32))
        self.start_timer.setObjectName("StartTimer")

        self.end_timer = QtWidgets.QPushButton(Dialog)
        self.end_timer.setGeometry(QtCore.QRect(220, 220, 150, 32))
        self.end_timer.setObjectName("endTimer")

        self.lcd_number = QtWidgets.QLCDNumber(Dialog)
        self.lcd_number.setGeometry(QtCore.QRect(60, 40, 281, 140))
        self.lcd_number.setObjectName("lcdNumber")

        self.change_volume = QtWidgets.QPushButton(Dialog)
        self.change_volume.setGeometry(QtCore.QRect(220, 185, 150, 32))
        self.change_volume.setObjectName("changeVolume")

        self.change_timer = QtWidgets.QPushButton(Dialog)
        self.change_timer.setGeometry(QtCore.QRect(40, 260, 150, 32))
        self.change_timer.setObjectName("changeTimer")

        self.change_break = QtWidgets.QPushButton(Dialog)
        self.change_break.setGeometry(QtCore.QRect(220, 260, 150, 32))
        self.change_break.setObjectName("changeBreak")

        self.model = QStandardItemModel(Dialog)
        self.comboSounds = QComboBox(Dialog)
        self.comboSounds.setGeometry(QtCore.QRect(40, 185, 150, 32))
        # self.comboSounds.setFixedSize(275, 50)
        self.comboSounds.setFont(QFont("", 12))
        self.comboSounds.setModel(self.model)

        data = ["analog_alarm.wav", "stop_watch_alarm.wav", "ringer.wav"]

        for sound in data:
            state = QStandardItem(sound)
            self.model.appendRow(state)

        self.retranslateUi(Dialog, QComboBox)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog, QComboBox):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "TimeFlo+"))
        self.start_timer.setText(_translate("Dialog", "Start Timer"))
        self.end_timer.setText(_translate("Dialog", "Quit Timer"))
        self.change_timer.setText(_translate("Dialog", "Change Timer"))
        self.change_break.setText(_translate("Dialog", "Change Break"))
        self.change_volume.setText(_translate("Dialog", "Change Volume"))
        self.comboSounds.setObjectName(_translate("QComboBox", "Select Sound"))
