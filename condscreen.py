#
# Copyright (C) 2018 tobalanx@qq.com
#

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

import common, typeprice, typetime


class TypeDropDown(DropDown):

    def __init__(self, condscr, **kwargs):
        super().__init__(**kwargs)
        self.condscr = condscr

    def on_select(self, data):
        self.attach_to.text = data
        self.condscr.ids.layout.remove_widget(self.condscr.type)

        if data == 'Price':
            self.condscr.type = typeprice.TypePrice(self.condscr.cond)
        else:
            self.condscr.type = typetime.TypeTime(self.condscr.cond)

        self.condscr.ids.layout.add_widget(self.condscr.type)


class CondScreen(Screen):
    text = ListProperty()

    def __init__(self, row, **kwargs):
        self.row = row
        self.cond = row.condit[row.xi][row.yi]
        self.text = self.cond
        super().__init__(**kwargs)

        if self.cond[1] == 1:
            self.type = typetime.TypeTime(self.cond)
            self.ids.btn_type.text = 'Time'
        elif self.cond[1] == 2:
            self.type = typeprice.TypePrice(self.cond)
            self.ids.btn_type.text = 'Price'
        else:
            self.type = Label(text='None')

        self.ids.layout.add_widget(self.type)

    def toggle_enable(self, button):
        self.cond[0] = not self.cond[0]
        button.text = "~" if self.cond[0] else '|'



class TestApp(App):

    def build(self):
        self.row_height = Window.height / 10
        self.row_space = 10
        # Type definition
        # 1: Time
        # 2: Price
        self.cond = [ common.init_cond(),
                      [False, 1, common.today(), 0, common.today()],
                      [False, 2, 5, False, 1.0]
                    ]

        return CondScreen(self.cond[0])


if __name__ == '__main__':

    kv = Builder.load_file("./cond.kv")
    TestApp().run()

#
