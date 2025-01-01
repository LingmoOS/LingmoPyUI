version='1.0.0'
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
timerDelay=10
widgetCount=0
class LingmoAnimation(QVariantAnimation):
	def __init__(self,obj: object,attr: str):
		super().__init__()
		self.obj=obj
		self.attr=attr
		self.precision=1000
	def setStartValue(self, value):
		return super().setStartValue(round(value*self.precision))
	def setEndValue(self, value):
		return super().setEndValue(round(value*self.precision))
	def updateCurrentValue(self, value):
		self.obj.__setattr__(self.attr,value/self.precision)
class LingmoFrame(QFrame):
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
		self.styleSheets[name]=str(style)
	def isHovered(self):
		return self.underMouse()
class LingmoAbstractButton(LingmoFrame):
	pressed=Signal()
	released=Signal()
	hovered=Signal()
	left=Signal()
	def __init__(self,parent=None,show=True):
		super().__init__(parent,show)
		self.ispressed=False
	def mousePressEvent(self, event):
		self.pressed.emit()
		self.ispressed=True
	def mouseReleaseEvent(self, event):
		self.released.emit()
		self.ispressed=False
	def enterEvent(self, event):
		self.hovered.emit()
	def leaveEvent(self, event):
		self.left.emit()
	def isPressed(self):
		return self.ispressed
class LingmoLabel(QLabel):
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
		self.setAlignment(Qt.AlignmentFlag.AlignCenter)
		widgetCount+=1
		self.setObjectName('LingmoWidget'+str(widgetCount))
	def __update__(self):
		self.update()
		styleSheetString='QLabel#'+self.objectName()+'{'
		for i in self.styleSheets:
			styleSheetString+=i+': '+self.styleSheets[i]+';'
		styleSheetString+='}'
		self.setStyleSheet(styleSheetString)
		self.adjustSize()
	def updateEvent():
		pass
	def addStyleSheet(self,name,style):
		self.styleSheets[name]=str(style)
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
		self.luminosityWidget.addStyleSheet('background-color',QColor(1,1,1,self.luminosity*255).name(QColor.NameFormat.HexArgb))
		self.tintWidget.addStyleSheet('background-color',self.tintColor.name(QColor.NameFormat.HexArgb))
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
class LingmoButton(LingmoAbstractButton):
	def __init__(self,parent=None,show=True,content='',
	normalColor=QColor(62,62,62,255)if LingmoTheme.instance.dark() else QColor(254,254,254,255),
	hoverColor=QColor(68,68,68,255)if LingmoTheme.instance.dark() else QColor(246,246,246,255),
	disableColor=QColor(59,59,59,255)if LingmoTheme.instance.dark() else QColor(251,251,251,255),
	dividerColor=QColor(80,80,80,255)if LingmoTheme.instance.dark() else QColor(233,233,233,255),
	textNormalColor=QColor(255,255,255,255)if LingmoTheme.instance.dark() else QColor(0,0,0,255),
	textPressedColor=QColor(162,162,162,255)if LingmoTheme.instance.dark() else QColor(96,96,96,255),
	textDisabledColor=QColor(131,131,131,255)if LingmoTheme.instance.dark() else QColor(160,160,160,255)):
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
	def updateEvent(self):
		if self.isEnabled():
			if self.isPressed():
				self.contentText.setColor(self.textPressedColor)
			else:
				self.contentText.setColor(self.textNormalColor)
		else:
			self.contentText.setColor(self.textDisabledColor)
		self.ctrlBg.setColor((self.hoverColor if self.isHovered() else self.normalColor)if self.isEnabled() else self.disabledColor)
		self.ctrlBg.setShadow((not self.isPressed())and self.isEnabled())
		self.focusRect.setVisible(self.hasFocus())
		self.contentText.setText(self.content)
		self.contentText.move(self.width()/2-self.contentText.width()/2,
						self.height()/2-self.contentText.height()/2)
	def setContent(self,val):
		self.content=val
class LingmoClip(LingmoFrame):
	def __init__(self,parent=None,show=True):
		super().__init__(parent,show)
		self.color=QColor(0,0,0,0)
		self.effect=QGraphicsOpacityEffect(self)
		self.effect.setOpacity(0.5)
		self.setGraphicsEffect(self.effect)
	def updateEvent(self):
		pass
