
from kivy.uix.boxlayout import BoxLayout

import common


class TypeTime(BoxLayout):

    def __init__(self, cond, **kwargs):
        super().__init__(**kwargs)
        self.cond = cond

        if not cond[0] == 1:
            self.cond[0] = 1
            self.cond[1] = common.datetime.date.today()
            self.cond[2] = 0
            self.cond[3] = common.datetime.date.today()

        self.ids.txi_start.text = str(self.cond[1])
        self.ids.txi_limit.text = str(self.cond[2])
        self.print_comment()


    def on_text_time(self, text):
        try:
            self.cond[2] = int(text)
        except:
            self.cond[2] = 0

        self.cond[3] = self.cond[1] + common.oneday * self.cond[2]
        self.print_comment()


    def print_comment(self):
        self.ids.lb_comment.text = 'Deadline is ' + str(self.cond[3])


#
