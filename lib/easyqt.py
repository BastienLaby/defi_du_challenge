# -*- coding: utf-8 -*-

# @package easyqt
# created on 10/08/2016 by bastien.laby
# last updated on 29/12/2016

import sys
import os
import platform

import logging
log = logging.Logger('info')

from PySide import QtCore, QtGui
from PySide.QtGui import QPalette, QColor
from PySide.QtCore import Qt


class EasyBase(object):
    '''
    '''

    def __init__(self, **signals):
        self.signals = signals
        for signalName, callback in signals.iteritems():
            if signalName == 'objectName':
                self.setObjectName(callback)
                continue
            try:
                getattr(self, signalName).connect(callback)
            except AttributeError:
                log.warning('Signal %s is not a builtin signal for the type %s', signalName, type(self))
                raise


class EasyApplication(QtGui.QApplication):
    '''
    '''

    def __init__(self):
        super(EasyApplication, self).__init__(sys.argv)


class EasyWindow(QtGui.QMainWindow, EasyBase):
    '''
    '''

    def __init__(self, show=True, title='EasyQT Window', **signals):
        super(EasyWindow, self).__init__(**signals)
        if show:
            self.show()
        self.setWindowTitle(title)


class EasyWidget(QtGui.QWidget, EasyBase):
    '''
    '''

    def __init__(self, layoutType=None, layout='VBoxLayout', **signals):
        super(EasyWidget, self).__init__(**signals)
        if layoutType:
            log.warning('EasyWidget : layoutType parameter is deprecated. Use "layout" parameter instead')
            self.layout = layoutType()
        if layout == 'VBoxLayout':
            self.layout = QtGui.QVBoxLayout()
        elif layout == 'HBoxLayout':
            self.layout = QtGui.QHBoxLayout()
        elif layout == 'GridLayout':
            self.layout = QtGui.QGridLayout()
        else:
            raise Exception('EasyWidget : Unknow layout %s' % layout)
        self.setLayout(self.layout)

    def addWidget(self, widget, row=-1, col=-1, rowSpan=1, colSpan=1, stretch=0):
        '''
        Add the given widget to the current layout.
        If the widget layout is a QGridLayout, the parameters "row" and "col" must be passed.
        '''

        if isinstance(widget, str):
            widget = QtGui.QLabel(widget)

        if isinstance(self.layout, QtGui.QGridLayout):
            self.layout.addWidget(widget, row, col, rowSpan, colSpan, stretch=stretch)
        else:
            self.layout.addWidget(widget)

    def addWidgets(self, *widgets):
        '''
        Add several widgets to the current layout.
        QGridLayout is not supported for this function.
        '''
        if isinstance(self.layout, QtGui.QGridLayout):
            raise Exception('GridLayout is not supported with addWidgets(*widgets) function')
        for widget in widgets:
            self.addWidget(widget)


class EasyPushButton(QtGui.QPushButton, EasyBase):
    '''
    A proxy class used to simplify the widget/layout management.
    '''
    def __init__(self, text, **signals):
        '''
        '''
        super(EasyPushButton, self).__init__(**signals)
        self.setText(text)


class EasyLabel(QtGui.QLabel, EasyBase):
    '''
    A proxy class used to simplify the widget/layout management.
    '''
    def __init__(self, text, **signals):
        '''
        '''
        super(EasyLabel, self).__init__(**signals)
        self.setText(text)



def callback():
    print 'callback'


if __name__ == '__main__':
    app = EasyApplication()
    window = EasyWindow()

    centralWidget = EasyWidget(layout='GridLayout')
    window.setCentralWidget(centralWidget)

    vWidget = EasyWidget(layout='VBoxLayout')
    centralWidget.addWidget(vWidget, 0, 0)
    for i in range(5):
        vWidget.addWidget(EasyPushButton(str(i), clicked=callback))

    hWidget = EasyWidget(layout='HBoxLayout')
    centralWidget.addWidget(hWidget, 0, 1)
    hWidget.addWidgets(*[EasyPushButton(str(i), clicked=callback) for i in range(3)])


    sys.exit(app.exec_())
