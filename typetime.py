
from kivy.uix.boxlayout import BoxLayout

import common


class TypeTime(BoxLayout):

    def __init__(self, cond, **kwargs):
        super().__init__(**kwargs)
        self.cond = cond

        if not cond[1] == 1:
            cond[1] = 1
            cond[2] = str(common.datetime.date.today())
            cond[3] = 0
            cond[4] = str(common.datetime.date.today())

        self.ids.txi_start.text = str(cond[2])
        self.ids.txi_limit.text = str(cond[3])
        self.print_comment()


    def on_text_time(self, text):
        try:
            self.cond[3] = int(text)
        except:
            self.cond[3] = 0

        self.cond[4] = str(self.str2date(self.cond[2]) + common.oneday * self.cond[3])
        self.print_comment()

    def str2date(self, dt):
        t = dt.split('-')
        t = common.datetime.date(int(t[0]), int(t[1]), int(t[2]))
        return t

    def print_comment(self):
        self.ids.lb_comment.text = 'Deadline is ' + str(self.cond[4])


#
