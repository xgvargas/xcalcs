#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ver isso para colocar o icone correto na taskbar do windows
http://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7
"""

from PySide.QtGui import *
from PySide.QtCore import *
import sys
from xcalcs_ui import *
from smartside import *


__author__ = 'Gustavo Vargas <xgvargas@gmail.com>'
__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)


import ctypes
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class MyApplication(QtGui.QMainWindow, Ui_MainWindow, SmartSide):
    def __init__(self, parent=None):
        super(MyApplication, self).__init__(parent)
        self.setupUi(self)
        self.auto_connect()
        self.cfg = QSettings('oi', 'carcamano')
        self.restoreGeometry(self.cfg.value('geometry'))
        #self.restoreState(self.cfg.value('state'))
        #print 'lendo bunda:',self.cfg.value('bunda', type=int)

    def closeEvent(self, event):
        self.cfg.setValue('geometry', self.saveGeometry())
        #self.cfg.setValue('state', self.saveState())
        self.cfg.setValue('bunda', 12)
        event.accept()

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
        print '_on_btn_coord__clicked', self.sender().isDown(), self.sender().isChecked()

    def _on_btn_conv__toggled(self):
        print '_on_btn_conv__toggle', self.sender().isDown(), self.sender().isChecked()

    def _on_btn_base__toggled(self):
        print '_on_btn_base__toggled', self.sender().isDown(), self.sender().isChecked()

    _funcoes = '`btn_f_.+`'
    def _when_funcoes__clicked(self):
        print self.sender().objectName()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApplication()
    window.show()
    #window.print_all_signals()
    sys.exit(app.exec_())
