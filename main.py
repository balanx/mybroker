#
# Copyright (C) 2018 tobalanx@qq.com
#

import json
from os.path import exists
from kivy.utils import platform
from kivy.app import App
#from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, StringProperty
from kivy.clock import Clock


import common, notescreen, settingscreen, stock


class ListRow(BoxLayout):
    #note = ListProperty()
    text = ListProperty(['']*5)

    def __init__(self, wisb, index, **kwargs):
        self.wisb = wisb
        self.index = index
        self.note = wisb.fd[index]
        super().__init__(**kwargs)
        self.show()

    def format(self, d1, d2):
        if not d2: return '0'
        d = 100*(d1-d2)/d2
        return ('%.2f' % d)

    def show(self, data=[0]*6):
        self.text[0] = self.note[1] + '\n' + ('%.2f' % data[2]) + '\n' + self.format(data[2], data[3]) + '%'
        self.text[1] = ('%.2f' % data[1]) + '\n' + self.format(data[1], data[3]) + '%'
        self.text[2] = ('%.2f' % data[4]) + '\n' + self.format(data[4], data[3]) + '%'
        self.text[3] = ('%.2f' % data[5]) + '\n' + self.format(data[5], data[3]) + '%'
        if not self.note[0]:
            self.text[4] = 'Stop'
        #elif len(self.note[2]) > 1:
        #    self.text[4] = str(self.note[2][1:])
        else:
            self.text[4] = str(len(self.note[2]) - 1)
        #print('==d==', self.note)


class ListScreen(Screen):
    text = ListProperty([False])
    rows = []
    mints = stock.minites_data()

    def __init__(self, wisb, **kwargs):
        self.app = wisb
        self.fd = wisb.fd
        self.interval = self.fd[0][0]
        super().__init__(**kwargs)
        self.refresh_list()
        #self.event = Clock.schedule_once(self.rounds)

    def refresh_list(self):
        self.ids.layout.clear_widgets()
        self.rows.clear()
        for i in self.fd[1:]:
            self.add_note(i)

    def add_note(self, note=None):
        if note is None:
            self.fd.append(common.init_note())
        self.rows.append(ListRow(self, len(self.rows) + 1))
        self.ids.layout.add_widget(self.rows[-1])

    def open_note(self, instance):
        self.index = instance.index
        print('fd:',  self.fd)
        print('row index in fd:',  self.index)

        self.notescr = notescreen.NoteScreen(self, name='note_screen')
        self.manager.add_widget(self.notescr)
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'note_screen'

    def close_note(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'list_screen'
        self.manager.remove_widget(self.notescr)
        self.rows[self.index - 1].note = self.fd[self.index]
        self.rows[self.index - 1].show()

    def del_note(self):
        self.close_note()
        del self.fd[self.index]
        self.refresh_list()

    def rounds(self, dt=None):
        #select = 'sh000001,sz399006'
        if not self.rows: return
        n = 1
        for i in self.rows:
            mqt = self.mints.get_one(i.note[1]) # mintes quoto
            i.show(mqt)
            t = self.fd[n][2]
            if mqt[0] != 0:
                if eval(t[0]) if (len(t) % 2) else not eval(t[0]):
                    t.append(mqt[0])
                    self.app.save_fd()
            n += 1
        #print('rounds ...')


    def open_setting(self):
        self.manager.transition = SlideTransition(direction='right')
        self.settingscr = settingscreen.SettingScreen(self, name = 'setting_screen')
        self.manager.add_widget(self.settingscr)
        self.manager.current = 'setting_screen'

    def close_setting(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'list_screen'
        self.manager.remove_widget(self.settingscr)
        self.interval = self.fd[0][0]
        if self.text[0]:
            self.event.cancel()
            self.event = Clock.schedule_interval(self.rounds, self.interval)

    def toggle_enable(self):
        self.text[0] = not self.text[0]
        if self.text[0]:
            self.event = Clock.schedule_interval(self.rounds, self.interval)
        elif self.event.is_triggered:
            self.event.cancel()

#


class MainApp(App):
    fn = 'mybroker.json'

    def build(self):
        self.row_height = Window.height / 10
        self.row_space = 10

        #self.fd = [ [3], common.init_cond(), , , ]
        self.fd = self.load_fd()
        listscr = ListScreen(self, name='list_screen')
        root = ScreenManager()
        root.add_widget(listscr)

        return root

    def load_fd(self):
        #print(platform)
        if platform == 'android':
            self.fn = '/storage/emulated/0/' + self.fn
        else:
            self.fn = './' + self.fn

        if not exists(self.fn):
            return [[3]]
        with open(self.fn) as fd:
            return json.load(fd)

    def save_fd(self):
        with open(self.fn, 'w') as fd:
            json.dump(self.fd, fd)


if __name__ == '__main__':

    #kv = Builder.load_file("./main.kv")
    MainApp().run()

#
