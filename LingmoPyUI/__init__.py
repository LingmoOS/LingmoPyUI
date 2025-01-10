version='1.0.0'
from enum import auto
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from . import LingmoAccentColor
from . import LingmoApp
from . import LingmoColor
from . import LingmoDefines
from .LingmoFrameless import LingmoFrameless
from . import LingmoIconDef
from .LingmoRectangle import LingmoRectangle
from . import LingmoTextStyle
from . import LingmoTheme
from . import LingmoTools
from . import LingmoUnits
import math
timerDelay=0
widgetCount=0
class LingmoAnimation(QVariantAnimation):
	Variable=1
	Callable=2
	def __init__(self,obj: object,attr: str,updateType=Variable):
		super().__init__()
		self.obj=obj
		self.attr=attr
		self.precision=1000
		self.updateType=updateType
	def setStartValue(self, value):
		return super().setStartValue(round(value*self.precision))
	def setEndValue(self, value):
		return super().setEndValue(round(value*self.precision))
	def updateCurrentValue(self, value):
		if self.updateType==self.Variable:
			self.obj.__setattr__(self.attr,value/self.precision)
		else:
			(self.obj.__getattr__(self.attr))(value/self.precision)
class LingmoFrame(QFrame):
	pressed=Signal()
	released=Signal()
	hovered=Signal()
	left=Signal()
	rightPressed=Signal()
	rightReleased=Signal()
	def __init__(self,parent=None,show=True):
		global widgetCount
		super().__init__(parent)
		self.timer=QTimer()
		self.timer.timeout.connect(self.updateEvent)
		self.timer.timeout.connect(self.__update__)
		self.timer.start(timerDelay)
		if show:
			self.show()
		self.styleSheets={}
		widgetCount+=1
		self.setObjectName('LingmoWidget'+str(widgetCount))
		self.ispressed=False
	def __update__(self):
		self.update()
		styleSheetString='QFrame#'+self.objectName()+'{'
		for i in self.styleSheets:
			styleSheetString+=i+': '+self.styleSheets[i]+';'
		styleSheetString+='}'
		self.setStyleSheet(styleSheetString)
	def updateEvent(self):
		pass
	def addStyleSheet(self,name,style):
		if isinstance(style,int) or isinstance(style,float):
			style=str(style)
		if isinstance(style,QColor):
			style=style.name(QColor.NameFormat.HexArgb)
		self.styleSheets[name]=style
	def isHovered(self):
		return self.underMouse()
	def mousePressEvent(self, event):
		if self.isEnabled():
			self.setFocus()
			if event.button()==Qt.MouseButton.LeftButton:
				self.pressed.emit()
			if event.button()==Qt.MouseButton.RightButton:
				self.rightPressed.emit()
			self.ispressed=True
	def mouseReleaseEvent(self, event):
		if self.isEnabled():
			if event.button()==Qt.MouseButton.LeftButton:
				self.released.emit()
			if event.button()==Qt.MouseButton.RightButton:
				self.rightReleased.emit()
			self.ispressed=False
	def enterEvent(self, event):
		if self.isEnabled():
			self.hovered.emit()
	def leaveEvent(self, event):
		if self.isEnabled():
			self.left.emit()
	def isPressed(self):
		return self.ispressed
class LingmoLabel(QLabel):
	def __init__(self,parent=None,show=True,autoAdjust=True):
		global widgetCount
		super().__init__(parent)
		self.timer=QTimer()
		self.timer.timeout.connect(self.updateEvent)
		self.timer.timeout.connect(self.__update__)
		self.timer.start(timerDelay)
		if show: 
			self.show()
		self.styleSheets={}
		self.setAlignment(Qt.AlignmentFlag.AlignCenter)
		widgetCount+=1
		self.setObjectName('LingmoWidget'+str(widgetCount))
		self.autoAdjust=autoAdjust
	def __update__(self):
		self.update()
		styleSheetString='QLabel#'+self.objectName()+'{'
		for i in self.styleSheets:
			styleSheetString+=i+': '+self.styleSheets[i]+';'
		styleSheetString+='}'
		self.setStyleSheet(styleSheetString)
		if self.autoAdjust:
			self.adjustSize()
	def updateEvent():
		pass
	def addStyleSheet(self,name,style):
		if isinstance(style,int) or isinstance(style,float):
			style=str(style)
		if isinstance(style,QBrush):
			style=style.color()
		if isinstance(style,QColor):
			style=style.name(QColor.NameFormat.HexArgb)
		self.styleSheets[name]=style
	def isHovered(self):
		return self.underMouse()
class LingmoAcrylic(LingmoFrame):
	def __init__(self,parent=None,show=True,tintColor=QColor(255,255,255,255),luminosity=0.01,noiseOpacity=0.02,target:QWidget=None,blurRadius=32,targetRect: QRect =None):
		super().__init__(parent,show)
		self.tintColor=tintColor
		self.luminosity=luminosity
		self.noiseOpacity=noiseOpacity
		self.target=target
		self.blurRadius=blurRadius
		self.targetRect=self.rect()if targetRect==None else targetRect
		self.blurWidget=LingmoFrame(self)
		self.blurEffect=QGraphicsBlurEffect(self.blurWidget)
		self.blurWidget.setGeometry(self.targetRect)
		self.luminosityWidget=LingmoFrame(self)
		self.luminosityWidget.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
		self.tintWidget=LingmoFrame(self)
		self.tintWidget.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
		self.imageWidget=LingmoLabel(self)
		self.imageWidget.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
		self.imageWidget.setPixmap('./Image/noise.png')
		self.imageWidget.addStyleSheet('background-repeat','repeat')
	def updateEvent(self):
		self.blurEffect.setBlurRadius(self.blurRadius)
		self.blurWidget.setGeometry(self.targetRect)
		self.luminosityWidget.addStyleSheet('background-color',QColor(1,1,1,self.luminosity*255))
		self.tintWidget.addStyleSheet('background-color',self.tintColor)
		self.imageWidget.setWindowOpacity(self.noiseOpacity)
	def setTintColor(self,val):
		self.tintColor=val
	def setTintOpacity(self,val):
		self.tintOpacity=val
	def setLuminosity(self,val):
		self.luminosity=val
	def setNoiseOpacity(self,val):
		self.noiseOpacity=val
	def setTarget(self,val):
		self.target=val
	def setBlurRadius(self,val):
		self.blurRadius=val
	def setTargetRect(self,val):
		self.targetRect=val
class LingmoAppBar(LingmoFrame):
	def __init__(self,parent=None,show=True):
		super().__init__(parent,show)
	def updateEvent(self):
		pass
