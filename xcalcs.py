#!/home/gustavo/p/xcalcs/venv/bin/python
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
cmd /k "cd /d D:\Projetos\xcalcs\venv\Scripts & activate & cd /d D:\Projetos\xcalcs & python xcalcs.py"
D:\Projetos\xcalcs\venv\Scripts\pythonw.exe xcalcs.py
"""

import sys, os
from xcalcs_ui import *
import smartside.signal as smartsignal
from smartside import setAsApplication, getBestTranslation
# from console import ConsoleForm
import configparser
import pickle
import units
import math
from struct import pack
import appdirs
import solver
import rpnsolver

__author__ = 'Gustavo Vargas <xgvargas@gmail.com>'
__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)


#if getattr(sys, 'frozen', False):
#    appPath = os.path.dirname(sys.executable)
#else:
#    appPath = os.path.dirname(os.path.realpath(__file__))
#settingFile = os.path.join(appPath, 'xcalcs.cfg')
#stackFile = os.path.join(appPath, 'stack.dat')
settingFile = os.path.join(appdirs.user_config_dir(), 'xcalcs.cfg')
stackFile = os.path.join(appdirs.user_data_dir(), 'xcalcs-stack.dat')
eqFile = os.path.join(appdirs.user_data_dir(), 'xcalcs-equation.dat')

settings = configparser.ConfigParser()
settings.read(settingFile)
cfg = settings['Config']


class XCalcsApp(QtGui.QWidget, Ui_form_main, smartsignal.SmartSignal):

    multiplier = {'T': 1e12, 'G': 1e9, 'M': 1e6, 'k': 1e3, 'm': 1e-3, 'u': 1e-6, 'n': 1e-9, 'p': 1e-12, 'f': 1e-15}

    def __init__(self, parent=None):
        super(XCalcsApp, self).__init__(parent)
        self.setupUi(self)
        self.eq_scroll = self.edt_equations.verticalScrollBar()
        self.result_scroll = self.edt_results.verticalScrollBar()
        self.auto_connect()

        self.restoreGeometry(QtCore.QByteArray.fromBase64(cfg['geometry']))

        if cfg.getboolean('stayontop', False):
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        self.shortcuts = self.installShortcuts('Interface_shortcuts', self.tr('(Shortcut: {})'))
        self.shortcuts = self.installShortcuts('Basic_shortcuts', self.tr('(Shortcut: {})'))
        self.shortcuts = self.installShortcuts('Advanced_shortcuts', self.tr('(Shortcut: {})'))

        self.format = cfg['format']
        self.angle = cfg['angle']
        self.coordinate = cfg['coordinate']

        self.boxRPN.setVisible(cfg.getboolean('showrpn', True))
        self.btn_show_rpn.setChecked(cfg.getboolean('showrpn', True))
        self.boxSolver.setVisible(cfg.getboolean('showsolver', False))
        self.btn_show_solver.setChecked(cfg.getboolean('showsolver', False))
        self.boxHelpers.setVisible(cfg.getboolean('showhelpers', False))
        self.btn_show_helpers.setChecked(cfg.getboolean('showhelpers', False))

        self.precision = int(cfg['precision'])
        self.btn_format.setValue(self.precision, 1, 12)

        self.btn_format.setText('{} ({:d})'.format(self.format.title(), self.precision))
        self.btn_angle.setText(self.angle.title())
        self.btn_coord.setText(self.coordinate.title())

        # self.console = None
        self.editing = None
        self.entry_val = 0
        self.entry_str = ''

        if cfg.getboolean('savestack', False) and os.path.isfile(stackFile):
            self.stack = pickle.load(open(stackFile, 'rb'))
            self.edt_equations.setText(pickle.load(open(eqFile, 'rb')))
        else:
            self.stack = []

        self.converter = units.Converter()
        self.cmb_quantity.setCurrentIndex(2)

        self.posfixMode = cfg.getboolean('posfix', False)
        if self.posfixMode:
            self.btn_posfix.setText('Posfix')
        else:
            self.btn_posfix.setText('Infix')

        # self.eq_scroll = self.edt_equations.verticalScrollBar()
        # self.edt_equations.setElements( (
        #     ()  #
        #     ()  #
        #     ()  #
        #     ()  #
        #     ) )

        # self.auto_connect()

        self.lbl_error.setText('')

        self.moveStackToBottom()
        self.updateAll()

        self.populateConstants()

    def closeEvent(self, e):
        cfg['geometry'] = str(self.saveGeometry().toBase64())
        cfg['format'] = self.format
        cfg['angle'] = self.angle
        cfg['coordinate'] = self.coordinate
        cfg['precision'] = str(self.precision)
        cfg['showrpn'] = str(self.boxRPN.isVisible())
        cfg['showsolver'] = str(self.boxSolver.isVisible())
        cfg['showhelpers'] = str(self.boxHelpers.isVisible())
        cfg['posfix'] = str(self.posfixMode)

        with open(settingFile, 'w') as configfile:
            settings.write(configfile)
        if cfg.getboolean('savestack', False):
            pickle.dump(self.stack, open(stackFile, 'wb'))
            pickle.dump(self.edt_equations.toPlainText(), open(eqFile, 'wb'))
        elif os.path.isfile(stackFile):
            os.remove(stackFile)
            os.remove(eqFile)
        e.accept()

    def installShortcuts(self, section, shortcut_text):
        shortcuts = []

        # TODO avisar que 'E' e 'G' eh reservado

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
        # print(c)
        # print(e.key())
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

            elif c == 'g':
                # print('cheguei')
                # if self.entry_str[0] == '-':
                #     print('1')
                #     print(self.entry_str)
                #     self.entry_str = self.entry_str[1:]
                # else:
                #     print('2')
                #     print(self.entry_str)
                #     self.entry_str = '-' + self.entry_str
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

    def getX(self, accept_complex=False):
        if self.editing:
            return self.entry_val

        if len(self.stack):
            v = self.stack[-1]
            if isinstance(v, complex) and not accept_complex:
                v = v.real
            return v

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

    def formatNumber(self, val, sep='\u00a0'):

        if isinstance(val, complex):
            if self.coordinate == 'cart':
                r = self.formatNumber(val.real)
                i = self.formatNumber(val.imag)
                v = '{} j{}'.format(r, i)
            else:
                m = math.sqrt(val.real**2 + val.imag**2)
                a = math.atan2(val.imag, val.real)

                # a varia de -pi a +pi.... TODO normalizar

                # FIXME a pode ser rad ou deg

                v = '{} \u03d5{}'.format(self.formatNumber(m), self.formatNumber(a))

            return v

        if self.format == 'sci':
            v = '{0:.{pre}E}'.format(val, pre=self.precision)
            # v = a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]

        elif self.format == 'eng':
            s = 1 if val >= 0 else -1
            t = '{0:.{pre}E}'.format(abs(val), pre=self.precision+2)
            n = t.split('E')[0].replace('.', '')
            e = int(t.split('E')[1])
            multiplier = ['a', 'p', 'n', 'µ', 'm', sep, 'k', 'M', 'G', 'T', 'E']
            d = e%3
            e = 3*(e//3)
            if e >= -15 and e <= 15:
                m = multiplier[e//3+5]
            else:
                m = str(e)
            # FIXME o arredondamento nao esta funcionando....
            v = '{:d}.{}{}{}'.format(s*int(n[:1+d]), n[1+d:1+d+self.precision], sep, m)

        else:
            v = '{0:.{pre}f}'.format(val, pre=self.precision)

        return v

    def updateBases(self):
        self.edt_bin.setText(bin(int(self.getX())))
        self.edt_oct.setText(oct(int(self.getX())))
        self.edt_hex.setText(hex(int(self.getX())))
        d = pack('>fd', self.getX(), self.getX())
        self.edt_float.setText('{0[0]:02X}.{0[1]:02X}.{0[2]:02X}.{0[3]:02X}'.format(d))
        self.edt_double.setText('{0[0]:02X}.{0[1]:02X}.{0[2]:02X}.{0[3]:02X}.{0[4]:02X}.{0[5]:02X}.{0[6]:02X}.{0[7]:02X}'.format(d[4:]))

    def updateConverter(self):
        v = self.getX()
        c, u = self.converter.convert(v,
                                      self.cmb_quantity.currentIndex(),
                                      self.list_conv_left.currentRow(),
                                      self.list_conv_right.currentRow())
        self.btn_conv_right.setText('{} {}'.format(self.formatNumber(c, ''), u))
        c, u = self.converter.convert(v,
                                      self.cmb_quantity.currentIndex(),
                                      self.list_conv_right.currentRow(),
                                      self.list_conv_left.currentRow())
        self.btn_conv_left.setText('{} {}'.format(self.formatNumber(c, ''), u))

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
        self._on_edt_equations__textChanged()

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
        self.updateStack()

    def _on_btn_format__clicked(self):
        if self.format == 'def':
            self.format = 'sci'
        elif self.format == 'sci':
            self.format = 'eng'
        else:
            self.format = 'def'

        self.btn_format.setText('{} ({:d})'.format(self.format.title(), self.precision))
        self.updateAll()
        self.populateConstants()

    def _on_btn_format__value_changed(self, val):
        self.precision = val
        self.btn_format.setText('{} ({:d})'.format(self.format.title(), self.precision))
        self.updateAll()
        self.populateConstants()

    def _on_btn_coord__clicked(self):
        self.coordinate = 'cart' if self.coordinate == 'pol' else 'pol'

        self.btn_coord.setText(self.coordinate.title())
        self.updateStack()

    # def _on_btn_solver__clicked(self):
    #     if not self.console:
    #         self.console = ConsoleForm()
    #     self.console.show()

    _funcoes = '`btn_f_.+`'
    def _when_funcoes__clicked(self):
        # print(self.sender().objectName())

        op = self.sender().objectName().split('_')[2]

        if self.editing:
            if op == 'minus':
                if self.entry_str[0] == '-':
                    self.entry_str = self.entry_str[1:]
                else:
                    self.entry_str = '-' + self.entry_str
                self.updateAll()
                return

            self.stack.append(self.entry_val)
            self.editing = False

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
                x, = self.pop()
                if isinstance(x, complex):
                    self.stack.append(x.real)
                    self.stack.append(x.imag)
                else:
                    self.stack.append(x)

            elif op == 'conjugate':
                x, = self.pop()
                if isinstance(x, complex):
                    self.stack.append(x.conjugate())
                else:
                    self.stack.append(x)

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
                x, y = self.pop(2)

                if not (isinstance(x, complex) or isinstance(y, complex)):
                    self.stack.append(complex(y, x))
                else:
                    self.stack.append(y)
                    self.stack.append(x)

        except IndexError:
            print('Index Error')
        except:
            raise

        self.updateAll()

    _avancadas = '`btn_s_.+`'
    def _when_avancadas__clicked(self):
        # print(self.sender().objectName())

        if self.editing:
            self.stack.append(self.entry_val)
            self.editing = False

        op = self.sender().objectName().split('_')[2]

        try:
            if op == 'root2':
                c, b, a = self.pop(3)

                d = b*b - 4 * a * c

                rd = math.sqrt(d) if d >= 0 else complex(0, math.sqrt(-d))

                self.stack.append((-b - rd) / (2*a))
                self.stack.append((-b + rd) / (2*a))

        # fatorial
        #  combinacao C(n,r) = n! / ( r! (n - r)! )
        # permutacao P(n,r) = n! / (n - r)!
        # random

        except IndexError:
            pass
            print('nhaca')
        except:
            raise

        self.updateAll()

    _constantes = '`btn_c_.+`'
    def _when_constantes__clicked(self):
        # print(self.sender().objectName())

        if self.editing:
            self.stack.append(self.entry_val)
            self.editing = False

        op = self.sender().objectName().split('_')[2]

        try:
            if op == 'pi':
                self.stack.append(3.14159265358979323846264338327950288)
            elif op == 'e':
                self.stack.append(2.71828182845904523536028747135266249)
            elif op == 'c':
                self.stack.append(299792458) # [m.s-1]
            elif op == 'G':
                self.stack.append(6.67408313131e-11) # [m3.kg−1.s−2]

        except IndexError:
            pass
            print('nhaca')
        except:
            raise

        self.updateAll()

    def _on_eq_scroll__valueChanged(self):
        self.edt_results.verticalScrollBar().setValue(self.eq_scroll.value())

    def _on_result_scroll__valueChanged(self):
        self.edt_equations.verticalScrollBar().setValue(self.result_scroll.value())

    def showError(self, text):
        self.lbl_error.setText(text)
        self.edt_results.clear()

    def _on_btn_posfix__clicked(self):
        if self.posfixMode:
            self.posfixMode = False
            self.btn_posfix.setText('Infix')
        else:
            self.posfixMode = True
            self.btn_posfix.setText('Posfix')

    def _on_edt_equations__textChanged(self):
        try:
            if self.posfixMode:
                r = rpnsolver.solve(self.edt_equations.toPlainText())
            else:
                r = solver.solve(self.edt_equations.toPlainText())

            txt = '''<html><head><style type="text/css">
 p {margin: 0px 0px; -qt-block-indent:0; text-indent:0px; white-space: pre-wrap; text-align: right;}
 body {font-family:'Courier New'; font-size:14pt; font-weight:400; font-style:normal;}
 </style></head><body>'''

            for v in r:
                if v[1] is not None:
                    # txt += '<p align="right">{:.5f}</p>'.format(v[1])
                    txt += '<p align="right">{}</p>'.format(self.formatNumber(v[1]))
                else:
                    txt += '<p align="right"> </p>'

            self.edt_results.setHtml(txt+'</body></html>')
            self.edt_results.verticalScrollBar().setValue(self.eq_scroll.value())
            self.lbl_error.setText('')

        except solver.VariableError as e:
            self.showError(self.tr('Undefined variable {}').format('AINDA NAO DEFINIDO!!'))
            print(e)

        except solver.LexError as e:
            self.showError(self.tr('Unknown character "{}" at line {:d}').format(e.args[0].value[0], e.args[0].lineno+1))

        except solver.ConstantError as e:
            self.showError(self.tr('Undefined constant {} in line {:d}').format(e.args[0][0], e.args[0][1]))

        except solver.GrammarError as e:
            self.showError(self.tr('Syntax error at line {:d}').format(e.args[0].lineno+1))

        except:
            self.lbl_error.setText(self.tr('Unknown error!!'))

    def _on_btn_clear__clicked(self):
        self.edt_equations.setHtml('')

    def _on_btn_copy__clicked(self):
        r = self.edt_results.toPlainText().split('\n')
        e = self.edt_equations.toPlainText().split('\n')
        t = ''
        for i, l in enumerate(e):
            rr = r[i] if i < len(r) else ''
            t+= '{: >16s} <-- {}\n'.format(rr, l)

        cb = QtGui.QApplication.clipboard()
        cb.setText(t)

    # _selectors = '`btn_show_.+`'
    # def _when_selectors__clicked(self):
    #     op = self.sender().objectName().split('_')[2]

    #     if op == 'rpn':
    #         self.boxRPN.setVisible(not self.boxRPN.isVisible())
    #     elif op == 'solver':
    #         self.boxSolver.setVisible(not self.boxSolver.isVisible())
    #     elif op == 'helpers':
    #         self.boxHelpers.setVisible(not self.boxHelpers.isVisible())

    #     # TODO quando ficar somente a stack deve travar a largura!

        # rpn = self.boxRPN.isVisible()
        # solver = self.boxSolver.isVisible()
        # helper = self.boxHelpers.isVisible()
        # if rpn and not (solver or helper):
        #     print(self.size())
        #     self.resize(100, self.size().height())

        # print(self.size())

    def populateConstants(self):
        constants = (
            ('Arquimeds (𝛑)', 3.14159265358979323846264338327950288, ''),
            ('Euler (e)', 2.71828182845904523536028747135266249, ''),
            ('c', 299792458, 'm/s'),
            ('G', 6.67408313131e-11, 'm³/(kg . s²)'),
            ('golden ratio (𝛗)', 1.6180339887498948, '')
        )
        self.tbl_constants.setRowCount(len(constants))
        # self.tbl_constants.setColumnCount(3)
        for line, cc in enumerate(constants):
            print(line, cc)
            self.tbl_constants.setItem(line, 0, QtGui.QTableWidgetItem(cc[0]))
            self.tbl_constants.setItem(line, 1, QtGui.QTableWidgetItem(self.formatNumber(cc[1])))
            self.tbl_constants.setItem(line, 2, QtGui.QTableWidgetItem(cc[2]))


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
