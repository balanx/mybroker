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
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, DictProperty
from kivy.clock import Clock
#from functools import partial



def init_note():
    return {'code': 'New',
            'enable': False,
            'comment': '',
            'policy': []}



class NoteRow(BoxLayout):
    note = DictProperty(init_note())


class NoteScreen(Screen):
    layout = ObjectProperty(None)
    note = DictProperty(init_note())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)



class ListRow(BoxLayout):
    note = DictProperty(init_note())




class ListScreen(Screen):
    layout = ObjectProperty(None)
    notev = ObjectProperty(Screen)
    fdata = ListProperty()
    rows = ListProperty()
    index = NumericProperty()

    scr_name = 'note_screen'
    fn = './data.json'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_data()

    def load_data(self):
        self.fdata = [ [],
                       {'connect': False}
                     ]
        if not exists(self.fn):
            return
        with open(self.fn) as fd:
            self.fdata = json.load(fd)

        for i in range(len(self.fdata[0])):
            self.add_note(self.fdata[0][i])

    def save_data(self):
        with open(self.fn, 'w') as fd:
            json.dump(self.fdata, fd)

    def add_note(self, note=None):
        if note is None:
            note = init_note()
            self.fdata[0].append(init_note())
        self.rows.append(ListRow(size=(1, Window.height/10), size_hint=(1, None) ))
        self.rows[-1].note = note
        self.layout.add_widget(self.rows[-1])

    def HoldButtonNum(self, instance):
        self.index = self.rows.index(instance)

        if self.manager.has_screen(self.scr_name):
            self.manager.remove_widget(self.manager.get_screen(self.scr_name))
            #del self.notev

        self.notev = NoteScreen(name=self.scr_name)
        self.notev.note = self.fdata[0][self.index]
        self.manager.add_widget(self.notev)
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = self.scr_name

        print('Data:',  self.fdata)
        print('Button index in list:',  self.index)


    def del_note(self):
        self.layout.remove_widget(self.rows[self.index])
        del self.rows[self.index]
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'list_screen'
        del self.fdata[0][self.index]
        self.save_data()


    def edit_note(self, note):
        self.fdata[0][self.index] = note
        self.rows[self.index].note = self.fdata[0][self.index]
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'list_screen'
        self.save_data()


#kv = Builder.load_file("./main.kv")


class MainApp(App):

    def build(self):
        self.listv = ListScreen(name='list_screen')
        root = ScreenManager()
        root.add_widget(self.listv)

        return root


if __name__ == '__main__':
    MainApp().run()

#