class LingmoButton(LingmoFrame):
	def __init__(self,parent=None,show=True,content='',
	normalColor=QColor(62,62,62,255)if LingmoTheme.instance.dark() else QColor(254,254,254,255),
	hoverColor=QColor(68,68,68,255)if LingmoTheme.instance.dark() else QColor(246,246,246,255),
	disableColor=QColor(59,59,59,255)if LingmoTheme.instance.dark() else QColor(251,251,251,255),
	dividerColor=QColor(80,80,80,255)if LingmoTheme.instance.dark() else QColor(233,233,233,255),
	textNormalColor=QColor(255,255,255,255)if LingmoTheme.instance.dark() else QColor(0,0,0,255),
	textPressedColor=QColor(162,162,162,255)if LingmoTheme.instance.dark() else QColor(96,96,96,255),
	textDisabledColor=QColor(131,131,131,255)if LingmoTheme.instance.dark() else QColor(160,160,160,255),clickShadowChange=True,autoResize=True):
		super().__init__(parent,show)
		self.content=content
		self.normalColor=normalColor
		self.hoverColor=hoverColor
		self.disabledColor=disableColor
		self.dividerColor=dividerColor
		self.textNormalColor=textNormalColor
		self.textPressedColor=textPressedColor
		self.textDisabledColor=textDisabledColor
		self.horizontalPadding=12
		self.verticalPadding=0
		self.ctrlBg=LingmoControlBackground(self,LingmoTheme.instance._roundWindowRadius)
		self.ctrlBg.setGeometry(self.horizontalPadding,self.verticalPadding,self.width()-2*self.horizontalPadding,self.height()-2*self.verticalPadding)
		self.setFont(LingmoTextStyle.body)
		self.setFocusPolicy(Qt.FocusPolicy.TabFocus)
		self.focusRect=LingmoFocusRectangle(self.ctrlBg,radius=4)
		self.focusRect.resize(self.ctrlBg.size())
		self.contentText=LingmoText(self)
		self.contentText.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.contentText.setFont(self.font())
		self.clickShadowChange=clickShadowChange
		self.autoResize=autoResize
	def updateEvent(self):
		if self.isEnabled():
			if self.isPressed():
				self.contentText.setColor(self.textPressedColor)
			else:
				self.contentText.setColor(self.textNormalColor)
		else:
			self.contentText.setColor(self.textDisabledColor)
		self.ctrlBg.setColor((self.hoverColor if self.isHovered() else self.normalColor)if self.isEnabled() else self.disabledColor)
		if self.clickShadowChange: self.ctrlBg.setShadow((not self.isPressed())and self.isEnabled())
		self.focusRect.setVisible(self.hasFocus())
		self.contentText.setText(self.content)
		self.contentText.move(10+12,self.height()/2-self.contentText.height()/2)
		self.contentText.raise_()
		if self.autoResize:
			self.ctrlBg.resize(self.contentText.width()+20,self.height())
		self.resize(self.ctrlBg.width()+2*self.horizontalPadding,self.ctrlBg.height()+2*self.verticalPadding)
	def setContent(self,val):
		self.content=val
	def setClickShadowChange(self,val):
		self.clickShadowChange=val
	def setAutoResize(self,val):
		self.autoResize=val
class LingmoClip(LingmoFrame):
	def __init__(self,parent=None,show=True,radius=0):
		super().__init__(parent,show)
		self.color=QColor(0,0,0,0)
		self.effect=QGraphicsOpacityEffect(self)
		self.effect.setOpacity(0.5)
		self.setGraphicsEffect(self.effect)
		self.radius=radius
	def updateEvent(self):
		self.addStyleSheet('border-radius',self.radius)
	def setRadius(self,val):
		self.radius=val
class LingmoControlBackground(LingmoFrame):
	def __init__(self,parent=None,show=True,radius: int = 4,shadow: bool = True,color = QColor(42,42,42,255) if LingmoTheme.instance.dark() else QColor(254,254,254,255),borderWidths=[1,1,1,1]):
		super().__init__(parent,show)
		self.radius=radius
		self.shadow=shadow
		self.color=color
		self.borderColor=QColor(48,48,48,255) if LingmoTheme.instance.dark() else QColor(188,188,188,255)
		self.startColor=QColor.lighter(self.borderColor,125)
		self.endColor=self.borderColor if self.shadow else self.startColor
		self.borderWidths=borderWidths
		self.rectBorder=LingmoFrame(self)
		self.rectBack=LingmoFrame(self)
		self.borderColorUnsetted=True
	def updateEvent(self):
		self.rectBack.addStyleSheet('border-radius',self.radius)
		self.rectBack.addStyleSheet('background-color',self.color)
		self.rectBack.setGeometry(self.borderWidths[0],self.borderWidths[1],self.width()-self.borderWidths[0]-self.borderWidths[2],self.height()-self.borderWidths[1]-self.borderWidths[3])
		self.borderColor=(QColor(48,48,48,255) if LingmoTheme.instance.dark() else QColor(188,188,188,255))if self.borderColorUnsetted else self.borderColor
		self.startColor=QColor.lighter(self.borderColor,125)
		self.endColor=self.borderColor if self.shadow else self.startColor
		self.rectBorder.addStyleSheet('background-color','''qlineargradient(x1:0 , y1:0 , x2:0 , y2:1,
                stop:0    rgba(%d,%d,%d,%d),
                stop:%d   rgba(%d,%d,%d,%d),
                stop:1.0  rgba(%d,%d,%d,%d))'''%(self.startColor.red(),self.startColor.green(),self.startColor.blue(),self.startColor.alpha(),
												1-3/self.height(),self.startColor.red(),self.startColor.green(),self.startColor.blue(),self.startColor.alpha(),
												self.endColor.red(),self.endColor.green(),self.endColor.blue(),self.endColor.alpha()))
		self.rectBorder.addStyleSheet('border-radius',self.radius)
		self.rectBorder.resize(self.size())
	def setColor(self,val):
		self.color=val
	def setRadius(self,val):
		self.radius=val
	def setShadow(self,val):
		self.shadow=val
	def setBorderWidths(self,val):
		self.borderWidths=val
	def setLeftMargin(self,val):
		self.borderWidths[0]=val
	def setTopMargin(self,val):
		self.borderWidths[1]=val
	def setRightMargin(self,val):
		self.borderWidths[2]=val
	def setButtomMargin(self,val):
		self.borderWidths[3]=val
	def setBorderWidth(self,val):
		self.borderWidths=[val,val,val,val]
	def setBorderColor(self,val):
		self.borderColor=val
		self.borderColorUnsetted=False
class LingmoDropDownBox(LingmoButton):
	def __init__(self,parent=None,show=True,content=''):
		super().__init__(parent,show,autoResize=False,content=content)
		self.icon=LingmoIcon(LingmoIconDef.ChevronDown,self,iconSize=15,autoAdjust=True)
		self.menu=LingmoMenu(autoResize=False)
		self.menu.showed.connect(self.onAboutToShow)
		self.menu.hided.connect(self.onAboutToHide)
		self.pressed.connect(self.showMenu)
		self.parentWidget().pressed.connect(self.hideMenu)
	def updateEvent(self):
		super().updateEvent()
		self.icon.move(self.ctrlBg.x()+self.ctrlBg.width()-20,self.height()/2-self.icon.height()/2)
		self.menu.background.resize(self.ctrlBg.width(),self.menu.background.height())
		self.ctrlBg.resize(self.contentText.x()+self.contentText.width()+self.icon.width(),self.height())
	def showMenu(self):
		if self.menu.count() and not self.menu.isVisible():
			pos=self.ctrlBg.mapToGlobal(QPoint(0,0))
			containerHeight=self.menu.background.height()
			if self.window().height()>pos.y()+self.height()+containerHeight:
				self.menu.setPosition(self.mapToGlobal(QPoint(self.ctrlBg.x()/2,self.height())))
			elif pos.y()>containerHeight:
				self.menu.setPosition(self.mapToGlobal(QPoint(self.ctrlBg.x()/2,-containerHeight)))
			else:
				self.menu.setPosition(self.mapToGlobal(QPoint(self.ctrlBg.x()/2,self.window().height()-(pos.y()+containerHeight))))
			self.menu.showMenu()
	def hideMenu(self):
		if not self.isHovered():
			self.menu.hideMenu()
	def addItem(self,item):
		self.menu.addItem(item)
	def onAboutToShow(self):
		self.icon.setIconSource(LingmoIconDef.ChevronUp)
	def onAboutToHide(self):
		self.icon.setIconSource(LingmoIconDef.ChevronDown)
