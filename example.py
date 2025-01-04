import LingmoPyUI


class ExampleApp:
    def __init__(self):
        self.frame = LingmoPyUI.LingmoFrame()
        self.window = LingmoPyUI.LingmoFrame(self.frame)
        self.setup_ui()

    def setup_ui(self):
        self.window.resize(1000, 1000)
        self.window.addStyleSheet("background-color", "green")

        self.frame.resize(500, 500)

        a = 0

        self.button = LingmoPyUI.LingmoButton(self.window)
        self.button.setContent("114514")
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
            LingmoPyUI.LingmoIconDef.Accept, self.window, content="1111"
        )
        self.iconButton.setDisplay(LingmoPyUI.LingmoIconButton.TextBesideIcon)
        self.iconButton.move(0,a)
        a += 40

        self.scrollbar = LingmoPyUI.LingmoScrollBar(self.frame, target=self.window)

        self.tooltip = LingmoPyUI.LingmoToolTip(self.button, content="1919810")

        self.progressButton = LingmoPyUI.LingmoProgressButton(self.window,content='123',progress=0.5)
        self.progressButton.move(0,a)
        self.progressButton.pressed.connect(self.progress)
        a+=40

    def run(self):
        LingmoPyUI.LingmoApp.run()
        
    def progress(self):
        self.progressButton.setProgress(1)

if __name__ == "__main__":
    app = ExampleApp()
    app.run()
