
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

    def __init__(self, wisb, **kwargs):
        super().__init__(**kwargs)
        self.wisb = wisb

    def on_select(self, data):
        self.attach_to.text = data
        self.wisb.ids.layout.remove_widget(self.wisb.type)

        if data == 'Price':
            self.wisb.type = typeprice.TypePrice(self.wisb.cond)
        else:
            self.wisb.type = typetime.TypeTime(self.wisb.cond)

        self.wisb.ids.layout.add_widget(self.wisb.type)


class CondScreen(Screen):
    text = ListProperty()

    def __init__(self, wisb, **kwargs):
        self.wisb = wisb
        self.cond = wisb.note[wisb.t1][wisb.t2]
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

    '''
    def close_cond(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'note_screen'
        self.manager.remove_widget(self)
    '''



class TestApp(App):

    def build(self):
        self.row_height = Window.height / 10
        self.row_space = 10
        # Type definition
        # 1: Time
        # 2: Price
        self.cond = [ common.init_cond(),
                      [False, 1, common.datetime.date.today(), 0, common.datetime.date.today()],
                      [False, 2, 5, False, 1.0]
                    ]

        return CondScreen(self.cond[0])


if __name__ == '__main__':

    kv = Builder.load_file("./cond.kv")
    TestApp().run()

#