class LingmoFilledButton(LingmoFrame):
	def __init__(self,parent=None,show=True,content=''):
		super().__init__(parent,show)
		self.content=content
		self.normalColor=LingmoTheme.instance.primaryColor
		self.hoverColor=self.normalColor.darker(110)if LingmoTheme.instance.dark() else self.normalColor.lighter(110)
		self.disableColor=QColor(82,82,82,255)if LingmoTheme.instance.dark()else QColor(199,199,199,255)
		self.pressedColor=self.normalColor.darker(120)if LingmoTheme.instance.dark() else self.normalColor.lighter(120)
		self.textColor=(QColor(173,173,173,255)if not self.isEnabled() else QColor(0,0,0,255))if LingmoTheme.instance.dark() else QColor(255,255,255,255)
		self.setFocusPolicy(Qt.FocusPolicy.TabFocus)
		self.horizontalPaddding=12
		self.verticalPadding=0
		self.background=LingmoControlBackground(self)
		self.focusRect=LingmoFocusRectangle(self.background,radius=4)
		self.focusRect.resize(self.background.size())
		self.contentText=LingmoText(self)
		self.contentText.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.contentText.setFont(self.font())
	def updateEvent(self):
		if self.isEnabled():
			if self.isPressed():
				self.bgColor=self.pressedColor
			elif self.isHovered():
				self.bgColor=self.hoverColor
			else:
				self.bgColor=self.normalColor
		else:
			self.bgColor=self.disableColor
		self.contentText.setColor(self.textColor)
		self.background.setColor(self.bgColor)
		self.background.setRadius(LingmoTheme.instance._roundWindowRadius)
		self.background.setBorderWidth(1 if self.isEnabled() else 0)
		self.background.setBorderColor(self.normalColor.darker(120)if self.isEnabled() else self.disableColor)
		self.focusRect.setVisible(self.hasFocus())
		self.contentText.setText(self.content)
		self.contentText.move(self.width()/2-self.contentText.width()/2,
						self.height()/2-self.contentText.height()/2)
class LingmoFocusRectangle(LingmoFrame):
	def __init__(self,parent=None,show=True,color=QColor(0,0,0,0),borderWidth=2,radius=10,borderColor=QColor(255,255,255,255)if LingmoTheme.instance.dark() else QColor(0,0,0,255)):
		super().__init__(parent,show)
		self.color=color
		self.borderWidth=borderWidth
		self.radius=radius
		self.borderColor=borderColor
	def updateEvent(self):
		self.raise_()
		self.addStyleSheet('background-color',self.color)
		self.addStyleSheet('border-width',self.borderWidth)
		self.addStyleSheet('border-radius',self.radius)
		self.addStyleSheet('border-color',self.borderColor)
		self.addStyleSheet('border-style','solid')
		self.resize(self.parentWidget().size())
	def setColor(self,val):
		self.color=val
	def setBorderWidth(self,val):
		self.borderWidth=val
	def setRadius(self,val):
		self.radius=val
	def setBorderColor(self,val):
		self.borderColor=val
class LingmoIcon(LingmoLabel):
	def __init__(self,iconSource,parent=None,show=True,iconSize=20,iconColor: QColor=QColor(255,255,255,255)if LingmoTheme.instance.dark() else QColor(0,0,0,255),autoAdjust=False):
		super().__init__(parent,show,autoAdjust)
		self.iconSource=iconSource
		self.iconSize=iconSize
		self.iconColor=iconColor
		self.iconColor=(QColor(255,255,255,255)if self.isEnabled() else QColor(130,130,130,255))if LingmoTheme.instance.dark() else (QColor(0,0,0,255)if self.isEnabled() else QColor(161,161,161,255))
	def updateEvent(self):
		self.fontDatabase=QFontDatabase()
		self.fontDatabase.addApplicationFont('./LingmoPyUI/Font/FluentIcons.ttf')
		self.fontFamily=QFont(self.fontDatabase.applicationFontFamilies(0)[-1])
		self.fontFamily.setPixelSize(self.iconSize)
		self.setFont(self.fontFamily)
		self.setText(chr(self.iconSource))
		self.addStyleSheet('color',self.iconColor)
		self.setAlignment(Qt.AlignmentFlag.AlignCenter)
	def setIconSource(self,val):
		self.iconSource=val
	def setIconSize(self,val):
		self.iconSize=val
	def setIconColor(self,val):
		self.iconColor=val
class LingmoIconButton(LingmoFrame):
	IconOnly=Qt.ToolButtonStyle.ToolButtonIconOnly
	TextOnly=Qt.ToolButtonStyle.ToolButtonTextOnly
	TextUnderIcon=Qt.ToolButtonStyle.ToolButtonTextUnderIcon
	TextBesideIcon=Qt.ToolButtonStyle.ToolButtonTextBesideIcon
	def __init__(self,iconSource,parent=None,show=True,display=IconOnly,iconSize=20,radius=LingmoTheme.instance._roundWindowRadius,content='',
	hoverColor=LingmoTheme.instance.itemHoverColor,pressedColor=LingmoTheme.instance.itemPressColor,
	normalColor=LingmoTheme.instance.itemNormalColor,disableColor=LingmoTheme.instance.itemNormalColor,):
		super().__init__(parent,show)
		self.display=display
		self.iconSize=iconSize
		self.iconSource=iconSource
		self.radius=radius
		self.content=content
		self.hoverColor=hoverColor
		self.pressedColor=pressedColor
		self.normalColor=normalColor
		self.disableColor=disableColor
		self.background=LingmoFrame(self)
		self.focusRect=LingmoFocusRectangle(self.background)
		self.tooltip=LingmoToolTip(self.background,interval=1000,content=self.content)
		self.icon=LingmoIcon(iconSource,show=False)
		self.text=LingmoText(show=False)
		self.setFocusPolicy(Qt.FocusPolicy.TabFocus)
		self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.boxLayout=QBoxLayout(QBoxLayout.Direction.LeftToRight,self.background)
		self.background.setLayout(self.boxLayout)
		self.boxLayout.addWidget(self.icon)
		self.boxLayout.setContentsMargins(0,0,0,0)
		self.boxLayout.setSpacing(0)
		self.setFocusPolicy(Qt.FocusPolicy.TabFocus)
		self.iconColor=QColor()
		self.iconColorUnsetted=True
		self.horizontalPadding=8
		self.verticalPadding=8
	def updateEvent(self):
		self.tooltip.setDisabled(self.content==''or self.display!=self.IconOnly)
		self.tooltip.setContent(self.content)
		self.text.setText(self.content)
		self.color=QColor()
		self.textColor=LingmoTheme.instance.fontPrimaryColor
		if self.isEnabled():
			if self.isPressed():
				self.color=self.pressedColor
			elif self.isHovered():
				self.color=self.hoverColor
			else:
				self.color=self.normalColor
			if self.iconColorUnsetted: self.iconColor=QColor(255,255,255,255)if LingmoTheme.instance.dark() else QColor(0,0,0,255)
		else:
			self.color=self.disableColor
			if self.iconColorUnsetted: self.iconColor=QColor(130,130,130,255)if LingmoTheme.instance.dark() else QColor(161,161,161,255)
		self.icon.setIconColor(self.iconColor)
		self.icon.setIconSize(self.iconSize)
		self.text.setText(self.content)
		self.text.setFont(LingmoTextStyle.caption)
		self.background.addStyleSheet('border-radius',self.radius)
		self.background.addStyleSheet('background-color',self.color)
		self.text.addStyleSheet('color',self.textColor)
		self.background.adjustSize()
		self.background.move(self.horizontalPadding,self.verticalPadding)
		self.resize(self.background.width()+2*self.horizontalPadding,self.background.height()+2*self.verticalPadding)
		self.focusRect.setVisible(self.hasFocus())
	def setDisplay(self,val):
		self.display=val
		self.boxLayout.removeWidget(self.icon)
		self.boxLayout.removeWidget(self.text)
		if self.display!=self.TextOnly:
			self.boxLayout.addWidget(self.icon)
		if self.display!=self.IconOnly:
			self.boxLayout.addWidget(self.text)
		if self.display==self.TextBesideIcon:
			self.boxLayout.setDirection(QBoxLayout.Direction.LeftToRight)
		else:
			self.boxLayout.setDirection(QBoxLayout.Direction.TopToBottom)
	def setIconColor(self,val):
		self.iconColor=val
		self.iconColorUnsetted=False
	def setIconSize(self,val):
		self.iconSize=val
	def setIconBorderWidth(self,val):
		self.icon.resize(val,self.icon.height())
	def setIconBorderHeight(self,val):
		self.icon.resize(self.icon.width(),val)
	def setIconBorderSize(self,width,height):
		self.icon.resize(width,height)
	def setPaddings(self,hori,vert):
		self.horizontalPadding=hori
		self.verticalPadding=vert
