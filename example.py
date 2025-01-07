import LingmoPyUI

class ExampleApp:
    def __init__(self):
        self.frame = LingmoPyUI.LingmoFrame()
        self.window = LingmoPyUI.LingmoFrame(self.frame)
        self.setup_ui()

    def setup_ui(self):
        self.window.resize(500, 1000)
        self.window.setWindowTitle('Example')
        self.window.addStyleSheet("background-color", "green")

        self.frame.resize(500, 500)

        a = 0

        self.button = LingmoPyUI.LingmoButton(self.window)
        self.button.setContent("LingmoButton")
        self.button.move(0, a)
        a += 40

        self.slider1 = LingmoPyUI.LingmoSlider(self.window)
        self.slider1.move(0, a)
        a += 40

        self.slider2 = LingmoPyUI.LingmoSlider(self.window)
        self.slider2.setOrientation(LingmoPyUI.Qt.Orientation.Vertical)
        self.slider2.move(0, a)
        a += 200

        self.iconButton = LingmoPyUI.LingmoIconButton(
            LingmoPyUI.LingmoIconDef.Accept, self.window, content="IconButton"
        )
        self.iconButton.setDisplay(LingmoPyUI.LingmoIconButton.TextBesideIcon)
        self.iconButton.move(0,a)
        a += 40

        self.scrollbar = LingmoPyUI.LingmoScrollBar(self.frame, target=self.window)
        self.scrollbar.setOrientation(LingmoPyUI.Qt.Orientation.Vertical)

        self.tooltip = LingmoPyUI.LingmoToolTip(self.button, content="ToolTip")

        self.progressButton = LingmoPyUI.LingmoProgressButton(self.window,content='Progress',progress=0.5)
        self.progressButton.move(0,a)
        self.progressButton.pressed.connect(self.progress)
        a+=40

        self.filledButton = LingmoPyUI.LingmoFilledButton(self.window,content='Filled')
        self.filledButton.move(0,a)
        a+=40

        self.progressRing1 = LingmoPyUI.LingmoProgressRing(self.window)
        self.progressRing1.move(0,a)
        self.progressRing2 = LingmoPyUI.LingmoProgressRing(self.window,progressVisible=True,progress=0.5)
        self.progressRing2.setIndeterminate(False)
        self.progressRing2.move(60,a)
        a+=64

        self.loadingButton = LingmoPyUI.LingmoLoadingButton(self.window,loading=True)
        self.loadingButton.setContent('LoadingButton')
        self.loadingButton.move(0,a)
        self.button.pressed.connect(lambda:self.loadingButton.setLoading(False))
        a+=40

        self.menu=LingmoPyUI.LingmoMenu()
        self.window.pressed.connect(self.menu.hideMenu)
        self.window.rightPressed.connect(self.menu.showMenu)
        
        self.menuItem1=LingmoPyUI.LingmoMenuItem(content='MenuItem1_aaaaaaaaa')
        self.menu.addItem(self.menuItem1)
        self.menuItem2=LingmoPyUI.LingmoMenuItem(iconSource=LingmoPyUI.LingmoIconDef.Admin,content='MenuItem2')
        self.menu.addItem(self.menuItem2)
        self.subMenu=LingmoPyUI.LingmoMenu()
        self.menuItem3=LingmoPyUI.LingmoMenuItem(content='MenuItem3',subMenu=self.subMenu)
        self.menu.addItem(self.menuItem3)

    def run(self):
        LingmoPyUI.LingmoApp.run()

    def progress(self):
        self.progressButton.setProgress(1)

if __name__ == "__main__":
    app = ExampleApp()
    app.run()
