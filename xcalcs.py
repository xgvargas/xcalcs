#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import sys
from xcalcs_ui import *
import smartside.signal as smartsignal
from smartside import setAsApplication#, getBestTranslation
from console import ConsoleForm


__author__ = 'Gustavo Vargas <xgvargas@gmail.com>'
__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)


class XCalcsApp(QtGui.QWidget, Ui_form_main, smartsignal.SmartSignal):
    def __init__(self, parent=None):
        super(XCalcsApp, self).__init__(parent)
        self.setupUi(self)
        self.auto_connect()
        # self.cfg = QSettings('oi', 'carcamano')
        # self.restoreGeometry(self.cfg.value('geometry'))
        #self.restoreState(self.cfg.value('state'))
        #print('lendo bunda:',self.cfg.value('bunda', type=int))

        self._display_to_bottom()

        self.console = None
        self.editing = None
        self.nuns = [0]*32

    def closeEvent(self, e):
        # self.cfg.setValue('geometry', self.saveGeometry())
        #self.cfg.setValue('state', self.saveState())
        # self.cfg.setValue('bunda', 12)
        e.accept()

    def keyPressEvent(self, e):
        # print(e.key(), e.nativeModifiers(), e.nativeScanCode(), e.nativeVirtualKey())
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
                print(self.tr('Clean all'))
            elif e.key() == QtCore.Qt.Key_Backspace:
                print(self.tr('apaga uma linha'))
            elif e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
                print(self.tr('duplica'))
        else:
            if e.key() == QtCore.Qt.Key_Escape:
                print('para edit')
            elif e.key() == QtCore.Qt.Key_Backspace:
                print('volta edit')
            elif e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
                print('confirma')
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
            print('numero')
            self._showNuns()

    def _showNuns(self):
        txt = '''<html><head><style type="text/css">
p {margin: 0px 0px; -qt-block-indent:0; text-indent:0px; white-space: pre-wrap; text-align: right;}
body {font-family:'Courier New'; font-size:9pt; font-weight:400; font-style:normal;}
</style></head><body>'''

        for n in self.nuns:
            txt += '<p align="right">{}</p>'.format('nhaaa')   #<span style=" color:#ff0000;">asdqweqweasd</span>

        self.edt_num.setHtml(txt+'</body></html>')
        self._display_to_bottom()

    def _display_to_bottom(self):
            b = self.scr_display.verticalScrollBar()
            b.setValue(b.maximum())

    def _on_btn_angle__clicked(self):
        print('_on_btn_angle__clicked')

    def _on_btn_format__clicked(self):
        print('_on_btn_format__clicked')

    def _on_btn_coord__clicked(self):
        print('_on_btn_coord__clicked')

    def _on_btn_solver__clicked(self):
        if not self.console:
            self.console = ConsoleForm()
        self.console.show()

    _funcoes = '`btn_f_.+`'
    def _when_funcoes__clicked(self):
        print(self.sender().objectName())

from os import path
def getBestTranslation(basedir, lang=None):
    """
    Find inside basedir the best translation available.

    lang, if defined, should be a list of prefered languages.

    It will look for file in the form:
    - en-US.qm
    - en_US.qm
    - en.qm
    """
    if not lang:
        lang = QtCore.QLocale.system().uiLanguages()

    for l in lang:

        l = l.translate({ord('_'): '-'})
        f = path.join(basedir, l+'.qm')
        if path.isfile(f): break

        l = l.translate({ord('-'): '_'})
        f = path.join(basedir, l+'.qm')
        if path.isfile(f): break

        l = l.split('_')[0]
        f = path.join(basedir, l+'.qm')
        if path.isfile(f): break

    else:
        return None

    translator = QtCore.QTranslator()
    translator.load(f)
    return translator

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    translator = getBestTranslation('i18n')
    app.installTranslator(translator)
    window = XCalcsApp()
    setAsApplication('gvtech.xcalcs.'+__version__)
    window.show()
    #window.print_all_signals()
    sys.exit(app.exec_())
