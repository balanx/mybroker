#
# Copyright (C) 2018 tobalanx@qq.com
#

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

from kivy.uix.popup import Popup
from kivy.uix.button import Button

from kivy.properties import BooleanProperty

import datetime as dt

oneday = dt.timedelta(days=1)
#today = dt.datetime.today() + dt.timedelta(hours=8)
def today():
    t = dt.datetime.today()
    w =int2week(t.weekday())
    return str(t)[:-7] + ' ' + w

def str2date(t):
    t = t[:-13].split('-')
    t = dt.date(int(t[0]), int(t[1]), int(t[2]))
    return t

def int2week(t):
    if t == 0: return 'Mon'
    elif t == 1: return 'Tue'
    elif t == 2: return 'Wed'
    elif t == 3: return 'Thu'
    elif t == 4: return 'Fri'
    elif t == 5: return 'Sat'
    elif t == 6: return 'Sun'
    else: return str(t)

#
def init_cond():
    return [False, 0, None, None, None]

def init_note():
    #               enable  soundon   debug     Log    condit
    return [['sh01', False, False], ['eval()'], [ ], [[init_cond()]] ]
    # condit = [ [c1 and c2 and ... ] or [] or ... ]

#     interval
# fd = [[3], []]
#    = [[3], [n1, n2, ...]]
#

#
# quota = [ [['sh000001'], [tm, curr, open, close, max, min], ],
#           [['sz399006'], [tm, curr, open, close, max, min], ] ]
#
# [[[''],[0]*6]] * n

class ConfirmPopup(Popup):
    result = BooleanProperty(False)



class TestApp(App):

    def build(self):
        self.menu_height = Window.height / 10
        self.pop = ConfirmPopup(on_dismiss=self.show)
        print(self.pop)
        btn = Button(text='popup', on_release=self.pop.open)

        return btn

    def show(self, instance):
        print(self.pop.result)
        print(instance)



if __name__ == '__main__':

    kv = Builder.load_file("./common.kv")
    TestApp().run()

#
