# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore

class PushAndScroll(QtGui.QPushButton):

    value_changed = QtCore.Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._value = 5
        self._min = 0
        self._max = 10
        self._delta = 1

    def setValue(self, val, minimum=0, maximum=10, delta=1):
        self._value = val
        self._min = minimum
        self._max = maximum
        self._delta = delta

    def wheelEvent(self, event):
        if event.delta() > 0 and self._value < self._max:
            self._value += self._delta
            self.value_changed.emit(self._value)
        if event.delta() < 0 and self._value > self._min:
            self._value -= self._delta
            self.value_changed.emit(self._value)
