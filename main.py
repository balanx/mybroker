from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.properties import ObjectProperty, NumericProperty, ListProperty
from kivy.clock import Clock
from functools import partial




class NoteScreen(Screen):
    view = ObjectProperty(None)



class ListScreen(Screen):
    view = ObjectProperty(None)
    data = ListProperty()
    rows = ListProperty()
    index = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.create_scrollview)

    def create_scrollview(self, dt):
        self.layout = GridLayout(cols=2, spacing=1, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter("height"))
        self.view.add_widget(self.layout)


    def add_note(self):
        self.data.append({'title': 'New', 'mints': [], 'content': ''})
        self.index = len(self.data) - 1
        self.rows.append(Label(text='text', size=(1, Window.height/10), size_hint=(1, None)))
        self.layout.add_widget(self.rows[-1])
        self.rows.append(Button(text=self.data[self.index]['title'], size=(1, Window.height/10), size_hint=(1, None) ))
        self.rows[-1].bind(on_release=partial(self.HoldButtonNum))
        self.layout.add_widget(self.rows[-1])

    def HoldButtonNum(self, instance):
        self.index = self.rows.index(instance)
        self.manager.current = 'note_screen'
        print('Button instance:',  instance)
        print('Button index in list:',  self.index)


    def del_note(self):
        self.layout.remove_widget(self.rows[self.index]);
        self.layout.remove_widget(self.rows[self.index - 1]);
        del self.rows[self.index];
        del self.rows[self.index - 1];
        del self.data[int(self.index / 2)];
        self.manager.current = 'list_screen';


    def edit_note(self, text):
        index = int(self.index / 2)
        self.data[index]['title'] = text
        self.rows[self.index].text = text



kv = Builder.load_file("./main.kv")


class MainApp(App):

    def build(self):
        return kv


if __name__ == '__main__':
    MainApp().run()

#
