from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import ListProperty

import common, condscreen


class NoteSubRow(BoxLayout):
    cond = ListProperty()

    def __init__(self, wisb, t1, t2, **kwargs):
        self.wisb = wisb
        self.t1 = t1
        self.t2 = t2
        self.cond = wisb.note[t1][t2]
        super().__init__(**kwargs)


class NoteRow(BoxLayout):
    cond = ListProperty()
    t2 = 0

    def __init__(self, wisb, t1, **kwargs):
        self.wisb = wisb
        self.t1 = t1
        self.cond = wisb.note[t1][0]
        super().__init__(**kwargs)


class NoteScreen(Screen):
    text = ListProperty([''])
    rows = []

    def __init__(self, wisb, **kwargs):
        self.index = wisb.index
        self.wisb = wisb
        self.note = wisb.fd[self.index]
        super().__init__(**kwargs)
        self.refresh_cond()

    def refresh_cond(self):
        self.ids.layout.clear_widgets()
        self.rows.clear()
        # [ False, 'sh01', ['Log'], [condition], [], ... ]
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
        self.show_cond()

    def add_cond(self, cond=None):
        t1 = len(self.note)
        self.note.append( [common.init_cond()] ) # [[]]
        self.rows.append(NoteRow(self, t1))
        self.ids.layout.add_widget(self.rows[-1])

    def add_subcond(self, instance):
        length = len(self.note[instance.t1])
        self.note[instance.t1].insert(length, common.init_cond() ) # []
        self.refresh_cond()

    def open_cond(self, instance):
        self.t1 = instance.t1
        self.t2 = instance.t2
        self.t3 = self.rows.index(instance)
        cond = self.note[self.t1][self.t2]
        self.condscr = condscreen.CondScreen(self, name='cond_screen')
        self.manager.add_widget(self.condscr)
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'cond_screen'

    def close_cond(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'note_screen'
        self.manager.remove_widget(self.condscr)
        self.rows[self.t3].cond = self.note[self.t1][self.t2]
        self.show_cond()

    def del_cond(self, instance):
        self.close_cond(instance)
        del self.note[self.t1][self.t2]
        if len(self.note[self.t1]) == 0:
            del self.note[self.t1]
        self.refresh_cond()

    def on_text_code(self, text):
        self.note[1] = text

    def cond2str(self, subcond):
        if not subcond[0]: return None
        if subcond[1] == 1: # time
            return '(common.today - common.str2date("' + subcond[2] + '")).days > ' + str(subcond[3])
        elif subcond[1] == 2: # price
            t = ' > ' if subcond[3] else ' < '
            if subcond[2] == 1:
                return 'mqt[1]' + t + str(subcond[4])
            elif subcond[2] == 2:
                return 'mqt[1]' + t + 'mqt[2]*' + str(subcond[4])
            elif subcond[2] == 3:
                return 'mqt[1]' + t + 'mqt[3]*' + str(subcond[4])
            elif subcond[2] == 4:
                return 'mqt[1] < ' + 'mqt[4]*' + str(subcond[4])
            elif subcond[2] == 5:
                return 'mqt[1] > ' + 'mqt[5]*' + str(subcond[4])
            else:
                return 'False'
        else:
            return 'False'

    def show_cond(self):
        r = ''
        for cond in self.note[3:]:
            s = ''
            for i in cond[:]:
                t = self.cond2str(i)
                if t is None: continue
                s += t + ' and '

            if s: r += '(' + s[:-5] + ') or '
        r = r[:-4] if r else 'False'
        self.note[2][0] = r
        self.text[0] = self.note[2]



class TestApp(App):

    def build(self):
        self.row_height = Window.height / 10
        self.row_space = 10
        self.fd = [[False], [False, 'sh01', ['False'], [[False, 0, None, None, None]]]]
        self.note = [ False,
                      'sh01',
                      ['False'],
                      [common.init_cond()],
                      [common.init_cond(), [False, 2, 5, False, 1.0]]
                    ]

        notescr = NoteScreen(name='note_screen')
        root = ScreenManager()
        root.add_widget(notescr)
        return root


if __name__ == '__main__':

    kv = Builder.load_file("./notescreen.kv")
    TestApp().run()


#
