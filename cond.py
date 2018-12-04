
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button


import common, typeprice


class TypeDropDown(DropDown):

    def on_select(self, data):
        self.attach_to.text = data


class CondScreen(Screen):

    def __init__(self, cond, **kwargs):
        super().__init__(**kwargs)
        self.cond = cond
        self.ids.btn_enable.text = "~" if self.cond['enable'] else '|'
        self.type = typeprice.TypePrice(cond)
        self.ids.layout.add_widget(self.type)

    def toggle_enable(self, button):
        self.cond['enable'] = not self.cond['enable']
        button.text = "~" if self.cond['enable'] else '|'




class TestApp(App):

    def build(self):
        self.menu_height = Window.height / 10
        self.cond = common.init_cond()

        return CondScreen(self.cond)

if __name__ == '__main__':
    
    kv = Builder.load_file("./cond.kv")
    TestApp().run()

#
