from LingmoPyUI import *
frame=LingmoFrame()
window=LingmoFrame(frame)
a=0
button=LingmoButton(window)
button.setContent('111')
button.move(0,a)
a+=40
button1=LingmoSlider(window)
# button1.setContent('111')
button1.move(0,a)
a+=40
button2=LingmoSlider(window)
button2.move(0,a)
a+=40
button2=LingmoIconButton(LingmoIconDef.Accept,window,content='1111')
button2.setDisplay(LingmoIconButton.TextBesideIcon)
button2.move(0,a)
a+=40
window.resize(1000,1000)
window.addStyleSheet('background-color','green')
frame.resize(500,500)
scrollbar=LingmoScrollBar(frame,target=window)
scrollbar.orientation=Qt.Orientation.Horizontal
tooltip=LingmoToolTip(button,content='发送到路口收到了科技焚枯食淡看来是道具发送到路口收到了科技焚枯食淡看来是道具发送到路口收到了科技焚枯食淡看来是道具')
LingmoApp.run()
