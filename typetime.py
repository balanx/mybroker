
from kivy.uix.boxlayout import BoxLayout

import common


class TypeTime(BoxLayout):

    def __init__(self, cond, **kwargs):
        super().__init__(**kwargs)
        self.cond = cond



#
