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

#date = dt.date
today = dt.date.today()
oneday = dt.timedelta(days=1)
#today = dt.datetime.today() + dt.timedelta(hours=8)

def timechk(cond):
    t = dt.date(*cond[2])
    limit = t + oneday * cond[3]
    t = (today - t).days
    cond[4] = cond[3] - t
    return str(limit) + '\n' + str(t) + ' : ' + str(cond[4])


#
def init_cond():
    return [False, 0]

def init_note():
    #                     enable  history
    return [ [ 'sh000001', False, False ],
             [ 'eval()', [[0]*6] ], # debug, quota
             [ ], # log
             [ [ init_cond() ] ] # condit = [ [c1 and c2 and ... ] or [] or ... ]
           ]


#  interval online
# fd = [[3, True], []]
#    = [[3, True], [n1, n2, ...]]
#

#
# quota = [ [['sh000001'], [tm, curr, open, close, max, min], ],
#           [['sz399006'], [tm, curr, open, close, max, min], ] ]
#
# [[[''],[0]*6]] * n


def reso1(d): return ('%.2f' % d)
def reso2(d): return ('%.3f' % d)


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
