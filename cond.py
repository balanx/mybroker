
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
#from kivy.properties import BooleanProperty, NumericProperty, ListProperty, DictProperty

import common, typeprice, typetime


class TypeDropDown(DropDown):

    def __init__(self, root, **kwargs):
        super().__init__(**kwargs)
        self.root = root


    def on_select(self, data):
        self.attach_to.text = data
        self.root.ids.layout.remove_widget(self.root.type)
        if data == 'Price':
            self.root.type = typeprice.TypePrice(self.root.subcond)
        else:
            self.root.type = typetime.TypeTime(self.root.subcond)

        self.root.ids.layout.add_widget(self.root.type)


class CondScreen(Screen):
    def __init__(self, index, cond, **kwargs):
        super().__init__(**kwargs)
        #self.index = index
        self.cond = cond
        self.subcond = cond[index]
        self.ids.btn_enable.text = "~" if cond[0] else '|'

        if self.subcond[0] == 1:
            self.type = typetime.TypeTime(self.subcond)
            self.ids.btn_type.text = 'Time'
        elif self.subcond[0] == 2:
            self.type = typeprice.TypePrice(self.subcond)
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
        self.index = 2
        # Type definition
        # 1: Time
        # 2: Price
        self.cond = [ False,
                      [0, None, None, None],
                      [1, common.datetime.date.today(), 0, common.datetime.date.today()],
                      [2, 5, False, 1.0]
                    ]

        return CondScreen(self.index, self.cond)


if __name__ == '__main__':

    kv = Builder.load_file("./cond.kv")
    TestApp().run()

#
