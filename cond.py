
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

#from kivy.properties import BooleanProperty, StringProperty, ListProperty, DictProperty

def init_cond():
    return {'expr': ['False'],
            'enable': False }


class TypeDropDown(DropDown):

    def __init__(self, button, **kwargs):
        super().__init__(**kwargs)
        self.button = button

    def on_select(self, data):
        self.button.text = data


class CondScreen(Screen):
    #enable = BooleanProperty()
    #cond = DictProperty(None)

    def __init__(self, cond, **kwargs):
        super().__init__(**kwargs)
        self.cond = cond
        self.ids.enable.text = "~" if self.cond['enable'] else '|'
        self.dropdown = TypeDropDown(self.ids.type_sel)
        #self.ids.type_sel.bind(on_release = self.dropdown.open)
        #self.dropdown.bind(on_select=lambda instance, x: setattr(self.ids.type_sel, 'text', x))

    def toggle_enable(self, button):
        self.cond['enable'] = not self.cond['enable']
        button.text = "~" if self.cond['enable'] else '|'



kv = Builder.load_file("./cond.kv")


class TestApp(App):

    def build(self):
        self.menu_height = Window.height / 10
        self.cond = init_cond()

        return CondScreen(self.cond)

if __name__ == '__main__':
    TestApp().run()

#
