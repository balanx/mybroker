
from kivy.uix.boxlayout import BoxLayout

import common


class TypePrice(BoxLayout):

    def __init__(self, cond, **kwargs):
        self.cond = cond
        cond[1] = 2
        super().__init__(**kwargs)

        if cond[2] == 2:
            self.ids.cb_open.active = True
        elif cond[2] == 3:
            self.ids.cb_close.active = True
        elif cond[2] == 4:
            self.ids.cb_max.active = True
        elif cond[2] == 5:
            self.ids.cb_min.active = True
        else: #if cond[2] == 1:
            self.ids.cb_abs.active = True

        if cond[3]:
            self.ids.cb_more.active = True
        else:
            self.ids.cb_less.active = True

        self.ids.txi_val.text = str(cond[4])


    def on_checkbox_active(self, instance, n):
        if instance.active:
            if n < 10:
                self.cond[2] = n
            elif n == 10: # more
                self.cond[3] = True
            else: # if n == 11: # less
                self.cond[3] = False


    def on_text_val(self, text):
        try:
            self.cond[4] = float(text)
        except:
            self.cond[4] = 0.0


#
