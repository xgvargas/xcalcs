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


__author__ = 'Gustavo Vargas <xgvargas@gmail.com>'
__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)


cfg = configparser.ConfigParser()
cfg.read('xcalcs.cfg')


class XCalcsApp(QtGui.QWidget, Ui_form_main, smartsignal.SmartSignal):
    def __init__(self, parent=None):
        super(XCalcsApp, self).__init__(parent)
        self.setupUi(self)
        self.auto_connect()

        self.restoreGeometry(QtCore.QByteArray.fromBase64(cfg['Config']['geometry']))

        self.shortcuts = self.installShortcuts('Interface_shortcuts', self.tr('(Shortcut: {})'))
        self.shortcuts = self.installShortcuts('Basic_shortcuts', self.tr('(Shortcut: {})'))

        self.format = cfg['Config']['format']
        self.angle = cfg['Config']['angle']
        self.coordinate = cfg['Config']['coordinate']

        self.console = None
        self.editing = None
        self.entry_val = 0

        if cfg['Config'].getboolean('savestack') and os.path.isfile('stack.dat'):
            self.stack = pickle.load(open('stack.dat', 'rb'))
        else:
            self.stack = []

        self.nhaca=0

        self.moveStackToBottom()
        self.updateAll()

    def closeEvent(self, e):
        cfg['Config']['geometry'] = str(self.saveGeometry().toBase64())
        cfg['Config']['format'] = self.format
        cfg['Config']['angle'] = self.angle
        cfg['Config']['coordinate'] = self.coordinate
        with open('xcalcs.cfg', 'w') as configfile:
            cfg.write(configfile)
        if cfg['Config'].getboolean('savestack'):
            pickle.dump(self.stack, open('stack.dat', 'wb'))
        elif os.path.isfile('stack.dat'):
            os.remove('stack.dat')
        e.accept()

    def installShortcuts(self, section, shortcut_text):
        shortcuts = []
        for k in cfg[section]:
            v = cfg[section][k]
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
        # print(e.key(), e.nativeModifiers(), e.nativeScanCode(), e.nativeVirtualKey())
        c = chr(e.key()) if e.key() < 255 else ''

        # multiplier = {'T': 1e12, 'G': 1e9, 'M': 1e6, 'k': 1e3, 'm': 1e-3, 'u': 1e-6, 'n': 1e-9, 'p': 1e-12, 'f': 1e-15}

        if not self.editing:
            if e.key() == QtCore.Qt.Key_Escape:
                print(self.tr('Clean all'))

            elif e.key() == QtCore.Qt.Key_Backspace:
                if len(self.stack):
                    print('apaga uma linha')
                    self.stack.pop()
                    self.updateAll()

            elif e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
                print('duplica', self.nhaca)
                self.stack.append(self.nhaca)
                self.nhaca += 1
                self.updateAll()
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
            self.updateAll()

    def getX(self):
        if self.editing:
            return self.entry_val

        if len(self.stack):
            return self.stack[-1]

        return 0

    def formatNumber(self, val):
        if self.format == 'sci':
            v = str(val)
        elif self.format == 'eng':
            v = str(val)
        else:
            v = str(val)

        return v

    def updateBases(self):
        self.edt_bin.setText(bin(self.getX()))
        self.edt_oct.setText(oct(self.getX()))
        self.edt_hex.setText(hex(self.getX()))
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

        for n in self.stack:
            txt += '''<tr><td align="right">{}</td><td width="30" align="center">
<span style="color:#D482B2;">{}</span></td></tr>'''.format(self.formatNumber(n), '23')

#         if self.editing:
#             txt += '''<tr><td><span style="color:#f00;">{}</span></td>
# <td width="30" bgcolor="#fff" align="center">
# <span style="color:#D482B2;">{}</span></td></tr>'''.format(self.formatNumber(self.entry_val), '23')
#             size += 1

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
    translator = getBestTranslation('i18n', [cfg['Config']['language']])
    app.installTranslator(translator)
    window = XCalcsApp()
    # setAsApplication('gvtech.xcalcs.'+__version__)
    window.show()
    #window.print_all_signals()
    sys.exit(app.exec_())
