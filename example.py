from LingmoPyUI import *
window=LingmoFrame()
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
button2=LingmoSlider(window)
button2.move(0,a)
button2.horizontal=False
a+=40
tooltip=LingmoToolTip(button,content='发送到路口收到了科技焚枯食淡看来是道具发送到路口收到了科技焚枯食淡看来是道具发送到路口收到了科技焚枯食淡看来是道具')
window.show()
LingmoApp.run()
