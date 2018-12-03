
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

#from kivy.properties import BooleanProperty, StringProperty, ListProperty, DictProperty

def init_cond():
    return {'expr': ['False'],
            'enable': False }


class TypeDropDown(DropDown):

    def on_select(self, data):
        self.attach_to.text = data


class TypePrice(BoxLayout):

    def __init__(self, cond, **kwargs):
        super().__init__(**kwargs)
        self.cond = cond

    def on_checkbox1_active(self, instance, text):
        if instance.active:
            print(text)

    def on_checkbox2_active(self, instance, text):
        if instance.active:
            print(text)


class CondScreen(Screen):
    #enable = BooleanProperty()
    #cond = DictProperty(None)

    def __init__(self, cond, **kwargs):
        super().__init__(**kwargs)
        self.cond = cond
        self.ids.btn_enable.text = "~" if self.cond['enable'] else '|'
        self.type = TypePrice(cond)
        self.ids.layout.add_widget(self.type)

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
