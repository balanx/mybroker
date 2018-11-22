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




class NoteView(Screen):
    pass



class Notes(Screen):
    view = ObjectProperty(None)
    notes = ListProperty()
    buttons = ListProperty()
    current_index = NumericProperty()

    def __init__(self, **kwargs):
        super(Notes, self).__init__(**kwargs)
        Clock.schedule_once(self.create_scrollview)

    def create_scrollview(self, dt):
        self.layout = GridLayout(cols=1, spacing=1, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter("height"))

        scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scrollview.add_widget(self.layout)
        self.view.add_widget(scrollview)


    def add_note(self):
        self.notes.append({'title': 'New ', 'mints': [], 'content': ''})
        note_index = len(self.notes) - 1
        self.buttons.append(Button(text=self.notes[note_index]['title'] + str(note_index),
                                    size=(50, 50), size_hint=(1, None),
                                    background_color=(0.5, 0.5, 0.5, 1), color=(1, 1, 1, 1)))
        self.buttons[note_index].bind(on_release=partial(self.HoldButtonNum, note_index))
        self.layout.add_widget(self.buttons[note_index])

    def HoldButtonNum(self, x, instance):
        self.current_index = x
        self.manager.current = 'noteview'
        print('Button instance:',  instance)
        print('Button index in list:',  x)




kv = Builder.load_file("./main.kv")


class MainApp(App):

    def build(self):
        return kv


if __name__ == '__main__':
    MainApp().run()

#
