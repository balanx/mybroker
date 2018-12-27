#
# Copyright (C) 2018 tobalanx@qq.com
#

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty

import common


class TypePrice(BoxLayout):
    text = ListProperty()
    sym = ['Abs', 'Open', 'Close', 'Max', 'Min', '>', '<']

    def __init__(self, cond, **kwargs):
        self.cond = cond
        if cond[1] != 2:
            del cond[1:]
            cond.extend([2, self.sym[0], self.sym[-1], 1.0, None])

        self.comment()
        super().__init__(**kwargs)


    def on_checkbox_active(self, instance, n):
        if instance.active:
            if n < 5:
                self.cond[2] = self.sym[n]
                if n == 3: # Max
                    self.cond[3] = self.sym[6]
                elif n == 4: # Min
                    self.cond[3] = self.sym[5]
            elif self.cond[2] != self.sym[3] and self.cond[2] != self.sym[4]:
                self.cond[3] = self.sym[n]

        self.comment()

    def on_text_val(self, text):
        try:
            self.cond[4] = float(text)
        except:
            self.cond[4] = 1.0

        self.comment()

    def comment(self):
        t = common.reso2(self.cond[4])
        if self.cond[2] != self.sym[0]:
            r = 'Pr ' + self.cond[3] + ' ' +  self.cond[2] + ' * ' + t
        else:
            r = 'Pr ' + self.cond[3] + ' ' +  t

        self.cond[5] = r
        self.text = [self.cond[2], self.cond[3], r]
        self.text[1] = self.cond[3]

#
