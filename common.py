
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

from kivy.uix.popup import Popup
from kivy.uix.button import Button

from kivy.properties import BooleanProperty

import datetime

oneday = datetime.timedelta(days=1)

def init_cond():
    return [False, 0, None, None, None]

def init_note():
    return [False, 'sh01', ['Strategy'], [init_cond()] ]


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