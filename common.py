#
# Copyright (C) 2018 tobalanx@qq.com
#

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

from kivy.uix.popup import Popup
from kivy.uix.button import Button

from kivy.properties import BooleanProperty

import datetime as dt

oneday = dt.timedelta(days=1)
today = dt.date.today()

def str2date(t):
    t = t.split('-')
    t = dt.date(int(t[0]), int(t[1]), int(t[2]))
    return t

def init_cond():
    return [False, 0, None, None, None]

def init_note():
    return [False, 'sh01', ['False'], [init_cond()] ]


class ConfirmPopup(Popup):
    result = BooleanProperty(False)




class TestApp(App):

    def build(self):
        self.menu_height = Window.height / 10
        self.pop = ConfirmPopup(on_dismiss=self.show)
        print(self.pop)
        btn = Button(text='popup', on_release=self.pop.open)

        return btn

    def show(self, instance):
        print(self.pop.result)
        print(instance)



if __name__ == '__main__':

    kv = Builder.load_file("./common.kv")
    TestApp().run()

#
