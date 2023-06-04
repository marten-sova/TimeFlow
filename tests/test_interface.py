from timer import Timer, SECOND_MS
from PyQt5 import QtCore

# This buffer is needed because the test framework / UI takes a little longer
# to respond than the exact MS that the timer lasts for
BUFFER = 350


def test_timer_flow(qtbot, monkeypatch):
    widget = Timer()
    widget.speed_multiplier = 1000
    qtbot.addWidget(widget)

    def check_break_label():
        assert widget.ui.start_timer.text() == "Start Break"

    def check_start_timer():
        assert widget.ui.start_timer.text() == "Start Timer"

    check_start_timer()
    start_work_timer_value = widget.ui.lcd_number.intValue()
    assert start_work_timer_value == 20
    finish_ms = (
        (SECOND_MS * (start_work_timer_value * 60)) / widget.speed_multiplier
    ) + BUFFER
    qtbot.mouseClick(widget.ui.start_timer, QtCore.Qt.LeftButton)
    qtbot.waitUntil(
        check_break_label, timeout=finish_ms,
    )

    break_timer_value = widget.ui.lcd_number.intValue()
    assert break_timer_value == 5
    finish_ms = (
        (SECOND_MS * (break_timer_value * 60)) / widget.speed_multiplier
    ) + BUFFER
    qtbot.mouseClick(widget.ui.start_timer, QtCore.Qt.LeftButton)
    qtbot.waitUntil(
        check_start_timer, timeout=finish_ms,
    )
