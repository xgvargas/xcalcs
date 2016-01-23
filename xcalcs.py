#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import sys, os
from xcalcs_ui import *
import smartside.signal as smartsignal
from smartside import setAsApplication#, getBestTranslation
from console import ConsoleForm
import configparser
import pickle
import decimal

__author__ = 'Gustavo Vargas <xgvargas@gmail.com>'
__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)


settings = configparser.ConfigParser()
settings.read('xcalcs.cfg')
cfg = settings['Config']


class XCalcsApp(QtGui.QWidget, Ui_form_main, smartsignal.SmartSignal):
    def __init__(self, parent=None):
        super(XCalcsApp, self).__init__(parent)
        self.setupUi(self)
        self.auto_connect()

        self.restoreGeometry(QtCore.QByteArray.fromBase64(cfg['geometry']))

        self.shortcuts = self.installShortcuts('Interface_shortcuts', self.tr('(Shortcut: {})'))
        self.shortcuts = self.installShortcuts('Basic_shortcuts', self.tr('(Shortcut: {})'))

        self.format = cfg['format']
        self.angle = cfg['angle']
        self.coordinate = cfg['coordinate']

        decimal.getcontext().prec = int(cfg['precision'])

        self.console = None
        self.editing = None
        self.entry_val = 0
        self.entry_str = ''

        if cfg.getboolean('savestack') and os.path.isfile('stack.dat'):
            self.stack = pickle.load(open('stack.dat', 'rb'))
        else:
            self.stack = []

        self.nhaca=0

        self.moveStackToBottom()
        self.updateAll()

    def closeEvent(self, e):
        cfg['geometry'] = str(self.saveGeometry().toBase64())
        cfg['format'] = self.format
        cfg['angle'] = self.angle
        cfg['coordinate'] = self.coordinate
        with open('xcalcs.cfg', 'w') as configfile:
            settings.write(configfile)
        if cfg.getboolean('savestack'):
            pickle.dump(self.stack, open('stack.dat', 'wb'))
        elif os.path.isfile('stack.dat'):
            os.remove('stack.dat')
        e.accept()

    def installShortcuts(self, section, shortcut_text):
        shortcuts = []
        for k in settings[section]:
            v = settings[section][k]
            if hasattr(self, k) and v:
                ks = QtGui.QKeySequence(v)
                s = QtGui.QShortcut(ks, self)
                obj = getattr(self, k)
                if shortcut_text:
                    obj.setToolTip('{} {}'.format(obj.toolTip(), shortcut_text.format(ks.toString())))
                s.activated.connect(obj.click)
                shortcuts.append(s)
        return shortcuts

    def keyPressEvent(self, e):
        print(e.key(), e.nativeModifiers(), e.nativeScanCode(), e.nativeVirtualKey())
        c = chr(e.key()) if e.key() < 255 else ''

        # multiplier = {'T': 1e12, 'G': 1e9, 'M': 1e6, 'k': 1e3, 'm': 1e-3, 'u': 1e-6, 'n': 1e-9, 'p': 1e-12, 'f': 1e-15}

        if not self.editing:
            if e.key() == QtCore.Qt.Key_Escape:
                print(self.tr('Clean all'))
                self.stack.clear()
                self.updateAll()

            elif e.key() == QtCore.Qt.Key_Backspace:
                if len(self.stack):
                    self.stack.pop()
                    self.updateAll()

            elif e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
                self.stack.append(self.stack[-1])
                self.updateAll()
        else:
            if e.key() == QtCore.Qt.Key_Escape:
                self.editing = False
                self.updateAll()

            elif e.key() == QtCore.Qt.Key_Backspace:
                if len(self.entry_str) > 1:
                    self.entry_str = self.entry_str[:-1]
                else:
                    self.editing = False
                self.updateAll()

            elif e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
                self.stack.append(self.entry_val)
                self.editing = False
                self.updateAll()

            elif c == 'E':
                pass

            elif c == 'G':
                pass

            else:
                pass  # TODO buscar por multiplicadores

        if c >= '0' and c <= '9' or c == '.' or c == ',':
            if not self.editing:
                #entra modo edicao
                self.editing = True
                self.entry_val = 0
                self.entry_str = ''

            if c >= '0' and c <= '9':
                self.entry_str += c

            if c == '.' or c == ',':
                if '.' not in self.entry_str:
                    self.entry_str += '.'

            self.updateAll()

        try:
            self.entry_val = float(self.entry_str)
        except:
            pass

        print(self.editing, self.entry_str, self.entry_val)

    # def stopEdit(self):
    #     self.editing = False

    def getX(self):
        if self.editing:
            return self.entry_val

        if len(self.stack):
            return self.stack[-1]

        return 0 # FIXME

    def formatNumber(self, val):
        if self.format == 'sci':
            v = str(val)
        elif self.format == 'eng':
            v = str(val)
        else:
            v = str(val)

        return v

    def updateBases(self):
        self.edt_bin.setText(bin(int(self.getX())))
        self.edt_oct.setText(oct(int(self.getX())))
        self.edt_hex.setText(hex(int(self.getX())))
        self.edt_float.setText(str(self.getX()))
        self.edt_double.setText(str(self.getX()))

    def updateConverter(self):
        v = self.getX()
        self.lbl_converted.setText(self.formatNumber(v))

    def updateStack(self):
        txt = '''<html><head>
<style type="text/css"> p, li { white-space: pre-wrap; } </style>
</head><body style=" font-family:'Courier New'; font-size:9pt; font-weight:400; font-style:normal;">
<table border="0" align="right" cellspacing="2" cellpadding="0">'''

        adjust = 1 if self.editing else 0

        for i, n in enumerate(self.stack):
            if i < len(self.stack)-3+adjust:
                line = str(len(self.stack)-i+adjust)
            else:
                line = ['X', 'Y', 'Z'][len(self.stack)-i-1+adjust]
            txt += '''<tr><td align="right">{}</td><td width="30" align="center">
<span style="color:#D482B2;">{}</span></td></tr>'''.format(self.formatNumber(n), line)

        if self.editing:
            txt += '''<tr><td align="right"><span style="color:#f00;">{}</span></td>
<td width="30" bgcolor="#fff" align="center">
<span style="color:#D482B2;">X</span></td></tr>'''.format(self.formatNumber(self.entry_str))

        self.edt_stack.setHtml(txt+'</table></body></html>')

        dh = self.edt_stack.document().size().height()
        self.layout_stack.setMaximumHeight(dh)
        self.layout_stack.setMinimumHeight(dh)
        self.moveStackToBottom()

    def updateAll(self):
        self.updateStack()
        self.updateConverter()
        self.updateBases()

    def moveStackToBottom(self):
            b = self.scr_stack.verticalScrollBar()
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
    translator = getBestTranslation('i18n', [cfg['language']])
    app.installTranslator(translator)
    window = XCalcsApp()
    # setAsApplication('gvtech.xcalcs.'+__version__)
    window.show()
    #window.print_all_signals()
    sys.exit(app.exec_())
