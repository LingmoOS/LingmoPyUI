from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class LingmoRectangle(QWidget):
    def __init__(self,parent:QWidget,x=0,y=0,width=10,height=10):
        super().__init__(parent)
        self.parent=parent
        self._color=QColor(255,255,255,255)
        self._radius=[0,0,0,0]
        self.colorChanged=Signal(type(self._color))
        self.radiusChanged=Signal(type(self._radius))
        self.setGeometry(x,y,width,height)
        parent.connect(self.colorChanged,parent,lambda:parent.update())
        parent.connect(self.radiusChanged,parent,lambda:parent.update())
    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, new_value):
        if self._color != new_value:
            self._color = new_value
            self.colorChanged.emit(new_value)
    @property
    def radius(self):
        return self._radius
    @radius.setter
    def radius(self, new_value):
        if self._radius != new_value:
            self._radius = new_value
            self.radiusChanged.emit(new_value)
    def update(self):
        self.setStyleSheet('color: '+self._color.name()+';')
        self.setStyleSheet('border-radius: '+self._radius+';')
        super().update()