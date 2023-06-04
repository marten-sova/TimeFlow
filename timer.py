"""
    File name: timer.py
    Author: Team Mac
    Date created: 2021-12-08
    Alert Sounds Credits: https://freesound.org
"""
import sys
from threading import Thread

from PyQt5.QtWidgets import QDialog, QInputDialog, QApplication, QComboBox
from PyQt5 import QtCore
import pygame

from ui import Ui


SECOND_MS = 1000

pygame.mixer.init()


class Timer(QDialog):
    """
    Timer program to help manage time and break out of the flow state.
    """

    def __init__(self):
        super(Timer, self).__init__()
        self.ui = Ui()
        self.ui.setupUi(self, QComboBox)

        self.change_allowed = True  # whether or not change buttons can be clicked
        self.work_active = True  # whether or not work timer is active
        self.break_active = True  # whether or not break timer is active
        self.break_time = 5
        self.work_unit_time_min = 20
        self.task_count = 1
        self.speed_multiplier = 1  # [1 for normal speed]
        self.volume_level = 1.0
        self.alert_sound = None
        self.task_break = None
        self.my_timer = QtCore.QTimer()

        self.ui.start_timer.clicked.connect(lambda: self.on_start_clicked())
        self.ui.end_timer.clicked.connect(lambda: self.on_end_clicked())
        self.ui.change_timer.clicked.connect(lambda: self.on_change_clicked())
        self.ui.change_break.clicked.connect(lambda: self.on_break_clicked())
        self.ui.change_volume.clicked.connect(lambda: self.on_volume_clicked())

        self.ui.lcd_number.display(f"{self.work_unit_time_min}.00")

    def play_sound(self):
        t = Thread(target=self._sound)
        t.start()

    def _sound(self):
        self.alert_sound = pygame.mixer.Sound(f"./sounds/{self.alert_sound}")
        self.alert_sound.set_volume(self.volume_level)
        self.alert_sound.play()

    def _countdown_time(self, minutes, seconds):
        if seconds == 0.0:
            minutes -= 1
            seconds = 0.60
        else:
            seconds -= 0.01
        return minutes, seconds

    def countdown(self):
        time = self.ui.lcd_number.value()
        if time != 0.0:
            minutes, seconds = self._countdown_time(int(time), round(time % 1, 2))

            seconds = "{:.2f}".format((seconds))[1::]
            self.ui.lcd_number.display(f"{minutes}{seconds}")
        else:
            minutes = 0.0
            seconds = 0.0

        if (minutes == 0 and float(seconds) == 0) and self.task_break in [
            True,
            None,
        ]:
            # Regular Break code
            self.task_break = False
            self.ui.start_timer.setText("Start Break")
            self.ui.lcd_number.setStyleSheet("color: red;")
            # enables change break time button, disables change work time button
            self.break_active = True
            self.work_active = False

            self.ui.lcd_number.display(f"{self.break_time}.00")
            self.my_timer.disconnect()
            self.play_sound()
            self.change_allowed = (
                True  # allows change buttons to work after timer finishes
            )
            return

        elif (minutes == 0 and float(seconds) == 0) and self.task_break is False:
            # Start task code
            self.task_break = True
            self.task_count += 1
            self.ui.start_timer.setText("Start Timer")
            self.ui.lcd_number.setStyleSheet("color: black;")
            # enables change work time button, disables change break time button
            self.work_active = True
            self.break_active = False

            self.ui.lcd_number.display(f"{self.work_unit_time_min}.00")
            self.my_timer.disconnect()
            self.play_sound()
            self.change_allowed = True
            return

    def on_end_clicked(self):
        sys.exit()

    def on_start_clicked(self):
        self.alert_sound = self.ui.comboSounds.currentText()
        if not self.change_allowed:
            return
        self.my_timer.timeout.connect(lambda: self.countdown())
        self.my_timer.start(
            round(SECOND_MS / self.speed_multiplier)
        )  # 1 second in milliseconds

        self.change_allowed = (
            False  # change buttons will not work when timer is operating
        )

    def on_change_clicked(self):
        if self.change_allowed is True and self.work_active is True:
            num, result = QInputDialog.getInt(
                self, "Work Timer Length Input Dialog", "Enter the work timer length:"
            )  # popup window for user configuration
            if result is True:
                self.work_unit_time_min = num
                self.ui.lcd_number.display(self.work_unit_time_min)

    def on_break_clicked(self):
        if self.change_allowed is True and self.break_active is True:
            num, result = QInputDialog.getInt(
                self, "Break Timer Length Input Dialog", "Enter the break timer length:"
            )
            if result is True:
                self.break_time = num
                self.ui.lcd_number.display(self.break_time)

    def on_volume_clicked(self):
        if self.change_allowed is True:
            num, result = QInputDialog.getInt(
                self,
                "Volume Change",
                "Select Volume Level",
                int(self.volume_level * 10),
                0,
                10,
                1,
            )
            if result is True:
                self.volume_level = float(num / 10)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Timer()
    window.show()
    app.exec()
