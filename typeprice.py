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
            self.cond[1] = 2
            self.cond[2] = self.sym[0]
            self.cond[3] = self.sym[-1]
            self.cond[4] = 1.0

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
        t = str(self.cond[4])
        #print(self.cond)
        if self.cond[2] != self.sym[0]:
            r = 'CP ' + self.cond[3] + ' ' +  self.cond[2] + ' * ' + t
        else:
            r = 'CP ' + self.cond[3] + ' ' +  t

        self.text = [self.cond[2], self.cond[3], r]
        self.text[1] = self.cond[3]

#