class LingmoControlBackground(LingmoFrame):
	def __init__(self,parent=None,show=True,radius: int = 4,shadow: bool = True,color = QColor(42,42,42,255) if LingmoTheme.instance.dark() else QColor(254,254,254,255),borderWidths=(1,1,1,1)):
		super().__init__(parent,show)
		self.radius=radius
		self.shadow=shadow
		self.color=color
		self.borderColor=QColor(48,48,48,255) if LingmoTheme.instance.dark() else QColor(188,188,188,255)
		self.startColor=QColor.lighter(self.borderColor,1.25)
		self.endColor=self.borderColor if self.shadow else self.startColor
		self.borderWidths=borderWidths
		self.rectBorder=LingmoFrame(self)
		self.rectBack=LingmoFrame(self)
	def updateEvent(self):
		self.rectBack.addStyleSheet('border-radius',self.radius)
		self.rectBack.addStyleSheet('background-color',self.color.name(QColor.NameFormat.HexArgb))
		self.rectBack.setGeometry(self.borderWidths[0],self.borderWidths[1],self.width()-self.borderWidths[0]-self.borderWidths[2],self.height()-self.borderWidths[1]-self.borderWidths[3])
		self.borderColor=QColor(48,48,48,255) if LingmoTheme.instance.dark() else QColor(188,188,188,255)
		self.startColor=QColor.lighter(self.borderColor,1.25)
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
class LingmoDropDownBox(LingmoFrame):
	def __init__(self,parent=None,show=True):
		super().__init__(parent,show)
	def updateEvent(self):
		pass
class LingmoFilledButton(LingmoFrame):
	def __init__(self,parent=None,show=True):
		super().__init__(parent,show)
	def updateEvent(self):
		pass
class LingmoFocusRectangle(LingmoFrame):
	def __init__(self,parent=None,show=True,color=QColor(0,0,0,0),borderWidth=2,radius=10,borderColor=QColor(255,255,255,255)if LingmoTheme.instance.dark() else QColor(0,0,0,255)):
		super().__init__(parent,show)
		self.color=color
		self.borderWidth=borderWidth
		self.radius=radius
		self.borderColor=borderColor
	def updateEvent(self):
		self.raise_()
		self.addStyleSheet('background-color',self.color.name(QColor.NameFormat.HexArgb))
		self.addStyleSheet('border-width',self.borderWidth)
		self.addStyleSheet('border-radius',self.radius)
		self.addStyleSheet('border-color',self.borderColor.name(QColor.NameFormat.HexArgb))
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
	def __init__(self,iconSource,parent=None,show=True,iconSize=20,iconColor: QColor=QColor(255,255,255,255)if LingmoTheme.instance.dark() else QColor(0,0,0,255)):
		super().__init__(parent,show)
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
		self.addStyleSheet('color',self.iconColor.name(QColor.NameFormat.HexArgb))
		self.setAlignment(Qt.AlignmentFlag.AlignCenter)
	def setIconSource(self,val):
		self.iconSource=val
	def setIconSize(self,val):
		self.iconSize=val
	def setIconColor(self,val):
		self.iconColor=val
class LingmoIconButton(LingmoAbstractButton):
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
	def updateEvent(self):
		self.tooltip.setDisabled(self.content==''or self.display!=self.IconOnly)
		self.tooltip.setContent(self.content)
		self.text.setText(self.content)
		self.color=QColor()
		self.iconColor=QColor()
		self.textColor=LingmoTheme.instance.fontPrimaryColor
		if self.isEnabled():
			if self.isPressed():
				self.color=self.pressedColor
			elif self.isHovered():
				self.color=self.hoverColor
			else:
				self.color=self.normalColor
			self.iconColor=QColor(255,255,255,255)if LingmoTheme.instance.dark() else QColor(0,0,0,255)
		else:
			self.color=self.disableColor
			self.iconColor=QColor(130,130,130,255)if LingmoTheme.instance.dark() else QColor(161,161,161,255)
		self.icon.setIconColor(self.iconColor)
		self.icon.setIconSize(self.iconSize)
		self.text.setText(self.content)
		self.text.setFont(LingmoTextStyle.caption)
		self.background.addStyleSheet('border-radius',self.radius)
		self.background.addStyleSheet('background-color',self.color.name(QColor.NameFormat.HexArgb))
		self.text.addStyleSheet('color',self.textColor.name(QColor.NameFormat.HexArgb))
		self.background.adjustSize()
		self.background.move(8,8)
		self.resize(self.background.width()+2*8,self.background.height()+2*8)
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
	def setIconSize(self,val):
		self.iconSize=val
	def setIconWidth(self,val):
		self.icon.resize(val,self.icon.height())
	def setIconHeight(self,val):
		self.icon.resize(self.icon.width(),val)
	def setIconSize(self,width,height):
		self.icon.resize(width,height)
