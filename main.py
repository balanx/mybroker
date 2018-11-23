from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.properties import ObjectProperty, NumericProperty, ListProperty
from kivy.clock import Clock
from functools import partial




class NoteScreen(Screen):
    pass



class ListScreen(Screen):
    view = ObjectProperty(None)
    data = ListProperty()
    buttons = ListProperty()
    index = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.create_scrollview)

    def create_scrollview(self, dt):
        self.layout = GridLayout(cols=1, spacing=1, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter("height"))

        scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scrollview.add_widget(self.layout)
        self.view.add_widget(scrollview)


    def add_note(self):
        self.data.append({'title': 'New ', 'mints': [], 'content': ''})
        self.index = len(self.data) - 1
        self.buttons.append(Button(text=self.data[self.index]['title'] + str(self.index),
                                    size=(50, 50), size_hint=(1, None),
                                    background_color=(0.5, 0.5, 0.5, 1), color=(1, 1, 1, 1)))
        self.buttons[self.index].bind(on_release=partial(self.HoldButtonNum))
        self.layout.add_widget(self.buttons[self.index])

    def HoldButtonNum(self, instance):
        self.index = self.buttons.index(instance)
        self.manager.current = 'note_screen'
        print('Button instance:',  instance)
        print('Button index in list:',  self.index)


    def del_note(self):
        self.layout.remove_widget(self.buttons[self.index]);
        del self.buttons[self.index];
        del self.data[self.index];
        self.manager.current = 'list_screen';


kv = Builder.load_file("./main.kv")


class MainApp(App):

    def build(self):
        return kv


if __name__ == '__main__':
    MainApp().run()

#
