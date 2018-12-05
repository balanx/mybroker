
from kivy.uix.boxlayout import BoxLayout

import common


class TypePrice(BoxLayout):

    def __init__(self, cond, **kwargs):
        super().__init__(**kwargs)
        self.cond = cond
        cond[0] = 2

        if cond[1] == 1:
            self.ids.cb_abs.active = True
        elif cond[1] == 2:
            self.ids.cb_open.active = True
        elif cond[1] == 3:
            self.ids.cb_close.active = True
        elif cond[1] == 4:
            self.ids.cb_max.active = True
        elif cond[1] == 5:
            self.ids.cb_min.active = True

        if cond[2]:
            self.ids.cb_more.active = True
        else:
            self.ids.cb_less.active = True

        self.ids.txi_val.text = str(cond[3])


    def on_checkbox_active(self, instance, n):
        if instance.active:
            if n < 10:
                self.cond[1] = n
            elif n == 10: # more
                self.cond[2] = True
            elif n == 11: # less
                self.cond[2] = False



    def on_text_val(self, text):
        try:
            self.cond[3] = float(text)
        except:
            self.cond[3] = 0.0


#