class LingmoImageButton(LingmoAbstractButton):
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
class LingmoLoadingButton(LingmoAbstractButton):
	def __init__(self,parent=None,show=True):
		super().__init__(parent,show)
	def updateEvent(self):
		pass
class LingmoMenu(LingmoFrame):
	def __init__(self,parent=None,show=True):
		super().__init__(parent,show)
	def updateEvent(self):
		pass
class LingmoMenuItem(LingmoFrame):
	def __init__(self,parent=None,show=True):
		super().__init__(parent,show)
	def updateEvent(self):
		pass
class LingmoObject(QObject):
	def __init__(self,parent=None,show=True):
		super().__init__(parent,show)
class LingmoProgressButton(LingmoFrame):
	def __init__(self,parent=None,show=True):
		super().__init__(parent,show)
	def updateEvent(self):
		pass
class LingmoProgressRing(LingmoFrame):
	def __init__(self,parent=None,show=True):
		super().__init__(parent,show)
	def updateEvent(self):
		pass
class LingmoRouter(LingmoFrame):
	def __init__(self,parent=None,show=True):
		super().__init__(parent,show)
	def updateEvent(self):
		pass
class LingmoScrollBar(LingmoFrame):
	def __init__(self,parent=None,show=True,orientation=Qt.Orientation.Horizontal,color=QColor(159,159,159,255)if LingmoTheme.instance.dark() else QColor(138,138,138,255)):
		super().__init__(parent,show)
		self.orientation=orientation
		self.color=color
		self.pressedColor=QColor.darker(self.color)if LingmoTheme.instance.dark() else QColor.lighter(self.color)
		self.minLine=2
		self.maxLine=6
		self.position=0
		self.horiDecrButton=LingmoIconButton(LingmoIconDef.CaretLeftSolid8,parent=self)
		self.horiIncrButton=LingmoIconButton(LingmoIconDef.CaretLeftSolid8,parent=self)
		self.vertDecrButton=LingmoIconButton(LingmoIconDef.CaretLeftSolid8,parent=self)
		self.vertIncrButton=LingmoIconButton(LingmoIconDef.CaretLeftSolid8,parent=self)
	def updateEvent(self):
		self.raise_()
		self.horiDecrButton.setVisible(self.horizontal())
		self.horiIncrButton.setVisible(self.horizontal())
		self.vertDecrButton.setVisible(self.vertical())
		self.vertIncrButton.setVisible(self.vertical())
	def horizontal(self):
		return self.orientation==Qt.Orientation.Horizontal
	def vertical(self):
		return self.orientation==Qt.Orientation.Vertical
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
			self.widgets[i-1].addStyleSheet('border-color',QColor(self.color.red(),self.color.green(),self.color.blue(),255*0.01*(self.elevation-i+1)).name(QColor.NameFormat.HexArgb))
