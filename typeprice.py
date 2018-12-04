
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

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
