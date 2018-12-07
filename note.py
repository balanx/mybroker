from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
#from kivy.uix.button import Button
#from kivy.uix.label import Label
#from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
#from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
#from kivy.properties import ObjectProperty, NumericProperty, ListProperty, DictProperty

import common, cond


class NoteSubRow(BoxLayout):
    #cond = DictProperty()

    def __init__(self, notescr, t1, t2, **kwargs):
        super().__init__(**kwargs)
        self.notescr = notescr
        self.t1 = t1
        self.t2 = t2


class NoteRow(BoxLayout):
    #cond = DictProperty()

    def __init__(self, notescr, t1, **kwargs):
        super().__init__(**kwargs)
        self.notescr = notescr
        self.t1 = t1


class NoteScreen(Screen):
    #layout = ObjectProperty(None)
    #note = DictProperty()
    #rows = ListProperty()
    rows = []
    #index = NumericProperty()

    def __init__(self, note, **kwargs):
        super().__init__(**kwargs)
        self.note = note
        self.refresh_cond()

    def refresh_cond(self):
        self.ids.layout.clear_widgets()
        # [ False, 'sh01', ['Strategy'], [condition], [], ... ]
        t1 = 3
        for cond in self.note[t1:]:
            self.rows.append(NoteRow(self, t1))
            self.ids.layout.add_widget(self.rows[-1])
            if len(cond) > 1: # 1st has done as NoteRow(), other as NoteSubRow()
                t2 = 1
                for i in cond[1:]:
                    self.rows.append(NoteSubRow(self, t1, t2))
                    self.ids.layout.add_widget(self.rows[-1])
                    t2 += 1
            t1 += 1

    def add_cond(self, cond=None):
        t1 = len(self.note)
        self.note.append([[]])
        self.rows.append(NoteRow(self, t1))
        self.ids.layout.add_widget(self.rows[-1])

    def add_subcond(self, instance):
        self.note[instance.t1].insert(-1, [])
        self.refresh_cond()

    #def HoldButtonNum(self, instance):
    #    self.index = self.rows.index(instance)
    #    self.note['policy'][self.index]['enable'] = not self.note['policy'][self.index]['enable']



class TestApp(App):

    def build(self):
        self.row_height = Window.height / 10
        self.row_space = 10
        self.note = [ False,
                      'sh01',
                      ['Strategy'],
                      [[False, 0, None, None, None]],
                      [[False, 0, None, None, None], [False, 2, 5, False, 1.0]]
                    ]

        return NoteScreen(self.note)


if __name__ == '__main__':

    kv = Builder.load_file("./note.kv")
    TestApp().run()


#
