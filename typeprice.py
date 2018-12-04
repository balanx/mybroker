
from kivy.uix.boxlayout import BoxLayout

import common


class TypePrice(BoxLayout):

    def __init__(self, cond, **kwargs):
        super().__init__(**kwargs)
        self.cond = cond

    def on_checkbox1_active(self, instance, text):
        if instance.active:
            print(text)

    def on_checkbox2_active(self, instance, text):
        if instance.active:
            print(text)


#
