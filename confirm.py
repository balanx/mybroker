
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

from kivy.uix.popup import Popup
from kivy.uix.button import Button

from kivy.properties import BooleanProperty




class ConfirmPopup(Popup):
    result = BooleanProperty(False)




kv = Builder.load_file("./confirm.kv")


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
    TestApp().run()

#
