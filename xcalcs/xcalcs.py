#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# from PySide.QtGui import *
# from PySide.QtCore import *
import sys
from xcalcs_ui import *
import smartside.signal as smartsignal
from smartside import setAsApplication


__author__ = 'Gustavo Vargas <xgvargas@gmail.com>'
__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)


class MyApplication(QtGui.QWidget, Ui_Form, smartsignal.SmartSignal):
    def __init__(self, parent=None):
        super(MyApplication, self).__init__(parent)
        self.setupUi(self)
        self.auto_connect()
        # self.cfg = QSettings('oi', 'carcamano')
        # self.restoreGeometry(self.cfg.value('geometry'))
        #self.restoreState(self.cfg.value('state'))
        #print 'lendo bunda:',self.cfg.value('bunda', type=int)

        self.editing = None
        self.nuns = [0]*32

    def closeEvent(self, e):
        # self.cfg.setValue('geometry', self.saveGeometry())
        #self.cfg.setValue('state', self.saveState())
        # self.cfg.setValue('bunda', 12)
        e.accept()

    def keyPressEvent(self, e):
        # print e.key(), e.nativeModifiers(), e.nativeScanCode(), e.nativeVirtualKey()
        c = chr(e.key()) if e.key() < 255 else ''
        shorts = (
                    ('+', self.btn_f_add),
                    ('-', self.btn_f_sub),
                    ('*', self.btn_f_mul),
                    ('/', self.btn_f_div),
                    ('S', self.btn_f_swap),
                    # ('P', self.btn_f_pi),
                    ('Q', self.btn_f_power2),
                    ('R', self.btn_f_sqrt2),
                    ('C', self.btn_f_tocomplex),
                    ('V', self.btn_f_breakcomplex),
                    ('I', self.btn_f_inv),
                    ('G', self.btn_f_minus),
                    ('L', self.btn_f_powerx),
                    )

        for k, f in shorts:
            if c == k:
                if self.editing:
                    #TODO confirma edicao
                    pass
                f.click()

        if not self.editing:
            if e.key() == QtCore.Qt.Key_Escape:
                print 'limpa tudo'
            elif e.key() == QtCore.Qt.Key_Backspace:
                print 'apaga uma linha'
            elif e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
                print 'duplica'
        else:
            if e.key() == QtCore.Qt.Key_Escape:
                print 'para edit'
            elif e.key() == QtCore.Qt.Key_Backspace:
                print 'volta edit'
            elif e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
                print 'confirma'
            elif c == 'E':
                pass
            elif c == 'G':
                pass

        if c >= '0' and c <= '9' or c == '.' or c == ',':
            if self.editing:
                #continua edicao
                pass
            else:
                #entra modo edicao
                self.editing = True
                self.edt_num.setHtml('oi')
            print 'numero'
            self._showNuns()

    def _showNuns(self):
        txt = '''<html><head><style type="text/css">
p {margin: 0px 0px; -qt-block-indent:0; text-indent:0px; white-space: pre-wrap; text-align: right;}
body {font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:400; font-style:normal;}
</style></head><body>'''

        for n in self.nuns:
            txt += '<p align="right">{}</p>'.format('nhaaa')

            self.edt_num.setHtml(txt+'</body></html>')

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
    setAsApplication('techin.xcalcs.'+__version__)
    window.show()
    #window.print_all_signals()
    sys.exit(app.exec_())