class LingmoSlider(LingmoFrame):
	def __init__(self,parent=None,show=True,tooltipEnabled=True,orientation=Qt.Orientation.Horizontal):
		super().__init__(parent,show)
		self.tooltipEnabled=True
		self.background=LingmoFrame(self)
		self.backgroundLength=180
		self.backgroundWidth=6
		self.addPage=LingmoFrame(self.background)
		self.handle=LingmoAbstractButton(self)
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
		self.icon=LingmoIcon(LingmoIconDef.FullCircleMask,self.handle)
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
		self.handle.addStyleSheet('background-color',(QColor(69,69,69,255)if LingmoTheme.instance.dark()else QColor(255,255,255,255)).name(QColor.NameFormat.HexArgb))
		self.icon.move(self.handle.width()/2-self.icon.width()/2,self.handle.height()/2-self.icon.height()/2)
		self.icon.setIconSize(self.iconScale*10)
		self.icon.setIconColor(LingmoTheme.instance.primaryColor)
		self.background.setFixedSize(self.backgroundLength if self.horizontal() else self.backgroundWidth,self.backgroundWidth if self.horizontal() else self.backgroundLength)
		self.background.addStyleSheet('border-radius',2)
		self.background.addStyleSheet('background-color',(QColor(162,162,162,255)if LingmoTheme.instance.dark() else QColor(138,138,138,255)).name(QColor.NameFormat.HexArgb))
		self.background.move(self.horizontalPadding,self.verticalPadding)
		self.addPage.move(0,0)
		self.addPage.resize(self.visualPosition*self.background.width() if self.horizontal() else 6,6 if self.horizontal() else self.visualPosition*self.background.height())
		self.addPage.addStyleSheet('border-radius',3)
		self.addPage.addStyleSheet('background-color',LingmoTheme.instance.primaryColor.name(QColor.NameFormat.HexArgb))
		self.resize(self.horizontalPadding*2+self.background.width(),self.verticalPadding*2+self.background.height())
		self.tooltip.setDisabled(not self.tooltipEnabled)
		self.value=(self.fromValue+self.visualPosition*(self.toValue-self.fromValue))*self.stepSize//self.stepSize
		self.value=int(self.value)if self.value%1==0 else self.value
		self.tooltip.text.setText('  '+str(self.value)+'  ')
		if self.sliding:
			pos=QCursor.pos()
			if self.horizontal():
				self.handle.move(min(max(self.handleFirstPos.x()-(self.slidePos.x()-pos.x()),self.handle.width()/2),self.background.width()-self.handle.width()/2),self.handleFirstPos.y())
			else:
				self.handle.move(self.handleFirstPos.x(),min(max(self.handleFirstPos.y()-(self.slidePos.y()-pos.y()),self.handle.height()/2),self.background.height()-self.handle.height()/2))
			self.visualPosition=(self.handle.x()-self.handle.width()/2)/(self.background.width()-self.handle.width())if self.horizontal() else (self.handle.y()-self.handle.height()/2)/(self.background.height()-self.handle.height())
		else:
			self.handle.move(self.horizontalPadding+(self.visualPosition if self.horizontal() else 0.5)*(self.background.width()-self.handle.width()),self.verticalPadding+(0.5 if self.horizontal() else self.visualPosition)*(self.background.height()-self.handle.height()))
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
class LingmoText(LingmoLabel):
	def __init__(self,parent=None,show=True,text='',color=LingmoTheme.instance.fontPrimaryColor):
		super().__init__(parent,show)
		self.colorEnabled=True
		self.color=color
		self.renderType=Qt.TextFormat.PlainText if LingmoTheme.instance._nativeText else Qt.TextFormat.AutoText
		self.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
		self.setFont(LingmoTextStyle.body)
		self.setAlignment(Qt.AlignmentFlag.AlignCenter)
	def updateEvent(self):
		self.adjustSize()
		self.addStyleSheet('color',QColor(self.color if self.colorEnabled else (qRgba(131,131,131,255)if LingmoTheme.instance.dark()else qRgba(160,160,160,255))).name(QColor.NameFormat.HexArgb))
		self.setTextFormat(self.renderType)
	def setColorEnabled(self,val: bool):
		self.colorEnabled=val
	def setColor(self,val):
		self.color=val
class LingmoTextButton(LingmoAbstractButton):
	def __init__(self,parent=None,show=True,content='',normalColor=LingmoTheme.instance.primaryColor,
			hoverColor: QColor = None,pressedColor: QColor = None,disableColor=QColor(82,82,82,255)if LingmoTheme.instance.dark() else QColor(199,199,199,255),
			backgroundHoverColor=LingmoTheme.instance.itemHoverColor,
			backgroundPressedColor=LingmoTheme.instance.itemPressColor,
			backgroundNormalColor=LingmoTheme.instance.itemNormalColor,
			backgroundDisableColor=LingmoTheme.instance.itemNormalColor,textBold=True):
		super().__init__(parent,show)
		self.content=content
		self.normalColor=normalColor
		self.hoverColor=(QColor.darker(self.normalColor,1.15)if LingmoTheme.instance.dark() else QColor.lighter(self.normalColor,1.15))if hoverColor==None else hoverColor
		self.pressedColor=(QColor.darker(self.normalColor,1.3)if LingmoTheme.instance.dark() else QColor.lighter(self.normalColor,1.3))if pressedColor==None else pressedColor
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
		self.ctrlBg.addStyleSheet('background-color',self.backgroundColor.name(QColor.NameFormat.HexArgb))
		self.ctrlBg.addStyleSheet('border-radius',LingmoTheme.instance._roundWindowRadius)
		self.contentText.addStyleSheet('color',self.textColor.name(QColor.NameFormat.HexArgb))
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
	def updateEvent(self):
		self.addStyleSheet('background-color','transparent')
		self.resize(self.background.width()+self.margins*2,self.background.height()+self.margins*2)
		self.move(self.parentObject.mapToGlobal(QPoint(self.parentObject.width()/2-self.width()/2,-self.height()-3)))
		self.background.setGeometry(self.padding,self.padding,self.text.width()+self.padding,self.text.height()+self.padding)
		self.text.move(self.background.width()/2-self.text.width()/2,self.background.height()/2-self.text.height()/2)
		self.background.addStyleSheet('background-color',(QColor(50,49,48,255)if LingmoTheme.instance.dark()else QColor(255,255,255,255)).name(QColor.NameFormat.HexArgb))
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