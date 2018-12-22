#
# Copyright (C) 2018 tobalanx@qq.com
#

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import ListProperty

import common, condscreen


class NoteSubRow(BoxLayout):
    text = ListProperty([''])

    def __init__(self, wisb, t1, t2, **kwargs):
        self.wisb = wisb
        self.t1 = t1
        self.t2 = t2
        self.cond = wisb.note[t1][t2]
        wisb.show_row(self)
        super().__init__(**kwargs)


class NoteRow(BoxLayout):
    text = ListProperty([''])
    t2 = 0

    def __init__(self, wisb, t1, **kwargs):
        self.wisb = wisb
        self.t1 = t1
        self.cond = wisb.note[t1][0]
        wisb.show_row(self)
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

    def close_cond(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'note_screen'
        self.manager.remove_widget(self.condscr)
        #self.rows[self.t3].cond = self.note[self.t1][self.t2]
        self.show_row(self.rows[self.t3])
        self.show_cond()

    def del_cond(self, instance):
        self.close_cond(instance)
        del self.note[self.t1][self.t2]
        if len(self.note[self.t1]) == 0:
            del self.note[self.t1]
        self.refresh_cond()


    def cond2str(self, subcond):
        if not subcond[0]: return None
        if subcond[1] == 1: # time
            return '(common.str2date(common.today()) - common.str2date("' + subcond[2] + '")).days > ' + str(subcond[3])
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
        self.note[1][0] = r
        self.text[0] = r + '\n' + str(self.note[2])
        return r

    def show_row(self, row):
        cond = row.cond
        if not cond[0]:
            row.text[0] = 'None'
        elif cond[1] == 1:
            row.text[0] = row.cond[4]
        elif cond[1] == 2:
            t = ' > ' if cond[3] else ' < '
            data = self.wisb.qt[self.index-1]
            pr = str(data[1][1])
            open = data[1][2]
            close = data[1][3]
            max = data[1][4]
            min = data[1][5]
            if cond[2] == 2:
                r = 'P' + t + 'open * ' + str(cond[4]) + '\n' + pr + ' ~ ' + str(open) + ' * ' + str(cond[4]) + ' = ' + str(open * cond[4])
            elif cond[2] == 3:
                r = 'P' + t + 'close * ' + str(cond[4]) + '\n' + pr + ' ~ ' + str(close) + ' * ' + str(cond[4]) + ' = ' + str(close * cond[4])
            elif cond[2] == 4:
                r = 'P < ' + 'max * ' + str(cond[4]) + '\n' + pr + ' ~ ' + str(max) + ' * ' + str(cond[4]) + ' = ' + str(max * cond[4])
            elif cond[2] == 5:
                r = 'P > ' + 'min * ' + str(cond[4]) + '\n' + pr + ' ~ ' + str(min) + ' * ' + str(cond[4]) + ' = ' + str(min * cond[4])
            else: #if cond[2] == 1:
                r = 'P' + t + str(cond[4]) + '\n' + pr + ' ~ ' + str(cond[4])
            row.text[0] = r
        else:
            row.text[0] = 'None'


class TestApp(App):

    def build(self):
        self.row_height = Window.height / 10
        self.row_space = 10
        self.fd = [[False], [['sh01', False, False], [], ['False'], [[False, 0, None, None, None]]]]
        self.note = [ ['sh01', False, False],
                      [],
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
