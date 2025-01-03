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

        button = LingmoPyUI.LingmoButton(self.window)
        button.setContent("114514")
        button.move(0, a)
        a += 40

        slider1 = LingmoPyUI.LingmoSlider(self.window)
        slider1.move(0, a)
        a += 40

        slider2 = LingmoPyUI.LingmoSlider(self.window)
        slider2.move(0, a)
        a += 40

        icon_button = LingmoPyUI.LingmoIconButton(
            LingmoPyUI.LingmoIconDef.Accept, self.window, content="1111"
        )
        icon_button.setDisplay(LingmoPyUI.LingmoIconButton.TextBesideIcon)
        icon_button.move(0,a)
        a += 40

        scrollbar = LingmoPyUI.LingmoScrollBar(self.frame, target=self.window)
        scrollbar.orientation = LingmoPyUI.Qt.Orientation.Horizontal

        tooltip = LingmoPyUI.LingmoToolTip(button, content="1919810")

    def run(self):
        LingmoPyUI.LingmoApp.run()


if __name__ == "__main__":
    app = ExampleApp()
    app.run()
