import LingmoPyUI
frame=LingmoPyUI.LingmoFrame()
window=LingmoPyUI.LingmoFrame(frame)
a=0
button=LingmoPyUI.LingmoButton(window)
button.setContent('111')
button.move(0,a)
a+=40
button1=LingmoPyUI.LingmoSlider(window)
# button1.setContent('111')
button1.move(0,a)
a+=40
button2=LingmoPyUI.LingmoSlider(window)
button2.move(0,a)
a+=40
button2=LingmoPyUI.LingmoIconButton(LingmoIconDef.Accept,window,content='1111')
button2.setDisplay(LingmoPyUI.LingmoIconButton.TextBesideIcon)
button2.move(0,a)
a+=40
window.resize(1000,1000)
window.addStyleSheet('background-color','green')
frame.resize(500,500)
scrollbar=LingmoPyUI.LingmoScrollBar(frame,target=window)
scrollbar.orientation=LingmoPyUI.Qt.Orientation.Horizontal
tooltip=LingmoPyUI.LingmoToolTip(button,content='发送到路口收到了科技焚枯食淡看来是道具发送到路口收到了科技焚枯食淡看来是道具发送到路口收到了科技焚枯食淡看来是道具')
if __name__ == "__main__":
    LingmoApp.run()
