import LingmoPyUI
class ExampleApp():
    def __init__(self):
        self.window = LingmoPyUI.LingmoWindow(showDark=True,showStayTop=True,width=500,height=500,title='Example')
        self.frame = LingmoPyUI.LingmoFrame(self.window.contentItem)
        self.setup_ui()
    def setup_ui(self):

        self.frame.resize(500,1000)

        a = 0

        self.button = LingmoPyUI.LingmoButton(self.frame)
        self.button.setContent("LingmoButton")
        self.button.move(0, a)
        a += 40

        self.slider1 = LingmoPyUI.LingmoSlider(self.frame)
        self.slider1.move(0, a)
        a += 40

        self.slider2 = LingmoPyUI.LingmoSlider(self.frame)
        self.slider2.setOrientation(LingmoPyUI.Qt.Orientation.Vertical)
        self.slider2.move(0, a)
        a += 200

        self.iconButton = LingmoPyUI.LingmoIconButton(LingmoPyUI.LingmoIconDef.Accept, self.frame, content="IconButton")
        self.iconButton.setIconBorderSize(40,30)
        self.iconButton.move(0,a)
        a += 40

        self.scrollbar = LingmoPyUI.LingmoScrollBar(self.window.contentItem, target=self.frame,autoOffsetIncrease=True)
        self.scrollbar.setOrientation(LingmoPyUI.Qt.Orientation.Vertical)

        self.tooltip = LingmoPyUI.LingmoToolTip(self.button, content="ToolTip")

        self.progressButton = LingmoPyUI.LingmoProgressButton(self.frame,content='Progress',progress=0.5)
        self.progressButton.move(0,a)
        self.progressButton.pressed.connect(self.progress)
        a+=40

        self.filledButton = LingmoPyUI.LingmoFilledButton(self.frame,content='Filled')
        self.filledButton.move(0,a)
        a+=40

        self.progressRing1 = LingmoPyUI.LingmoProgressRing(self.frame)
        self.progressRing1.move(0,a)
        self.progressRing2 = LingmoPyUI.LingmoProgressRing(self.frame,progressVisible=True,progress=0.5)
        self.progressRing2.setIndeterminate(False)
        self.progressRing2.move(60,a)
        a+=64

        self.loadingButton = LingmoPyUI.LingmoLoadingButton(self.frame,loading=True)
        self.loadingButton.setContent('LoadingButton')
        self.loadingButton.move(0,a)
        self.button.pressed.connect(lambda:self.loadingButton.setLoading(False))
        a+=40

        self.menu=LingmoPyUI.LingmoMenu()
        self.frame.pressed.connect(self.menu.hideMenu)
        self.frame.rightPressed.connect(self.menu.showMenu)
        
        self.menuItem1=LingmoPyUI.LingmoMenuItem(content='Simple MenuItem')
        self.menu.addItem(self.menuItem1)
        self.menuItem2=LingmoPyUI.LingmoMenuItem(iconSource=LingmoPyUI.LingmoIconDef.Admin,content='Icon MenuItem')
        self.menu.addItem(self.menuItem2)
        self.subMenu=LingmoPyUI.LingmoMenu()
        self.menuItem3=LingmoPyUI.LingmoMenuItem(content='SubMenu MenuItem',subMenu=self.subMenu)
        self.menu.addItem(self.menuItem3)
        self.menuItem4=LingmoPyUI.LingmoMenuItem(content='Checkable MenuItem',checkable=True)
        self.menu.addItem(self.menuItem4)
        self.menuItem5=LingmoPyUI.LingmoMenuItem(content='Sub MenuItem')
        self.subMenu.addItem(self.menuItem5)

        a=0
        self.dropDownBox=LingmoPyUI.LingmoDropDownBox(self.frame,content='DropDownBox')
        self.dropDownBox.move(200,a)
        for i in range(1,21):
            item=LingmoPyUI.LingmoMenuItem(content='Item'+str(i))
            self.dropDownBox.addItem(item)
        a+=40

        self.progressButton.pressed.connect(lambda:self.window.showSuccess('This is all the widgets',1500,'OK'))
        self.filledButton.pressed.connect(lambda:self.window.showWarning('This is all the widgets',1500,'OK'))
        self.loadingButton.pressed.connect(self.window.showLoading)
        self.iconButton.pressed.connect(lambda:self.window.showInfo('This is all the widgets',1500,'OK'))

    def run(self):
        LingmoPyUI.LingmoApp.run()

    def progress(self):
        self.progressButton.setProgress(1)
    

if __name__ == "__main__":
    app = ExampleApp()
    app.run()