class LingmoImageButton(LingmoFrame):
	def __init__(self,normalImage: str,parent=None,show=True,hoveredImage: str|None = None,pushedImage: str|None = None):
		super().__init__(parent,show)
		self.normalImage=normalImage
		self.hoveredImage=self.normalImage if hoveredImage==None else hoveredImage
		self.pushedImage=self.normalImage if pushedImage==None else pushedImage
		self.image=LingmoLabel(self)
		self.resize(12,12)
	def updateEvent(self):
		self.resize(self.size())
		if self.isPressed():
			self.image.setPixmap(QPixmap(self.pushedImage))
		elif self.isHovered():
			self.image.setPixmap(QPixmap(self.hoveredImage))
		else:
			self.image.setPixmap(QPixmap(self.normalImage))
class LingmoInfoBar(LingmoFrame):
	def __init__(self,parent=None,show=True):
		super().__init__(parent,show)
	def updateEvent(self):
		pass
class LingmoLoadingButton(LingmoButton):
	def __init__(self,parent=None,show=True,loading=False):
		super().__init__(parent,show,autoResize=False)
		self.loading=loading
		self.ring=LingmoProgressRing(self,strokeWidth=3)
		self.ringWidth=16
		self.ringWidthAnimation=LingmoAnimation(self,'ringWidth')
		self.ringWidthAnimation.setDuration(167)
		self.ringWidthAnimation.setEasingCurve(QEasingCurve.Type.OutCubic)
	def updateEvent(self):
		super().updateEvent()
		self.ring.resize(self.ringWidth,16)
		self.setDisabled(self.loading)
		self.ring.setVisible(self.ringWidth!=0)
		self.ring.move(self.contentText.x()+self.contentText.width()+6,self.height()/2-self.ring.height()/2)
		self.ctrlBg.resize(self.contentText.x()+self.contentText.width()+self.ringWidth,self.height())
	def setLoading(self,val):
		self.loading=val
		self.setRingWidth(16 if self.loading else 0)
	def setRingWidth(self,val):
		if LingmoTheme.instance._animationEnabled:
			self.ringWidthAnimation.setStartValue(self.ringWidth)
			self.ringWidthAnimation.setEndValue(val)
			self.ringWidthAnimation.start()
		else:
			self.ringWidth=val
class LingmoMenuItem(LingmoFrame):
	def __init__(self,iconSource=None,subMenu=None,content='',autoClose=True,checkable=False,mirrored=False):
		super().__init__(show=False)
		self.iconSpacing=5
		self.iconSource=iconSource
		self.iconSize=16
		self.mirrored=mirrored
		self.indicator=LingmoIcon(LingmoIconDef.CheckMark,parent=self,show=False,autoAdjust=True)
		self.arrow=LingmoIcon(LingmoIconDef.ChevronRightMed,parent=self,show=False,autoAdjust=True)
		self.text=LingmoText(self)
		self.subMenu=subMenu
		self.checked=False
		self.checkable=checkable
		self.pressed.connect(self.setChecked)
		self.padding=6
		self.iconWidth=24
		self.iconHeight=24
		self.content=content
		if self.iconSource:
			self.icon=LingmoIcon(self.iconSource,parent=self,iconSize=self.iconSize)
			self.icon.resize(self.iconWidth,self.iconHeight)
		else:
			self.icon=LingmoFrame(self)
		self.text.setText(self.content)
		self.autoClose=autoClose
		self.pressed.connect(self.onPressed)
		self.resize(self.icon.width()+self.text.width()+3*self.padding,max(self.icon.height(),self.text.height())+2*self.padding if self.isVisible()else 0)
		self.arrowPadding=self.arrow.width()+self.iconSpacing if self.subMenu else 0
		self.indicatorPadding=self.indicator.width()+self.iconSpacing if self.checkable else 0
		self.leftPadding= self.arrowPadding if self.mirrored else self.indicatorPadding
		self.rightPadding= self.indicatorPadding if self.mirrored else self.arrowPadding
	def updateEvent(self):
		if LingmoTheme.instance.dark():
			if self.isEnabled():
				if self.isPressed():
					self.textColor=QColor(162,162,162,255)
				else:
					self.textColor=QColor(255,255,255,255)
			else:
				self.textColor=QColor(131,131,131,255)
		else:
			if self.isEnabled():
				if self.isPressed():
					self.textColor=QColor(96,96,96,255)
				else:
					self.textColor=QColor(0,0,0,255)
			else:
				self.textColor=QColor(160,160,160,255)
		self.arrowPadding=self.arrow.width()+self.iconSpacing if self.subMenu else 0
		self.indicatorPadding=self.indicator.width()+self.iconSpacing if self.checkable else 0
		self.leftPadding= self.arrowPadding if self.mirrored else self.indicatorPadding
		self.rightPadding= self.indicatorPadding if self.mirrored else self.arrowPadding
		self.addStyleSheet('border-radius',LingmoTheme.instance._roundWindowRadius)
		self.addStyleSheet('background-color',(LingmoTheme.instance.itemHoverColor if self.isHovered() else LingmoTheme.instance.itemNormalColor))
		if self.iconSource: 
			self.icon.setGeometry(self.padding+self.leftPadding,self.padding,self.iconWidth,self.iconHeight)
		else:
			self.icon.setGeometry(self.padding+self.leftPadding,self.padding,0,0)
		self.text.move(self.icon.x()+self.icon.width()+(self.padding if self.iconSource else 0),self.height()/2-self.text.height()/2)
		self.resize(self.width(),36 if self.isVisible()else 0)
		self.indicator.setVisible(self.checked)
		self.arrow.setVisible(bool(self.subMenu))
		self.indicator.move(self.width()-self.rightPadding if self.mirrored else 6,self.height()/2-self.indicator.height()/2)
		self.arrow.move(6 if self.mirrored else self.width()-self.rightPadding,self.height()/2-self.arrow.height()/2)
		self.text.setFont(LingmoTextStyle.body)
		if self.iconSource:
			self.icon.setIconColor(self.palette().windowText())
	def setChecked(self):
		self.checked=not self.checked if self.checkable else False
	def onPressed(self):
		if self.subMenu and isinstance(self.subMenu,LingmoMenu):
			self.subMenu.setPosition(self.parentWidget().mapToGlobal(QPoint(self.x()+self.width()+2,self.y())))
			self.subMenu.showMenu()
		elif self.autoClose and isinstance(self.parentWidget().parentWidget(),LingmoMenu):
			self.parentWidget().parentWidget().hideMenu()
	def getWidth(self):
		return self.icon.width()+self.text.width()+3*self.padding+self.leftPadding+self.rightPadding
