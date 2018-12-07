from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

import common, condscreen


class NoteSubRow(BoxLayout):

    def __init__(self, wisb, t1, t2, **kwargs):
        super().__init__(**kwargs)
        self.wisb = wisb
        self.t1 = t1
        self.t2 = t2


class NoteRow(BoxLayout):
    t2 = 0

    def __init__(self, wisb, t1, **kwargs):
        super().__init__(**kwargs)
        self.wisb = wisb
        self.t1 = t1


class NoteScreen(Screen):
    rows = []

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
        self.note.append( [common.init_cond()] ) # [[]]
        self.rows.append(NoteRow(self, t1))
        self.ids.layout.add_widget(self.rows[-1])

    def add_subcond(self, instance):
        self.note[instance.t1].insert(-1, common.init_cond() ) # []
        self.refresh_cond()

    def open_cond(self, instance):
        cond = self.note[instance.t1][instance.t2]
        self.condscr = condscreen.CondScreen(cond, name='cond_screen')
        self.manager.add_widget(self.condscr)
        self.manager.current = 'cond_screen'



class TestApp(App):

    def build(self):
        self.row_height = Window.height / 10
        self.row_space = 10
        self.note = [ False,
                      'sh01',
                      ['Strategy'],
                      [common.init_cond()],
                      [common.init_cond(), [False, 2, 5, False, 1.0]]
                    ]

        notescr = NoteScreen(self.note, name='note_screen')
        root = ScreenManager()
        root.add_widget(notescr)
        return root


if __name__ == '__main__':

    kv = Builder.load_file("./notescreen.kv")
    TestApp().run()


#
