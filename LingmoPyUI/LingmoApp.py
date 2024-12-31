from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

import sys
import os

from . import LingmoIconDef

windowIcon=''
locale=QLocale()
launcher=QObject()
userSystemAppBar=False
_app=QApplication([])
_translator=QTranslator(QApplication.instance())
QApplication.installTranslator(_translator)
uiLanguages=locale.uiLanguages()
for i in uiLanguages:
    basename='lingmoui_'+QLocale(i).name()
    if _translator.load(os.path.dirname(sys.argv[0])+basename):
        _app.translate()
        break

def run():
    _app.exec()

def iconData(keyword):
    arr=QJsonArray()
    for i in LingmoIconDef.__dict__:
        if (keyword in i) or keyword=='':
            value=QJsonValue({'name':i,'icon':LingmoIconDef.__dict__[i]})
            arr.append(value)
            