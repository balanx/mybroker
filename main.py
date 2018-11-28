from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
#from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
#from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, DictProperty
from kivy.clock import Clock
#from functools import partial



def init_note():
    return {'title': 'New', 'policy': [], 'comment': ''}


class NoteScreen(Screen):
    view = ObjectProperty(None)
    note = DictProperty(init_note())



class ListRow(BoxLayout):
    note = DictProperty(init_note())




class ListScreen(Screen):
    layout = ObjectProperty(None)
    notev = ObjectProperty(Screen)
    data = ListProperty()
    rows = ListProperty()
    index = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_screen(self):
        self.notev = self.manager.get_screen('note_screen')


    def add_note(self):
        self.data.append(init_note())
        self.index = len(self.data) - 1
        self.rows.append(ListRow(size=(1, Window.height/10), size_hint=(1, None) ))
        #self.rows[-1].bind(on_release=partial(self.HoldButtonNum))
        self.layout.add_widget(self.rows[-1])

    def HoldButtonNum(self, instance):
        self.index = self.rows.index(instance)
        #self.notev.note = self.data[self.index]
        #self.notev.text1 = self.data[self.index]['title']
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'note_screen'

        print('Data:',  self.data)
        print('Button index in list:',  self.index)


    def del_note(self):
        self.layout.remove_widget(self.rows[self.index]);
        #self.layout.remove_widget(self.rows[self.index - 1]);
        del self.rows[self.index];
        #del self.rows[self.index - 1];
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'list_screen';
        if self.data[self.index] is self.data[-1]:
            self.index -= 1
            del self.data[-1];
        else:
            del self.data[self.index];


    def edit_note(self, text):
        self.data[self.index]['title'] = text
        self.rows[self.index].note = self.data[self.index]
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'list_screen';


#kv = Builder.load_file("./main.kv")


class MainApp(App):

    def build(self):
        self.listv = ListScreen(name='list_screen')
        self.notev = NoteScreen(name='note_screen')
        root = ScreenManager()
        root.add_widget(self.listv)
        root.add_widget(self.notev)

        self.listv.get_screen()

        return root


if __name__ == '__main__':
    MainApp().run()

#
