# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore


class TextEditHighlight(QtGui.QTextEdit):

    running = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textChanged.connect(self._doHighlight)

    def _doHighlight(self):
        if self.running:
            return
        self.running = True

        numFormat = QtGui.QTextCharFormat()
        numFormat.setForeground(QtGui.QBrush(QtGui.QColor("blue")))
        numbers = (QtCore.QRegExp("[,.\d]+"), numFormat)

        opFormat = QtGui.QTextCharFormat()
        opFormat.setForeground(QtGui.QBrush(QtGui.QColor("red")))
        operators = (QtCore.QRegExp("[+*/^-]"), opFormat)

        varFormat = QtGui.QTextCharFormat()
        varFormat.setForeground(QtGui.QBrush(QtGui.QColor("green")))
        variables = (QtCore.QRegExp("[a-z][a-z0-9]*\s*="), varFormat)

        constFormat = QtGui.QTextCharFormat()
        constFormat.setForeground(QtGui.QBrush(QtGui.QColor("orange")))
        constants = (QtCore.QRegExp("PI|C|E"), constFormat)

        cursor = self.textCursor()
        for item in (numbers, operators, variables, constants):
            pos = 0
            index = item[0].indexIn(self.toPlainText(), pos)
            while (index != -1):
                cursor.setPosition(index)
                cursor.movePosition(QtGui.QTextCursor.EndOfWord,
                            QtGui.QTextCursor.KeepAnchor, 1)
                cursor.mergeCharFormat(item[1])
                pos = index + item[0].matchedLength()
                index = item[0].indexIn(self.toPlainText(), pos)
        self.running = False
