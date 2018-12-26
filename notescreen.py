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

    def close_cond(self, condscr):
        self.text[0] = str(self.result)
        sm = self.notescr.manager
        sm.transition = SlideTransition(direction='right')
        sm.current = 'note_screen'
        sm.remove_widget(condscr)
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
            d = self.notescr.listscr.quota[self.index]
            #d = [0, [1,2,3,4,5,6]]
            if len(d) > 1:
                tm, Pr, Open, Close, Max, Min = d[-1]
            else:
                tm, Pr, Open, Close, Max, Min = [0]*6

            Pr = str(Pr)
            t = ' ~ '
            if cond[2] == 'Abs':
                r = Pr + t + str(cond[4])
            else:
                base = eval(cond[2])
                r = Pr + t + str(base) + ' * ' + str(cond[4]) + ' = ' + str(base * cond[4])

            self.result = cond[5]
            self.text[0] = self.result + '\n' + r
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

    def add_cond(self, cond=None):
        xi = len(self.condit)
        self.condit.append([common.init_cond()]) # [[]]
        self.rows.append(NoteRow(self, xi))
        self.ids.layout.add_widget(self.rows[-1])

    def add_subcond(self, row):
        self.condit[row.xi].append(common.init_cond()) # []
        self.refresh_cond()


    def del_cond(self, condscr):
        self.close_cond(condscr)
        del self.condit[self.xi][self.yi]
        if len(self.condit[self.xi]) == 0:
            del self.condit[self.xi]
        self.refresh_cond()


    def cond2str(self, subcond):
        if not subcond[0]: return None
        if subcond[1] == 1: # time
            return '(common.str2date(common.today()) - common.str2date("' + subcond[2] + '")).days > ' + str(subcond[3])
        elif subcond[1] == 2: # price
            t = ' > ' if subcond[3] else ' < '
            if subcond[2] == 1:
                return 'mq[1]' + t + str(subcond[4])
            elif subcond[2] == 2:
                return 'mq[1]' + t + 'mq[2]*' + str(subcond[4])
            elif subcond[2] == 3:
                return 'mq[1]' + t + 'mq[3]*' + str(subcond[4])
            elif subcond[2] == 4:
                return 'mq[1] < ' + 'mq[4]*' + str(subcond[4])
            elif subcond[2] == 5:
                return 'mq[1] > ' + 'mq[5]*' + str(subcond[4])
            else:
                return 'False'
        else:
            return 'False'

    def comment(self):
        r, n = '(', 0
        for i in self.rows:
            t = i.result
            if t == None: continue
            if i.xi > n and len(r) > 1: # Not ') or (' if previous None
                r = r[:-5] + ') or (' + t
                n = i.xi
            else:
                r += t

            r += ' and '
        r = r[:-5] + ')'
        self.text[0] = r
        return r


class TestApp(App):

    def build(self):
        self.row_height = Window.height / 10
        self.row_space = 10
        self.note = [ ['sh01', False, False],
                      [],
                      ['False'],
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
