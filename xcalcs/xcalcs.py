#!/usr/bin/python

# -*- coding: utf-8 -*-

from PySide.QtGui import *
from PySide.QtCore import *
import sys
from xcalcs_ui import *
from smartside import *


class MyApplication(QtGui.QMainWindow, Ui_MainWindow, SmartSide):
    def __init__(self, parent=None):
        super(MyApplication, self).__init__(parent)
        self.setupUi(self)
        self.auto_connect()

    def keyPressEvent(self, event):
        print event.key(), event.nativeModifiers(), event.nativeScanCode(), event.nativeVirtualKey()
        if event.key() == QtCore.Qt.Key_Escape:
            print 'foi ESC!'
            print dir(event)

    def _on_btn_angle__clicked(self):
        print '_on_btn_angle__clicked'

    def _on_btn_format__clicked(self):
        print '_on_btn_format__clicked'

    def _on_btn_coord__clicked(self):
        print '_on_btn_coord__clicked'

    def _on_btn_conv__clicked(self):
        print '_on_btn_conv__clicked'

    def _on_btn_base__clicked(self):
        print '_on_btn_base__clicked'

    _funcoes = '`btn_f_.+`'
    def _when_funcoes__clicked(self):
        print 'balacubacu'
        print self.sender()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApplication()
    window.show()
    #window.print_all_signals()
    sys.exit(app.exec_())
