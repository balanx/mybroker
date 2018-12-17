
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition


class SettingScreen(Screen):
    text = ['']

    def __init__(self, wisb, **kwargs):
        self.wisb = wisb
        self.text[0] = str(self.wisb.fd[0][0])
        super().__init__(**kwargs)

    def on_text_interval(self, text):
        try:
            t = float(text)
        except:
            t = 3

        if t < 0.1:
            self.wisb.fd[0][0] = 0.1
        else:
            self.wisb.fd[0][0] = t


#
