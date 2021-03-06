#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import sys
from console_ui import *
import smartside.signal as smartsignal
import solver


__author__ = 'Gustavo Vargas <xgvargas@gmail.com>'
__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)


class ConsoleForm(QtGui.QWidget, Ui_form_console, smartsignal.SmartSignal):
    def __init__(self, parent=None):
        super(ConsoleForm, self).__init__(parent)
        self.setupUi(self)

        self.eq_scroll = self.edt_equations.verticalScrollBar()

        self.auto_connect()

        self.lbl_error.setText('')

    def _on_eq_scroll__valueChanged(self):
        self.edt_results.verticalScrollBar().setValue(self.eq_scroll.value())

    def showError(self, text):
        self.lbl_error.setText(text)
        self.edt_results.clear()

    def _on_edt_equations__textChanged(self):
        try:
            r = solver.solve(self.edt_equations.toPlainText())
            txt = '''<html><head><style type="text/css">
 p {margin: 0px 0px; -qt-block-indent:0; text-indent:0px; white-space: pre-wrap; text-align: right;}
 body {font-family:'Courier New'; font-size:14pt; font-weight:400; font-style:normal;}
 </style></head><body>'''

            for v in r:
                if v[1] is not None:
                    txt += '<p align="right">{:.5f}</p>'.format(v[1])
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
            t+= '{: >16s} =: {}\n'.format(rr, l)

        cb = QtGui.QApplication.clipboard()
        cb.setText(t)


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    window = ConsoleForm()
    window.show()
    #window.print_all_signals()
    sys.exit(app.exec_())
