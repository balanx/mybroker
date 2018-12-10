import json
from os.path import join, exists
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
#from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
#from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
#from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, StringProperty
from kivy.clock import Clock
#from functools import partial


import common, notescreen


class ListRow(BoxLayout):
    #note = ListProperty()

    def __init__(self, index, wisb, **kwargs):
        self.wisb = wisb
        self.note = wisb.fd[index]
        #print(self.note)
        super().__init__(**kwargs)


class ListScreen(Screen):
    rows = []

    scr_name = 'note_screen'

    def __init__(self, fd, **kwargs):
        super().__init__(**kwargs)
        self.fd = fd
        self.refresh_list()

    def refresh_list(self):
        self.ids.layout.clear_widgets()
        self.rows.clear()
        for i in self.fd[1:]:
            #print('==dd', i)
            self.add_note(i)

    def add_note(self, note=None):
        if note is None:
            self.fd.append(common.init_note())
        self.rows.append(ListRow(len(self.rows) + 1, self))
        self.ids.layout.add_widget(self.rows[-1])

    def open_note(self, instance):
        self.index = self.rows.index(instance) + 1
        print('fd:',  self.fd)
        print('row index in fd:',  self.index)

        #if self.manager.has_screen(self.scr_name):
        #    self.manager.remove_widget(self.manager.get_screen(self.scr_name))

        self.notescr = notescreen.NoteScreen(self.index, self, name=self.scr_name)
        self.manager.add_widget(self.notescr)
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = self.scr_name




class MainApp(App):
    fn = './data.json'
    fd = [[False]]

    def build(self):
        self.row_height = Window.height / 10
        self.row_space = 10
        #self.fd = [ [False], common.init_cond(), , , ]

        self.listscr = ListScreen(self.fd, name='list_screen')
        root = ScreenManager()
        root.add_widget(self.listscr)

        return root

    def load_list(self):
        if not exists(self.fn):
            return
        with open(self.fn) as fd:
            self.fd = json.load(fd)

    def save_list(self):
        with open(self.fn, 'w') as fd:
            json.dump(self.fd, fd)


if __name__ == '__main__':

    #kv = Builder.load_file("./main.kv")
    MainApp().run()

#
