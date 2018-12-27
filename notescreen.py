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


class NoteRow(BoxLayout):
    text = ListProperty([''])
    result = ''

    def __init__(self, notescr, xi, yi, ri, **kwargs):
        self.notescr = notescr
        self.xi, self.yi, self.ri = xi, yi, ri
        self.condit = notescr.condit
        self.cond = self.condit[xi][yi]
        self.show()
        super().__init__(**kwargs)

    def open_cond(self):
        self.condscr = condscreen.CondScreen(self, name='cond_screen')
        sm = self.notescr.manager
        sm.add_widget(self.condscr)
        sm.transition = SlideTransition(direction='left')
        sm.current = 'cond_screen'

    def close_cond(self):
        self.text[0] = str(self.result)
        sm = self.notescr.manager
        sm.transition = SlideTransition(direction='right')
        sm.current = 'note_screen'
        sm.remove_widget(self.condscr)
        self.show()
        self.notescr.comment()

    def show(self):
        cond = self.cond
        if not cond[0]: # disable
            self.result = None
            self.text[0] = str(None)
        elif cond[1] == 1:
            self.result = str(False) if cond[4] > 0 else str(True)
            self.text[0] = common.timechk(cond)
        elif cond[1] == 2:
            #print('====', self.notescr.note)
            d = self.notescr.note[1][1]
            #d = [[1,2,3,4,5,6]]
            tm, Pr, Open, Close, Max, Min = d[-1]
            if cond[2] == 'Abs':
                r = cond[2]
            else:
                base = eval(cond[2])
                r = common.reso1(base) + ' * ' + common.reso2(cond[4]) + ' = ' + common.reso1(base * cond[4])

            self.result = cond[5]
            self.text[0] = common.reso1(Pr) + self.result[2:] + '\n' + r
        else: # type = 0
            self.result = None
            self.text[0] = str(None)



class NoteScreen(Screen):
    text = ListProperty([''])
    rows = []

    def __init__(self, listscr, **kwargs):
        self.index = listscr.index
        self.listscr = listscr
        self.note = listscr.fd[1][self.index]
        self.condit = self.note[3]
        super().__init__(**kwargs)
        self.refresh_cond()

    def refresh_cond(self):
        self.ids.layout.clear_widgets()
        self.rows.clear()
        # [ False, 'sh01', ['Log'], [condition, ... ] ]
        xi, ri = 0, 0
        for cond in self.condit:
            yi = 0
            for i in cond:
                t = NoteRow(self, xi, yi, ri)
                self.rows.append(t)
                self.ids.layout.add_widget(t)
                ri += 1
                yi += 1
            xi += 1
        self.comment()

    def add_cond(self):
        xi = len(self.condit)
        ri = len(self.rows)
        self.condit.append([common.init_cond()]) # [[]]
        self.rows.append(NoteRow(self, xi, 0, ri))
        self.ids.layout.add_widget(self.rows[-1])

    def add_subcond(self, row):
        self.condit[row.xi].append(common.init_cond()) # []
        self.refresh_cond()

    def del_cond(self, row):
        row.close_cond()
        del self.condit[row.xi][row.yi]
        if len(self.condit[row.xi]) == 0:
            del self.condit[row.xi]
        self.refresh_cond()

    def comment(self):
        r, n = '', 0
        for i in self.rows:
            t = i.result
            if t == None: continue
            if i.xi > n and len(r) > 0: # Not ') or (' if previous None
                r = r[:-5] + ') or (' + t
                n = i.xi
            else:
                r += t

            r += ' and '

        r = str(False) if len(r) == 0 else '(' + r[:-5] + ')'
        self.note[1][0] = r
        self.text[0] = r + '\n' + str(self.note[2])
        return r


class TestApp(App):

    def build(self):
        self.row_height = Window.height / 10
        self.row_space = 10
        self.note = [ ['sh01', False, False],
                      [ 'eval()', [[0]*6] ], # debug, quota
                      [],
                      [ [ common.init_cond(), [False, 0, 5, False, 1.0] ],
                        [ common.init_cond() ]
                      ]
                    ]
        self.fd = [[False], [self.note]]
        self.index = 0

        notescr = NoteScreen(self, name='note_screen')
        root = ScreenManager()
        root.add_widget(notescr)
        return root


if __name__ == '__main__':

    kv = Builder.load_file("./notescreen.kv")
    TestApp().run()


#
