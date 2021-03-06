#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cmd /k "cd /d D:\Projetos\xcalcs\venv\Scripts & activate & cd /d D:\Projetos\xcalcs & python xcalcs.py"
D:\Projetos\xcalcs\venv\Scripts\pythonw.exe xcalcs.py
"""

import sys, os
from xcalcs_ui import *
import smartside.signal as smartsignal
from smartside import setAsApplication#, getBestTranslation
from console import ConsoleForm
import configparser
import pickle
import units
import math
from struct import pack

__author__ = 'Gustavo Vargas <xgvargas@gmail.com>'
__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)


settings = configparser.ConfigParser()
settings.read('xcalcs.cfg')
cfg = settings['Config']


class XCalcsApp(QtGui.QWidget, Ui_form_main, smartsignal.SmartSignal):

    multiplier = {'T': 1e12, 'G': 1e9, 'M': 1e6, 'k': 1e3, 'm': 1e-3, 'u': 1e-6, 'n': 1e-9, 'p': 1e-12, 'f': 1e-15}

    def __init__(self, parent=None):
        super(XCalcsApp, self).__init__(parent)
        self.setupUi(self)
        self.auto_connect()

        self.restoreGeometry(QtCore.QByteArray.fromBase64(cfg['geometry']))

        if cfg.getboolean('stayontop', False):
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        self.shortcuts = self.installShortcuts('Interface_shortcuts', self.tr('(Shortcut: {})'))
        self.shortcuts = self.installShortcuts('Basic_shortcuts', self.tr('(Shortcut: {})'))

        self.format = cfg['format']
        self.angle = cfg['angle']
        self.coordinate = cfg['coordinate']

        self.precision = int(cfg['precision'])
        self.btn_format.setValue(self.precision, 1, 12)

        self.btn_format.setText('{} ({:d})'.format(self.format.title(), self.precision))
        self.btn_angle.setText(self.angle.title())
        self.btn_coord.setText(self.coordinate.title())

        self.console = None
        self.editing = None
        self.entry_val = 0
        self.entry_str = ''

        if cfg.getboolean('savestack', False) and os.path.isfile('stack.dat'):
            self.stack = pickle.load(open('stack.dat', 'rb'))
        else:
            self.stack = []

        self.converter = units.Converter()
        self.cmb_quantity.setCurrentIndex(2)

        self.moveStackToBottom()
        self.updateAll()

    def closeEvent(self, e):
        cfg['geometry'] = str(self.saveGeometry().toBase64())
        cfg['format'] = self.format
        cfg['angle'] = self.angle
        cfg['coordinate'] = self.coordinate
        cfg['precision'] = str(self.precision)
        with open('xcalcs.cfg', 'w') as configfile:
            settings.write(configfile)
        if cfg.getboolean('savestack', False):
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
        # print(e.key(), e.nativeModifiers(), e.nativeScanCode(), e.nativeVirtualKey())
        c = chr(e.key()) if e.key() < 255 else ''

        if not self.editing:
            if e.key() == QtCore.Qt.Key_Escape:
                self.stack.clear()
                self.updateAll()

            elif e.key() == QtCore.Qt.Key_Backspace:
                if len(self.stack):
                    self.stack.pop()
                    self.updateAll()

            elif e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
                if len(self.stack):
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


        try:
            self.entry_val = float(self.entry_str)
        except:
            pass

        self.updateAll()
        # print(self.editing, self.entry_str, self.entry_val)

    def getX(self):
        if self.editing:
            return self.entry_val

        if len(self.stack):
            return self.stack[-1]

        return 0 # FIXME

    def pop(self, n=1):
        if len(self.stack) >= n:
            r = []
            for _ in range(n):
                r.append(self.stack.pop())
        else:
            raise IndexError

        return tuple(r)

    def popAngle(self):
        v = self.stack.pop()
        if self.angle == 'deg':
            v = math.radians(v)
        return v

    def appendAngle(self, a):
        if self.angle == 'deg':
            a = math.degrees(a)

        self.stack.append(a)

    def formatNumber(self, val):

        if self.format == 'sci':
            a = '{0:.{pre}E}'.format(val, pre=self.precision)
            v = a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]
        elif self.format == 'eng':
            v = str(val)
        else:
            v = str(val)

        return v

    def updateBases(self):
        self.edt_bin.setText(bin(int(self.getX())))
        self.edt_oct.setText(oct(int(self.getX())))
        self.edt_hex.setText(hex(int(self.getX())))
        d = pack('>fd', self.getX(), self.getX())
        self.edt_float.setText('{0[0]:02X}.{0[1]:02X}.{0[2]:02X}.{0[3]:02X}'.format(d))
        self.edt_double.setText(
            '{0[0]:02X}.{0[1]:02X}.{0[2]:02X}.{0[3]:02X}.{0[4]:02X}.{0[5]:02X}.{0[6]:02X}.{0[7]:02X}'.format(d[4:]))

    def updateConverter(self):
        v = self.getX()
        c, u = self.converter.convert(v,
                                      self.cmb_quantity.currentIndex(),
                                      self.list_conv_left.currentRow(),
                                      self.list_conv_right.currentRow())
        self.btn_conv_right.setText('{} {}'.format(self.formatNumber(c), u))
        c, u = self.converter.convert(v,
                                      self.cmb_quantity.currentIndex(),
                                      self.list_conv_right.currentRow(),
                                      self.list_conv_left.currentRow())
        self.btn_conv_left.setText('{} {}'.format(self.formatNumber(c), u))

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
<span style="color:#D482B2;">X</span></td></tr>'''.format(self.entry_str)

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

    def _on_cmb_quantity__currentIndexChanged(self):
        names = self.converter.getNames(self.cmb_quantity.currentIndex())
        self.list_conv_left.clear()
        self.list_conv_left.insertItems(0, names)
        self.list_conv_left.setCurrentRow(0)
        self.list_conv_right.clear()
        self.list_conv_right.insertItems(0, names)
        self.list_conv_right.setCurrentRow(1)
        self.updateConverter()

    _conv_lists = '`list_conv_.+`'
    def _when_conv_lists__clicked(self):
        self.updateConverter()

    _conv_copy = '`btn_conv_.+`'
    def _when_conv_copy__clicked(self):
        self.stack.append(float(self.sender().text()))
        self.updateAll()

    def _on_btn_angle__clicked(self):
        self.angle = 'deg' if self.angle == 'rad' else 'rad'

        self.btn_angle.setText(self.angle.title())

    def _on_btn_format__clicked(self):
        if self.format == 'def':
            self.format = 'sci'
        elif self.format == 'sci':
            self.format = 'eng'
        else:
            self.format = 'def'

        self.btn_format.setText('{} ({:d})'.format(self.format.title(), self.precision))
        self.updateAll()

    def _on_btn_format__value_changed(self, val):
        self.precision = val
        self.btn_format.setText('{} ({:d})'.format(self.format.title(), self.precision))
        self.updateAll()

    def _on_btn_coord__clicked(self):
        self.coordinate = 'cart' if self.coordinate == 'pol' else 'pol'

        self.btn_coord.setText(self.coordinate.title())

    def _on_btn_solver__clicked(self):
        if not self.console:
            self.console = ConsoleForm()
        self.console.show()

    _funcoes = '`btn_f_.+`'
    def _when_funcoes__clicked(self):
        # print(self.sender().objectName())

        if self.editing:
            self.stack.append(self.entry_val)
            self.editing = False

        op = self.sender().objectName().split('_')[2]

        try:
            if op == '10powerx':
                x, = self.pop()
                self.stack.append(math.pow(10, x))

            elif op == 'acos':
                x, = self.pop()
                self.appendAngle(math.acos(x))

            elif op == 'add':
                x, y = self.pop(2)
                self.stack.append(x+y)

            elif op == 'asin':
                x, = self.pop()
                self.appendAngle(math.asin(x))

            elif op == 'atg':
                x, = self.pop()
                self.appendAngle(math.atan(x))

            elif op == 'breakcomplex':
                pass
            elif op == 'conjugate':
                pass
            elif op == 'cos':
                x = self.popAngle()
                self.stack.append(math.cos(x))

            elif op == 'div':
                x, y = self.pop(2)
                self.stack.append(y/x)

            elif op == 'epowerx':
                x, = self.pop()
                self.stack.append(math.exp(x))

            elif op == 'inv':
                x, = self.pop()
                self.stack.append(1./x)

            elif op == 'ln':
                x, = self.pop()
                self.stack.append(math.log(x))

            elif op == 'log10':
                x, = self.pop()
                self.stack.append(math.log10(x))

            elif op == 'log2':
                x, = self.pop()
                self.stack.append(math.log2(x))

            elif op == 'minus':
                x, = self.pop()
                self.stack.append(-x)

            elif op == 'mul':
                x, y = self.pop(2)
                self.stack.append(x*y)

            elif op == 'power2':
                x, = self.pop()
                self.stack.append(math.pow(x, 2))

            elif op == 'powerx':
                x, y = self.pop(2)
                self.stack.append(math.pow(y, x))

            elif op == 'sin':
                x = self.popAngle()
                self.stack.append(math.sin(x))

            elif op == 'sqrt2':
                x, = self.pop()
                self.stack.append(math.sqrt(x))

            elif op == 'sqrtx':
                x, y = self.pop(2)
                self.stack.append(math.pow(y, 1./x))

            elif op == 'sub':
                x, y = self.pop(2)
                self.stack.append(y-x)

            elif op == 'swap':
                x, y = self.pop(2)
                self.stack.append(x)
                self.stack.append(y)

            elif op == 'tg':
                x = self.popAngle()
                self.stack.append(math.tan(x))

            elif op == 'tocomplex':
                pass
        except IndexError:
            pass
            print('nhaca')
        except:
            raise

        self.updateAll()


        # fatorial
        #  combinacao C(n,r) = n! / ( r! (n - r)! )
        # permutacao P(n,r) = n! / (n - r)!
        # random




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

    # if hasattr(sys, "frozen"):
    #     appver = esky.Esky(sys.executable, "http://example.com/downloads/")
    #     appver.auto_update()

    app = QtGui.QApplication(sys.argv)
    translator = getBestTranslation('i18n', [cfg['language']])
    app.installTranslator(translator)
    window = XCalcsApp()
    # setAsApplication('gvtech.xcalcs.'+__version__)
    window.show()
    # window.print_all_signals()
    sys.exit(app.exec_())
