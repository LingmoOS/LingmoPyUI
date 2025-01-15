from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from . import LingmoTools
from ctypes import windll
from ctypes.wintypes import *

dwmapi=windll.dwmapi
user32=windll.user32
timerDelay=10
widgetCount=0

class LingmoFrameless(QObject):
	def __init__(self,parent:QWidget,appbar,maximizeButton,minimizeButton,closeButton,
                topmost=False,disabled=False,fixsize=False,effect='normal',effective=False,
                availableEffects=[],isDarkMode=False,useSystemEffect=False):
		super().__init__(parent)
		self.appbar=appbar	
		self.maximizeButton=maximizeButton
		self.minimizeButton=minimizeButton
		self.closeButton=closeButton	
		self.parent().setTopmost(topmost)
		self.parent().setDisabled(disabled)
		self.fixSize=fixsize
		self.effect=effect
		self.effective=effective
		self.availableEffects=availableEffects
		self.isDarkMode=isDarkMode
		self.useSystemEffect=useSystemEffect
		self.hitTestList=[]
		self.edges=0
		self.clickTimer=0
		self.margins=8
		self.current=0
		self.componentComplete()
	def onDestruction(self):
		QApplication.instance().removeNativeEventFilter(self)
	def componentComplete(self):
		if not self.isEnabled():
			return 
		w=self.parent().width()
		h=self.parent().height()
		self.current=self.parent().winId()
		if LingmoTools.isLinux():
			self.parent().setWindowFlag(Qt.WindowType.CustomizeWindowHint,True)
		self.parent().setWindowFlag(Qt.WindowType.FramelessWindowHint,True)
		self.setProperty('__borderWidth',1)
		self.parent().installEventFilter(self)
		QApplication.instance().installNativeEventFilter(self)
		if self.maximizeButton:
			self.setHitTestVisible(self.maximizeButton)
		if self.minimizeButton:
			self.setHitTestVisible(self.minimizeButton)
		if self.closeButton:
			self.setHitTestVisible(self.closeButton)
		appbarHeight=self.appbar.height()
		h=round(h+appbarHeight)
		if self.fixSize:
			self.parent().setMaximumSize(w,h)
			self.parent().setMinimumSize(w,h)
		else:
			self.parent().setMaximumHeight(self.parent().maximumHeight()+appbarHeight)
			self.parent().setMinimumHeight(self.parent().minimumHeight()+appbarHeight)
		self.parent().resize(w,h)
	def nativeEventFilter(self,message,result):
		return False
	def showSystemMenu(self,point):
		pass
	def hitAppBar(self):
		for i in range(len(self.hitTestList)):
			if i.isHovered():
				return False
		return self.appbar.isHovered()
	def hitMaximizeButton(self):
		return self.maximizeButton.isHovered()
	def updateCursor(self,edges):
		if edges==0:
			self.parent().setCursor(Qt.CursorShape.ArrowCursor)
		elif edges==Qt.Edge.LeftEdge or self.edges==Qt.Edge.RightEdge:
			self.parent().setCursor(Qt.CursorShape.SizeHorCursor)
		elif edges==Qt.Edge.TopEdge or self.edges==Qt.Edge.BottomEdge:
			self.parent().setCursor(Qt.CursorShape.SizeVerCursor)
		elif (edges==Qt.Edge.LeftEdge|self.edges==Qt.Edge.TopEdge)or(edges==Qt.Edge.RightEdge|self.edges==Qt.Edge.BottomEdge):
			self.parent().setCursor(Qt.CursorShape.SizeFDiagCursor)
		elif (edges==Qt.Edge.RightEdge|self.edges==Qt.Edge.TopEdge)or(edges==Qt.Edge.LeftEdge|self.edges==Qt.Edge.BottomEdge):
			self.parent().setCursor(Qt.CursorShape.SizeBDiagCursor)
	def setHitTestVisible(self,val):
		if not(val in self.hitTestList):
			self.hitTestList.append(val)
	def setWindowTopMost(self,topmost):
		self.parent().setWindowFlag(Qt.WindowType.WindowStaysOnTopHint,topmost)
	def eventFilter(self,obj,ev:QEvent):
		if ev.type()==QEvent.Type.MouseButtonPress:
			if self.edges!=0:
				if isinstance(ev,QMouseEvent):
					if ev.button()==Qt.MouseButton.LeftButton:
						self.updateCursor(self.edges)
						self.parent().startSystemResize(self.edges)
			else:
				if self.hitAppBar():
					clickTimer=QDateTime.currentMSecsSinceEpoch()
					offset=clickTimer-self.clickTimer
					self.clickTimer=clickTimer
					if offset<300:
						if self.parent().isMaximized():
							self.parent().showNormal()
						else:
							self.parent().showMaximized()
					else:
						self.parent().startSystemMove()
		elif ev.type()==QEvent.Type.MouseButtonRelease:
			self.edges=0
		elif ev.type()==QEvent.Type.MouseMove:
			if not (self.parent().isMaximized() or self.parent().isFullScreen()):
				if not self.fixSize:
					if isinstance(ev,QMouseEvent):
						p=ev.position().toPoint()
						if p.x()>=self.margins and p.x()<=self.parent().width()-self.margins and \
							p.y()>=self.margins and p.y()<=self.parent().height()-self.margins:
							self.edges=0
							self.updateCursor(self.edges)
						else:
							self.edges=0
							if p.x()<self.margins:
								self.edges |= Qt.Edge.LeftEdge
							if p.x()>self.parent().width()-self.margins:
								self.edges |= Qt.Edge.RightEdge
							if p.y()<self.margins:
								self.edges |= Qt.Edge.TopEdge
							if p.y()>self.parent().height()-self.margins:
								self.edges |= Qt.Edge.BottomEdge
		return super().eventFilter(obj,ev)
    
