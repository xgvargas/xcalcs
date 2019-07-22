# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore


class TextEditHighlight(QtGui.QTextEdit):

    running = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textChanged.connect(self._doHighlight)
        self.elements = (
            ("[()]", "black")                 # grupos
            ,("[,.\d]+", "blue")              # numeros
            ,("[+*/^-]", "red")               # operadores
            ,("PI|C|E", "orange")             # contantes
            ,("[a-z][a-z0-9]*", "magenta")    # instancias
            ,("[a-z][a-z0-9]*\s*=", "green")  # declaracoes
            )

    def setElements(self, elements):
        self.elements = elements

    def _doHighlight(self):
        if self.running:
            return
        self.running = True

        cursor = self.textCursor()
        for item in self.elements:
            regex = QtCore.QRegExp(item[0])
            style = QtGui.QTextCharFormat()
            style.setForeground(QtGui.QBrush(QtGui.QColor(item[1])))
            pos = 0
            index = regex.indexIn(self.toPlainText(), pos)
            while (index != -1):
                cursor.setPosition(index)

                # cursor.movePosition(QtGui.QTextCursor.EndOfWord, QtGui.QTextCursor.KeepAnchor, 1)
                cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor, regex.matchedLength())

                cursor.mergeCharFormat(style)

                pos = index + regex.matchedLength()
                index = regex.indexIn(self.toPlainText(), pos)
        self.running = False
