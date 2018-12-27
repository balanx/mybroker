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
from kivy.properties import ListProperty
from kivy.core.audio import SoundLoader
from kivy.clock import Clock


import common, notescreen, settingscreen, stock


class ListRow(BoxLayout):
    text = ListProperty(['']*5)

    def __init__(self, wisb, index, **kwargs):
        self.wisb = wisb
        self.index = index
        self.note = wisb.fd[1][index]
        super().__init__(**kwargs)
        self.show()

    def format(self, d1, d2):
        if not d2: return '0'
        d = 100*(d1-d2)/d2
        return ('%.2f' % d)

    def show(self, data=[0]*6):
        self.text[0] = self.note[0][0] + '\n' + ('%.2f' % data[2]) + '\n' + self.format(data[2], data[3]) + '%'
        self.text[1] = ('%.2f' % data[1]) + '\n' + self.format(data[1], data[3]) + '%'
        self.text[2] = ('%.2f' % data[4]) + '\n' + self.format(data[4], data[3]) + '%'
        self.text[3] = ('%.2f' % data[5]) + '\n' + self.format(data[5], data[3]) + '%'
        if not self.note[0][1]:
            self.text[4] = 'None'
        else:
            self.text[4] = str(len(self.note[2])) + (' #' if self.note[0][2] else '  ')


class ListScreen(Screen):
    rows = []
    mints = stock.minites_data()
    online = False
    sound = SoundLoader.load('./19.wav')
    mute = True
    text = ListProperty([online]) # online_symbol

    def __init__(self, wisb, **kwargs):
        self.app = wisb
        self.fd = wisb.fd
        super().__init__(**kwargs)
        self.refresh_list()
        #
        self.quota = [[[''],[0]*6]] * len(self.rows)
        self.event = Clock.schedule_once(self.rounds)


    def refresh_list(self):
        self.ids.layout.clear_widgets()
        self.rows.clear()
        for i in self.fd[1]:
            self.add_note(i)

    def add_note(self, note=None):
        if note is None:
            self.fd[1].append(common.init_note())
        self.rows.append(ListRow(self, len(self.rows)))
        self.ids.layout.add_widget(self.rows[-1])

    def open_note(self, row):
        self.index = row.index
        row.note[0][2] = False
        print('fd:', self.fd)
        print('row index in fd:', self.index)

        self.notescr = notescreen.NoteScreen(self, name='note_screen')
        self.manager.add_widget(self.notescr)
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'note_screen'

    def close_note(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'list_screen'
        self.manager.remove_widget(self.notescr)
        self.rows[self.index].note = self.fd[1][self.index]
        self.rows[self.index].show()

    def del_note(self):
        self.close_note()
        del self.fd[1][self.index]
        self.refresh_list()

    def rounds(self, dt=None):
        #select = 'sh000001,sz399006'
        if not self.rows: return
        codes = ''
        self.quota = []
        for i in self.rows:
            t = i.note[0][0]
            codes += t + ','
            self.quota.append([[t]])

        self.mints.gets(codes[:-1], self.quota)
        history = False
        for i in range(len(self.quota)):
            mq = self.quota[i][-1] # minites quotation
            #print('==q==', self.quota, mq)
            if len(mq) == 1 or not self.rows[i].note[0][1]: continue
            self.rows[i].show(mq)
            if self.rows[i].note[0][2]: history = True
            t = self.fd[1][i]
            tm, Pr, Open, Close, Max, Min = mq
            if mq[0] != 0:
                if not eval(t[1][0]) if (len(t[2]) % 2) else eval(t[1][0]):
                    t[2].append(mq[0])
                    self.rows[i].note[0][2] = True
                    self.app.save_fd()
                    history = True

        #print('rounds ...', mq)
        if history and self.sound.state == 'stop' and not self.mute:
            self.sound.play()

    def open_setting(self):
        self.manager.transition = SlideTransition(direction='right')
        self.settingscr = settingscreen.SettingScreen(self, name = 'setting_screen')
        self.manager.add_widget(self.settingscr)
        self.manager.current = 'setting_screen'

    def close_setting(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'list_screen'
        self.manager.remove_widget(self.settingscr)
        interval = self.fd[0][0]
        self.text[0] = self.online
        if self.event.is_triggered:
            self.event.cancel()
        if self.online:
            self.event = Clock.schedule_interval(self.rounds, interval)


#


class MainApp(App):
    fn = 'mybroker.json'

    def build(self):
        self.title = 'MyBroker'
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
            return [[3.0], []]
        with open(self.fn) as fd:
            return json.load(fd)

    def save_fd(self):
        with open(self.fn, 'w') as fd:
            json.dump(self.fd, fd)


if __name__ == '__main__':

    #kv = Builder.load_file("./main.kv")
    MainApp().run()

#
