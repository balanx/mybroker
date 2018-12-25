#
# Copyright (C) 2018 tobalanx@qq.com
#

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty

import common


class TypeTime(BoxLayout):
    text = ListProperty()

    def __init__(self, cond, **kwargs):
        self.cond = cond

        if not cond[1] == 1:
            cond[1] = 1
            cond[2] = self.date2list(common.today)
            cond[3] = 0
            cond[4] = None

        self.text = [common.timechk(self.cond), str(cond[2])]
        super().__init__(**kwargs)


    def on_text_time(self, text):
        try:
            self.cond[3] = int(text)
        except:
            self.cond[3] = 0

        self.text[0] = common.timechk(self.cond)


    def set_today(self):
        self.cond[2] = self.date2list(common.today)
        self.text[1] = str(self.cond[2])

    def date2list(self, d):
        d = str(d)
        d = [d[:4], d[5:7], d[8:]]
        return list(map(int, d))


#
