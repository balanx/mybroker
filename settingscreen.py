#
# Copyright (C) 2018 tobalanx@qq.com
#

from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty


class SettingScreen(Screen):
    text = ListProperty()

    def __init__(self, listscr, **kwargs):
        self.listscr = listscr
        self.text = self.listscr.fd[0]
        super().__init__(**kwargs)

    def on_text_interval(self, text):
        try:
            t = float(text)
        except:
            t = 3.0

        if t < 1.0:
            self.listscr.fd[0][0] = 1.0
        else:
            self.listscr.fd[0][0] = t

#
