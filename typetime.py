#
# Copyright (C) 2018 tobalanx@qq.com
#

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty

import datetime as dt
import common


class TypeTime(BoxLayout):
    text = ListProperty()

    def __init__(self, cond, **kwargs):
        self.cond = cond

        if not cond[1] == 1:
            cond[1] = 1
            cond[2] = common.today()
            cond[3] = 0
            cond[4] = None

        self.text = [None, cond[2]]
        self.comment()
        super().__init__(**kwargs)


    def on_text_time(self, text):
        try:
            self.cond[3] = int(text)
        except:
            self.cond[3] = 0

        self.comment()

    def comment(self):
        limit = common.str2date(self.cond[2]) + common.oneday * self.cond[3]
        t1 = (dt.date.today() - common.str2date(self.cond[2])).days
        self.text[0] = str(limit) + '\n' + str(t1) + ' / ' + str(self.cond[3]-t1)
        self.cond[4] = self.text[0]

    def set_today(self):
        self.cond[2] = common.today()
        self.text[1] = self.cond[2]


#