class LingmoMenu(LingmoFrame):
	showed=Signal()
	hided=Signal()
	def __init__(self,position=None,animationEnabled=True,autoResize=True):
		super().__init__(show=False)
		self.animationEnabled=animationEnabled
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint|Qt.WindowType.Tool)
		self.scrolled=False
		self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
		self.opacity=0
		self.background=LingmoFrame(self)
		self.background.move(5,5)
		self.background.addStyleSheet('background-color',QColor(45,45,45,255)if LingmoTheme.instance.dark()else QColor(252,252,252,255))
		self.background.addStyleSheet('border-style','solid')
		self.background.addStyleSheet('border-width',1)
		self.background.addStyleSheet('border-color',QColor(26,26,26,255)if LingmoTheme.instance.dark() else QColor(191,191,191,255))
		self.background.addStyleSheet('border-radius',LingmoTheme.instance._roundWindowRadius+1)
		self.shadow=LingmoShadow(self.background,radius=LingmoTheme.instance._roundWindowRadius)
		self.position=position
		self.items: list[LingmoMenuItem] = []
		self.showAnimation=LingmoAnimation(self,'opacity')
		self.showAnimation.setStartValue(0)
		self.showAnimation.setEndValue(1)
		self.hideAnimation=LingmoAnimation(self,'opacity')
		self.hideAnimation.setStartValue(1)
		self.hideAnimation.setEndValue(0)
		self.scrollbar=LingmoScrollBar(self,target=self.background,orientation=Qt.Orientation.Vertical)
		self.scrollbar.setOffsetDecrease(5)
		self.scrollbar.setOffsetIncrease(5)
		self.scrollbar.setOffsetPerpendicalar(5)
		self.autoResize=autoResize
	def updateEvent(self):
		self.addStyleSheet('background-color','transparent')
		self.setWindowOpacity(self.opacity)
		self.resize(self.background.width()+10,300 if self.scrolled else self.background.height()+10)
		self.scrollbar.setVisible(self.scrolled)
		maxWidth=0
		for i in range(len(self.items)):
			maxWidth=max(maxWidth,self.items[i].getWidth())
			if i==0:
				self.items[i].move(4,4)
			else:
				self.items[i].move(4,self.items[i-1].y()+self.items[i-1].height()+(4 if self.items[i-1].isVisible()else 0))
		if self.autoResize:
			
			for i in range(len(self.items)):
				self.items[i].resize(maxWidth,self.items[i].height())
			self.background.resize(maxWidth+8,(self.items[-1].y()+self.items[-1].height()+4)if len(self.items)else 36)
		else:
			for i in range(len(self.items)):
				self.items[i].resize(self.background.width()-8,self.items[i].height())
			self.background.resize(self.background.width(),(self.items[-1].y()+self.items[-1].height()+4)if len(self.items)else 36)
		self.scrolled=len(self.items)>10
	def showMenu(self):
		pos=QCursor.pos() if self.position==None else self.position
		self.move(pos)
		self.setVisible(True)
		self.showAnimation.setDuration(83 if LingmoTheme.instance._animationEnabled and self.animationEnabled else 0)
		self.showAnimation.start()
		self.showed.emit()
	def hideMenu(self):
		self.hideAnimation.setDuration(83 if LingmoTheme.instance._animationEnabled and self.animationEnabled else 0)
		self.hideAnimation.start()
		self.setVisible(False)
		for i in self.items:
			if i.subMenu:
				i.subMenu.hideMenu()
		self.hided.emit()
	def addItem(self,item: LingmoMenuItem):
		self.items.append(item)
		item.setParent(self.background)
	def setPosition(self,val):
		self.position=val
	def focusOutEvent(self, event):
		self.hideMenu()
	def count(self):
		return len(self.items)
class LingmoObject(QObject):
	def __init__(self,parent=None,show=True):
		super().__init__(parent,show)
class LingmoProgressButton(LingmoButton):
	def __init__(self,parent=None,show=True,content='',progress=0):
		super().__init__(parent,show)
		self.progress=progress
		self.ctrlBg.deleteLater()
		self.ctrlBg=LingmoControlBackground(self)
		self.ctrlBg.setRadius(LingmoTheme.instance._roundWindowRadius)
		self.clip=LingmoClip(self.ctrlBg,radius=LingmoTheme.instance._roundWindowRadius)
		self.rectBack=LingmoFrame(self.clip)
		self.setContent(content)
		self.setClickShadowChange(False)
		self.focusRect=LingmoFocusRectangle(self.ctrlBg)
		self.focusRect.setRadius(4)
		self.rectBackWidth=self.clip.width()*self.progress
		self.rectBackHeight=3
		self.widthAnimation=LingmoAnimation(self,'rectBackWidth')
		self.widthAnimation.setDuration(167)
		self.heightAnimation=QSequentialAnimationGroup()
		self.heightAnimation1=QPauseAnimation(167 if LingmoTheme.instance._animationEnabled else 0)
		self.heightAnimation2=LingmoAnimation(self,'rectBackHeight')
		self.heightAnimation2.setDuration(167)
	def updateEvent(self):
		if self.checked():
			self.textNormalColor=QColor(0,0,0,255)if LingmoTheme.instance.dark() else QColor(255,255,255,255)
			self.textPressedColor=self.textNormalColor
			self.textDisabledColor=QColor(173,173,173,255)if LingmoTheme.instance.dark()else QColor(255,255,255,255)
		else:
			self.textNormalColor=QColor(255,255,255,255)if LingmoTheme.instance.dark() else QColor(0,0,0,255)
			self.textPressedColor=QColor(162,162,162,255) if LingmoTheme.instance.dark() else QColor(96,96,96,255)
			self.textDisabledColor=QColor(131,131,131,255)if LingmoTheme.instance.dark()else QColor(160,160,160,255)
		super().updateEvent()
		self.normalColor=LingmoTheme.instance.primaryColor if self.checked() else (QColor(62,62,62,255)if LingmoTheme.instance.dark() else QColor(254,254,254,255))
		self.hoverColor=(self.normalColor.darker(110)if LingmoTheme.instance.dark()else self.normalColor.lighter(110))if self.checked() else (QColor(68,68,68,255)if LingmoTheme.instance.dark()else QColor(246,246,246,255))
		self.disableColor=(QColor(82,82,82,255)if LingmoTheme.instance.dark() else QColor(199,199,199,255))if self.checked() else (QColor(59,59,59,255)if LingmoTheme.instance.dark()else QColor(244,244,244,255))
		self.pressedColor=self.normalColor.darker(120)if LingmoTheme.instance.dark()else self.normalColor.lighter(120)
		self.clip.resize(self.ctrlBg.size())
		if not self.isEnabled():
			self.bgColor=self.disableColor
		elif self.isPressed() and self.checked():
			self.bgColor=self.pressedColor
		elif self.isHovered():
			self.bgColor=self.hoverColor
		else:
			self.bgColor=self.normalColor
		self.ctrlBg.move(self.horizontalPadding,self.verticalPadding)
		self.ctrlBg.setBorderWidth(0 if self.checked()else 1)
		self.ctrlBg.setColor(self.bgColor)
		self.rectBack.resize(self.rectBackWidth,self.rectBackHeight)
		self.rectBack.setVisible(not self.checked())
		self.rectBack.addStyleSheet('background-color',LingmoTheme.instance.primaryColor)
	def checked(self):
		return self.rectBack.height()==self.ctrlBg.height() and self.progress==1
	def setRectBackWidth(self,val):
		if val!=self.rectBackWidth:
			self.widthAnimation.setStartValue(self.rectBackWidth)
			self.widthAnimation.setEndValue(val)
			self.widthAnimation.start()
	def setRectBackHeight(self,val):
		if val!=self.rectBackHeight:
			self.heightAnimation2.setStartValue(self.rectBackHeight)
			self.heightAnimation2.setEndValue(val)
			self.heightAnimation.start()
	def setProgress(self,val):
		self.progress=val
		self.setRectBackWidth(self.clip.width()*self.progress)
		self.setRectBackHeight(self.clip.height()if self.progress==1 else 3)
