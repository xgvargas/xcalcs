# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore
import re


class TextEditHighlight(QtGui.QTextEdit):

    running = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textChanged.connect(self._doHighlight)
        self.elements = (
            (r'[()]', r'black')  # grupos
            ,(r'[+*/^-]', r'red')  # operadores
            ,(r'PI|C|E', r'orange')  # contantes
            ,(r'[a-z][a-z0-9]*', r'magenta')  # instancias
            ,(r'[a-z][a-z0-9]*\s*=', r'green')  # declaracoes
            ,(r'\b(?:(?:\d+(?:[.,]\d+)?)|(?:[.,]\d+))(?:(?:[Ee][+-]?\d+)|[fpnumkMGT])?', r'blue')  # numeros
            ,(r'[#].*?\n', r'gray')  # comentarios
            )

    def setElements(self, elements):
        self.elements = elements

    def _doHighlight(self):
        if self.running:
            return
        self.running = True

        cursor = self.textCursor()
        text = self.toPlainText() + '\n'
        for item in self.elements:
            # print('-------------', item[0])
            style = QtGui.QTextCharFormat()
            style.setForeground(QtGui.QBrush(QtGui.QColor(item[1])))
            for elem in re.finditer(item[0], text):
                # print(elem, elem.start(), elem.end())
                cursor.setPosition(elem.start())
                cursor.movePosition(
                    QtGui.QTextCursor.Right,
                    QtGui.QTextCursor.KeepAnchor,
                    elem.end()-elem.start()
                    )
                cursor.mergeCharFormat(style)
        self.running = False
