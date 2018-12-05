
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button


import common, typeprice, typetime


class TypeDropDown(DropDown):

    def __init__(self, root, **kwargs):
        super().__init__(**kwargs)
        self.root = root

    def on_select(self, data):
        self.attach_to.text = data
        self.root.ids.layout.remove_widget(self.root.type)
        if data == 'Price':
            self.root.type = typeprice.TypePrice(self.root.cond)
        else:
            self.root.type = typetime.TypeTime(self.root.cond)

        self.root.ids.layout.add_widget(self.root.type)

class CondScreen(Screen):

    def __init__(self, cond, **kwargs):
        super().__init__(**kwargs)
        self.cond = cond
        self.ids.btn_enable.text = "~" if self.cond['enable'] else '|'
        self.type = Label(text='None')
        self.ids.layout.add_widget(self.type)

    def toggle_enable(self, button):
        self.cond['enable'] = not self.cond['enable']
        button.text = "~" if self.cond['enable'] else '|'




class TestApp(App):

    def build(self):
        self.row_height = Window.height / 10
        self.row_space = 10
        self.cond = common.init_cond()

        return CondScreen(self.cond)

if __name__ == '__main__':
    
    kv = Builder.load_file("./cond.kv")
    TestApp().run()

#