class LingmoProgressRing(LingmoFrame):
	def __init__(self,parent=None,show=True,duration=2000,strokeWidth=6,progressVisible=False,color=LingmoTheme.instance.primaryColor,
			indeterminate=True,clip=True,progress=0):
		super().__init__(parent,show)
		self.duration=duration
		self.strokeWidth=strokeWidth
		self.progressVisible=progressVisible
		self.color=color
		self.backgroundColor=QColor(99,99,99,255)if LingmoTheme.instance.dark() else QColor(214,214,214,255)
		self.indeterminate=indeterminate
		self.clip=clip
		self.resize(56,56)
		self.addStyleSheet('background-color','transparent')
		self.addStyleSheet('border-color',self.backgroundColor)
		self.addStyleSheet('border-width',self.strokeWidth)
		self.addStyleSheet('border-style','solid')
		self.visualPosition=progress
		self.startAngle=0
		self.sweepAngle=0
		self.startAngleAnimation=QSequentialAnimationGroup()
		self.sweepAngleAnimation=QSequentialAnimationGroup()
		self.startAngleAnimation1=LingmoAnimation(self,'startAngle')
		self.startAngleAnimation1.setStartValue(0)
		self.startAngleAnimation1.setEndValue(450)
		self.startAngleAnimation2=LingmoAnimation(self,'startAngle')
		self.startAngleAnimation2.setStartValue(450)
		self.startAngleAnimation2.setEndValue(1080)
		self.sweepAngleAnimation1=LingmoAnimation(self,'sweepAngle')
		self.sweepAngleAnimation1.setStartValue(0)
		self.sweepAngleAnimation1.setEndValue(180)
		self.sweepAngleAnimation2=LingmoAnimation(self,'sweepAngle')
		self.sweepAngleAnimation2.setStartValue(180)
		self.sweepAngleAnimation2.setEndValue(0)
		self.startAngleAnimation.addAnimation(self.startAngleAnimation1)
		self.startAngleAnimation.addAnimation(self.startAngleAnimation2)
		self.sweepAngleAnimation.addAnimation(self.sweepAngleAnimation1)
		self.sweepAngleAnimation.addAnimation(self.sweepAngleAnimation2)
		self.startAngleAnimation.setLoopCount(-1)
		self.sweepAngleAnimation.setLoopCount(-1)
		self.startAngleAnimation1.setDuration(self.duration/2)
		self.startAngleAnimation2.setDuration(self.duration/2)
		self.sweepAngleAnimation1.setDuration(self.duration/2)
		self.sweepAngleAnimation2.setDuration(self.duration/2)
		if indeterminate:
			self.startAngleAnimation.start()
			self.sweepAngleAnimation.start()
		self.text=LingmoText(self)
	def updateEvent(self):
		self.addStyleSheet('border-radius',self.width()/2)
		self._radius=self.width()/2-self.strokeWidth
		self._progress=0 if self.indeterminate else self.visualPosition
		self.text.setVisible((not self.indeterminate)and self.progressVisible)
		self.text.setText(str(int(self.visualPosition*100))+'%')
		self.text.move(self.width()/2-self.text.width()/2,self.height()/2-self.text.height()/2)
	def paintEvent(self,event):
		painter=QPainter(self)
		pen=QPen()
		pen.setColor(self.color)
		pen.setWidth(self.strokeWidth/6*7)
		pen.setCapStyle(Qt.PenCapStyle.RoundCap)
		painter.setPen(pen)
		if self.indeterminate:
			painter.drawArc(self.strokeWidth/2,self.strokeWidth/2,self.width()-self.strokeWidth,self.height()-self.strokeWidth,
				self.startAngle*16,self.sweepAngle*16)
		else:
			painter.drawArc(self.strokeWidth/2,self.strokeWidth/2,self.width()-self.strokeWidth,self.height()-self.strokeWidth,
				-0.5*math.pi,self._progress*360*16)
	def setIndeterminate(self,val):
		self.indeterminate=val
		if val:
			self.startAngleAnimation.start()
			self.sweepAngleAnimation.start()
		else:
			self.startAngleAnimation.stop()
			self.sweepAngleAnimation.stop()
	def setProgress(self,val):
		self.visualPosition=val
class LingmoRouter(LingmoFrame):
	def __init__(self,parent=None,show=True):
		super().__init__(parent,show)
	def updateEvent(self):
		pass
class LingmoScrollBar(LingmoFrame):
	def __init__(self,parent=None,target:QWidget =None,show=True,orientation=Qt.Orientation.Horizontal,color=QColor(159,159,159,255)if LingmoTheme.instance.dark() else QColor(138,138,138,255)):
		super().__init__(parent,show)
		self.orientation=orientation
		self.target=target
		self.color=color
		self.pressedColor=QColor.darker(self.color)if LingmoTheme.instance.dark() else QColor.lighter(self.color)
		self.minLine=2
		self.maxLine=6
		self.position=0
		self.stepLength=10
		self.horizontalPadding=15 if self.horizontal()else 3
		self.verticalPadding=15 if self.vertical else 3
		self.horiDecrButton=LingmoIconButton(LingmoIconDef.CaretLeftSolid8,parent=self)
		self.horiIncrButton=LingmoIconButton(LingmoIconDef.CaretRightSolid8,parent=self)
		self.vertDecrButton=LingmoIconButton(LingmoIconDef.CaretUpSolid8,parent=self)
		self.vertIncrButton=LingmoIconButton(LingmoIconDef.CaretDownSolid8,parent=self)
		self.bar=LingmoFrame(self)
		self.barWidth=self.minLine
		self.horiDecrButton.setPaddings(2,2)
		self.horiIncrButton.setPaddings(2,2)
		self.vertDecrButton.setPaddings(2,2)
		self.vertIncrButton.setPaddings(2,2)
		self.horiDecrButton.pressed.connect(self.decrease)
		self.horiIncrButton.pressed.connect(self.increase)
		self.vertDecrButton.pressed.connect(self.decrease)
		self.vertIncrButton.pressed.connect(self.increase)
		self.animation=QSequentialAnimationGroup()
		self.animation1=QPauseAnimation()
		self.animation2=LingmoAnimation(self,'barWidth')
		self.animation2.setDuration(167)
		self.animation2.setEasingCurve(QEasingCurve.Type.OutCubic)
		self.animation.addAnimation(self.animation1)
		self.animation.addAnimation(self.animation2)
		self.hovered.connect(lambda:self.setBarWidth(self.maxLine))
		self.left.connect(lambda:self.setBarWidth(self.minLine))
		self.scrolling=False
		self.scrollPos=QPoint()
		self.barFirstPos=QPoint()
		self.bar.pressed.connect(lambda:self.setScrolling(True))
		self.bar.released.connect(lambda:self.setScrolling(False))
		self.offsetDecrease=0
		self.offsetIncrease=0
		self.offsetPerpendicular=0
	def updateEvent(self):
		self.horizontalPadding=15 if self.horizontal()else 3
		self.verticalPadding=15 if self.vertical() else 3
		self.raise_()
		self.horiDecrButton.setVisible(self.horizontal())
		self.horiIncrButton.setVisible(self.horizontal())
		self.vertDecrButton.setVisible(self.vertical())
		self.vertIncrButton.setVisible(self.vertical())
		self.horiDecrButton.setIconBorderSize(12,12)
		self.horiIncrButton.setIconBorderSize(12,12)
		self.vertDecrButton.setIconBorderSize(12,12)
		self.vertIncrButton.setIconBorderSize(12,12)
		self.horiDecrButton.setIconSize(8)
		self.horiIncrButton.setIconSize(8)
		self.vertDecrButton.setIconSize(8)
		self.vertIncrButton.setIconSize(8)
		self.horiDecrButton.setIconColor(self.color)
		self.horiIncrButton.setIconColor(self.color)
		self.vertDecrButton.setIconColor(self.color)
		self.vertIncrButton.setIconColor(self.color)
		self.horiDecrButton.move(2,self.height()/2-self.horiDecrButton.height()/2)
		self.horiIncrButton.move(self.width()-2-self.horiIncrButton.width(),self.height()/2-self.horiIncrButton.height()/2)
		self.vertDecrButton.move(self.width()/2-self.vertDecrButton.width()/2,2)
		self.vertIncrButton.move(self.width()/2-self.vertDecrButton.width()/2,self.height()-2-self.vertIncrButton.height())
		self.barSize=(self.target.parentWidget().width()/self.target.width() if self.horizontal() else self.target.parentWidget().height()/self.target.height())if self.target!=None else 1
		self.bar.resize(self.barSize*(self.width()-2*self.horizontalPadding)if self.horizontal()else self.barWidth,
				self.barSize*(self.height()-2*self.verticalPadding)if self.vertical()else self.barWidth)
		self.addStyleSheet('background-color',(QColor(44,44,44,255)if LingmoTheme.instance.dark()else QColor(255,255,255,255)))
		self.addStyleSheet('border-radius',5)
		if self.bar.isPressed():	
			self.bar.addStyleSheet('background-color',self.pressedColor)
		else:
			self.bar.addStyleSheet('background-color',self.color)
		self.bar.addStyleSheet('border-radius',self.barWidth/2)
		self.resize(self.parentWidget().width()-self.offsetDecrease-self.offsetIncrease if self.horizontal()else self.horizontalPadding*2+self.vertDecrButton.width(),
			self.parentWidget().height()-self.offsetDecrease-self.offsetIncrease if self.vertical() else self.verticalPadding*2+self.horiDecrButton.height())
		self.move(self.offsetDecrease if self.horizontal() else self.parentWidget().width()-self.width()-self.offsetPerpendicular,self.offsetDecrease if self.vertical() else self.parentWidget().height()-self.height()-self.offsetPerpendicular)
		self.bar.setVisible(self.barSize<1)
		self.visualPosition=self.position if self.barSize<1 else 0
		self.target.move(-self.visualPosition*(self.target.width()-self.target.parentWidget().width())if self.horizontal() else self.target.x(),
				-self.visualPosition*(self.target.height()-self.target.parentWidget().height())if self.vertical() else self.target.y())
		if self.scrolling:
			pos=QCursor.pos()
			if self.horizontal():
				self.bar.move(min(max(self.barFirstPos.x()-(self.scrollPos.x()-pos.x()),self.horizontalPadding),self.width()-self.bar.width()-self.horizontalPadding),self.barFirstPos.y())			
			else:
				self.bar.move(self.barFirstPos.x(),min(max(self.barFirstPos.y()-(self.scrollPos.y()-pos.y()),self.verticalPadding),self.height()-self.bar.height()-self.verticalPadding))
			self.position=(self.bar.x()-self.horizontalPadding)/(self.width()-self.bar.width()-2*self.horizontalPadding)if self.horizontal() else (self.bar.y()-self.verticalPadding)/(self.height()-self.bar.height()-2*self.verticalPadding)
		else:
			self.bar.move(self.horizontalPadding+self.position*(self.width()-2*self.horizontalPadding-self.bar.width()) if self.horizontal() else self.width()/2-self.bar.width()/2,
				self.verticalPadding+self.position*(self.height()-2*self.verticalPadding-self.bar.height()) if self.vertical() else self.height()/2-self.bar.height()/2)
	def horizontal(self):
		return self.orientation==Qt.Orientation.Horizontal
	def vertical(self):
		return self.orientation==Qt.Orientation.Vertical
	def increase(self):
		if self.target!=None:
			if self.horizontal():
				self.position+=10/(self.target.width()-self.target.parentWidget().width())
			else:
				self.position+=10/(self.target.height()-self.target.parentWidget().height())
			self.position=min(self.position,1)
	def decrease(self):
		if self.target!=None:
			if self.horizontal():
				self.position-=10/(self.target.width()-self.target.parentWidget().width())
			else:
				self.position-=10/(self.target.height()-self.target.parentWidget().height())
			self.position=max(self.position,0)
	def setBarWidth(self,val):
		if val==self.maxLine:
			self.animation1.setDuration(450)
		else:
			self.animation1.setDuration(150)
		self.animation2.setStartValue(self.barWidth)
		self.animation2.setEndValue(val)
		self.animation.start()
	def setScrolling(self,val):
		if val==True:
			self.scrollPos=QCursor.pos()
			self.barFirstPos=self.bar.pos()
		self.scrolling=val
	def setOrientation(self,val):
		self.orientation=val
	def setOffsetDecrease(self,val):
		self.offsetDecrease=val
	def setOffsetIncrease(self,val):
		self.offsetIncrease=val
	def setOffsetPerpendicalar(self,val):
		self.offsetPerpendicular=val
class LingmoShadow(LingmoFrame):
	def __init__(self,parent:QWidget=None,elevation=5,color=QColor(0,0,0,255),radius=4):
		self.parentObject=parent
		super().__init__(show=False)
		self.elevation=elevation
		self.color=color
		self.radius=radius
		self.widgets=[LingmoFrame(self.parentObject.parentWidget()) for i in range(self.elevation)]
	def updateEvent(self):
		geometry=self.parentObject.geometry()
		hPadding=self.parentObject.horizontalPadding if hasattr(self.parentObject,'horizontalPadding') else 0
		vPadding=self.parentObject.verticalPadding if hasattr(self.parentObject,'verticalPadding') else 0
		self.parentObject.raise_()
		for i in range(1,len(self.widgets)+1):
			self.widgets[i-1].setGeometry(geometry.left()-i+hPadding,geometry.top()-i+vPadding,geometry.width()+2*i-2*hPadding,geometry.height()+2*i-2*vPadding)
			self.widgets[i-1].addStyleSheet('background-color','#00000000')
			self.widgets[i-1].addStyleSheet('border-width',i)
			self.widgets[i-1].addStyleSheet('border-style','solid')
			self.widgets[i-1].addStyleSheet('border-radius',self.radius+i)
			self.widgets[i-1].addStyleSheet('border-color',QColor(self.color.red(),self.color.green(),self.color.blue(),255*0.01*(self.elevation-i+1)))
class LingmoSlider(LingmoFrame):
	def __init__(self,parent=None,show=True,tooltipEnabled=True,orientation=Qt.Orientation.Horizontal):
		super().__init__(parent,show)
		self.tooltipEnabled=True
		self.background=LingmoFrame(self)
		self.backgroundLength=180
		self.backgroundWidth=6
		self.addPage=LingmoFrame(self.background)
		self.handle=LingmoFrame(self)
		self.horizontalPadding=10
		self.verticalPadding=10
		self.visualPosition=0.7
		self.stepSize=1
		self.fromValue=0
		self.toValue=100
		self.orientation=orientation
		self.iconScale=1
		self.value=0
		self.shadow=LingmoShadow(self.handle,radius=10)
		self.icon=LingmoIcon(LingmoIconDef.FullCircleMask,self.handle,autoAdjust=True)
		self.iconScaleAnimation=LingmoAnimation(self,'iconScale')
		self.iconScaleAnimation.setDuration(167)
		self.iconScaleAnimation.setEasingCurve(QEasingCurve.Type.OutCubic)
		self.handle.pressed.connect(lambda:self.setIconScale(0.8))
		self.handle.released.connect(lambda:self.setIconScale(1.2 if self.isHovered()else 1.0))
		self.handle.hovered.connect(lambda:self.setIconScale(1.2))
		self.handle.left.connect(lambda:self.setIconScale(1.0))
		self.handle.pressed.connect(lambda:self.setSliding(True))
		self.handle.released.connect(lambda:self.setSliding(False))
		self.tooltip=LingmoToolTip(self.handle)
		self.sliding=False
		self.slidePos=QPoint()
		self.handleFirstPos=QPoint()
	def updateEvent(self):
		self.handle.resize(20,20)
		self.handle.addStyleSheet('border-radius',10)
		self.handle.addStyleSheet('background-color',(QColor(69,69,69,255)if LingmoTheme.instance.dark()else QColor(255,255,255,255)))
		self.icon.move(self.handle.width()/2-self.icon.width()/2,self.handle.height()/2-self.icon.height()/2)
		self.icon.setIconSize(self.iconScale*10)
		self.icon.setIconColor(LingmoTheme.instance.primaryColor)
		self.background.setFixedSize(self.backgroundLength if self.horizontal() else self.backgroundWidth,self.backgroundWidth if self.horizontal() else self.backgroundLength)
		self.background.addStyleSheet('border-radius',2)
		self.background.addStyleSheet('background-color',(QColor(162,162,162,255)if LingmoTheme.instance.dark() else QColor(138,138,138,255)))
		self.background.move(self.horizontalPadding,self.verticalPadding)
		self.addPage.move(0,0 if self.horizontal() else self.background.height()-self.visualPosition*self.background.height()+(1 if self.visualPosition!=1 else 0))
		self.addPage.resize(self.visualPosition*self.background.width() if self.horizontal() else 6,6 if self.horizontal() else self.visualPosition*self.background.height())
		self.addPage.addStyleSheet('border-radius',3)
		self.addPage.addStyleSheet('background-color',LingmoTheme.instance.primaryColor)
		self.resize(self.horizontalPadding*2+self.background.width(),self.verticalPadding*2+self.background.height())
		self.tooltip.setDisabled(not self.tooltipEnabled)
		self.value=(self.fromValue+self.visualPosition*(self.toValue-self.fromValue))*self.stepSize//self.stepSize
		self.value=int(self.value)if self.value%1==0 else self.value
		self.tooltip.setContent('  '+str(self.value)+'  ')
		if self.sliding:
			pos=QCursor.pos()
			if self.horizontal():
				self.handle.move(min(max(self.handleFirstPos.x()-(self.slidePos.x()-pos.x()),self.handle.width()/2),self.background.width()-self.handle.width()/2),self.handleFirstPos.y())
			else:
				self.handle.move(self.handleFirstPos.x(),min(max(self.handleFirstPos.y()-(self.slidePos.y()-pos.y()),self.handle.height()/2),self.background.height()-self.handle.height()/2))
			self.visualPosition=(self.handle.x()-self.handle.width()/2)/(self.background.width()-self.handle.width())if self.horizontal() else 1-(self.handle.y()-self.handle.height()/2)/(self.background.height()-self.handle.height())
		else:
			self.handle.move(self.horizontalPadding+(self.visualPosition if self.horizontal() else 0.5)*(self.background.width()-self.handle.width()),self.verticalPadding+(0.5 if self.horizontal() else (1-self.visualPosition))*(self.background.height()-self.handle.height()))
	def setIconScale(self,val):
		self.iconScaleAnimation.setStartValue(self.iconScale)
		self.iconScaleAnimation.setEndValue(val)
		self.iconScaleAnimation.start()
	def setSliding(self,val):
		if val==True:
			self.slidePos=QCursor.pos()
			self.handleFirstPos=self.handle.pos()
		self.sliding=val
	def horizontal(self):
		return self.orientation==Qt.Orientation.Horizontal
	def vertical(self):
		return self.orientation==Qt.Orientation.Vertical
	def setOrientation(self,val):
		self.orientation=val
class LingmoText(LingmoLabel):
	def __init__(self,parent=None,show=True,text='',color=LingmoTheme.instance.fontPrimaryColor,autoAdjust=True):
		super().__init__(parent,show,autoAdjust=autoAdjust)
		self.colorEnabled=True
		self.color=color
		self.renderType=Qt.TextFormat.PlainText if LingmoTheme.instance._nativeText else Qt.TextFormat.AutoText
		self.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
		self.setFont(LingmoTextStyle.body)
		self.setAlignment(Qt.AlignmentFlag.AlignCenter)
	def updateEvent(self):
		self.addStyleSheet('color',QColor(self.color if self.colorEnabled else (qRgba(131,131,131,255)if LingmoTheme.instance.dark()else qRgba(160,160,160,255))))
		self.setTextFormat(self.renderType)
	def setColorEnabled(self,val: bool):
		self.colorEnabled=val
	def setColor(self,val):
		self.color=val
class LingmoTextButton(LingmoFrame):
	def __init__(self,parent=None,show=True,content='',normalColor=LingmoTheme.instance.primaryColor,
			hoverColor: QColor = None,pressedColor: QColor = None,disableColor=QColor(82,82,82,255)if LingmoTheme.instance.dark() else QColor(199,199,199,255),
			backgroundHoverColor=LingmoTheme.instance.itemHoverColor,
			backgroundPressedColor=LingmoTheme.instance.itemPressColor,
			backgroundNormalColor=LingmoTheme.instance.itemNormalColor,
			backgroundDisableColor=LingmoTheme.instance.itemNormalColor,textBold=True):
		super().__init__(parent,show)
		self.content=content
		self.normalColor=normalColor
		self.hoverColor=(QColor.darker(self.normalColor,115)if LingmoTheme.instance.dark() else QColor.lighter(self.normalColor,115))if hoverColor==None else hoverColor
		self.pressedColor=(QColor.darker(self.normalColor,130)if LingmoTheme.instance.dark() else QColor.lighter(self.normalColor,130))if pressedColor==None else pressedColor
		self.disableColor=disableColor
		self.backgroundNormalColor=backgroundNormalColor
		self.backgroundHoverColor=backgroundHoverColor
		self.backgroundPressedColor=backgroundPressedColor
		self.backgroundDisableColor=backgroundDisableColor
		self.textBold=textBold
		self.horizontalPadding=12
		self.verticalPadding=0
		self.ctrlBg=LingmoFrame(self)
		self.ctrlBg.setGeometry(self.horizontalPadding,self.verticalPadding,self.width()-2*self.horizontalPadding,self.height()-2*self.verticalPadding)
		self.setFont(LingmoTextStyle.body)
		self.setFocusPolicy(Qt.FocusPolicy.TabFocus)
		self.focusRect=LingmoFocusRectangle(self.ctrlBg,radius=8)
		self.focusRect.resize(self.ctrlBg.size())
		self.contentText=LingmoText(self)
		self.contentText.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.contentText.setFont(self.font())
	def updateEvent(self):
		self.textColor=self.normalColor
		self.backgroundColor=self.backgroundNormalColor
		if not self.isEnabled():
			self.textColor=self.disableColor
			self.backgroundColor=self.backgroundDisableColor
		elif self.isPressed():
			self.textColor=self.pressedColor
			self.backgroundColor=self.backgroundPressedColor
		elif self.isHovered():
			self.textColor=self.hoverColor
			self.backgroundColor=self.backgroundHoverColor
		self.ctrlBg.addStyleSheet('background-color',self.backgroundColor)
		self.ctrlBg.addStyleSheet('border-radius',LingmoTheme.instance._roundWindowRadius)
		self.contentText.addStyleSheet('color',self.textColor)
		self.focusRect.setVisible(self.hasFocus())
		self.contentText.setText(self.content)
		self.contentText.move(self.width()/2-self.contentText.width()/2,
						self.height()/2-self.contentText.height()/2)
	def setContent(self,val):
		self.content=val
	def setTextBold(self,val):
		self.textBold=val
class LingmoToolTip(LingmoFrame):
	def __init__(self,parent: QWidget,interval=0,content='',padding=6,margins=6):
		self.parentObject=parent
		super().__init__(show=False)
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint|Qt.WindowType.ToolTip)
		self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
		self.background=LingmoFrame(self)
		self.text=LingmoText(self.background)
		self.content=content
		self.text.setText(content)
		self.text.setWordWrap(True)
		self.padding=padding
		self.margins=margins
		self.background.setGeometry(self.padding,self.padding,self.text.width()+self.padding,self.text.height()+self.padding)
		self.text.setFont(LingmoTextStyle.body)
		self.listening=False
		self.timer1=QTimer()
		self.interval=interval
		self.shadow=LingmoShadow(self.background,radius=LingmoTheme.instance._roundWindowRadius)
		self.timer1.timeout.connect(lambda:self.isVisible())
	def updateEvent(self):
		self.addStyleSheet('background-color','transparent')
		self.resize(self.background.width()+self.margins*2,self.background.height()+self.margins*2)
		self.move(self.parentObject.mapToGlobal(QPoint(self.parentObject.width()/2-self.width()/2,-self.height()-3)))
		self.background.setGeometry(self.padding,self.padding,self.text.width()+self.padding,self.text.height()+self.padding)
		self.text.move(self.background.width()/2-self.text.width()/2,self.background.height()/2-self.text.height()/2)
		self.background.addStyleSheet('background-color',(QColor(50,49,48,255)if LingmoTheme.instance.dark()else QColor(255,255,255,255)))
		self.background.addStyleSheet('border-radius',LingmoTheme.instance._roundWindowRadius)
		if not(self.listening) and self.parentObject.underMouse() and self.isEnabled():
			self.listen()
		elif self.isVisible() and not(self.parentObject.underMouse()):
			self.listening=False
			self.hide()
		self.text.setText(self.content)
	def listen(self):
		self.listening=True
		self.timer1.timeout.connect(self.showText)
		self.timer1.start(self.interval)
	def showText(self):
		self.show()
		self.timer1.stop()
	def setContent(self,val):
		self.content=val
class LingmoWindow(LingmoFrame):
	def __init__(self,parent=None,show=True):
		super().__init__(parent,show)
	def updateEvent(self):
		pass