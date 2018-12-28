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

    def __init__(self, listscr, index, **kwargs):
        self.listscr = listscr
        self.index = index
        self.note = listscr.fd[1][index]
        super().__init__(**kwargs)
        self.show()

    def format(self, d1, d2):
        if not d2: return '0'
        d = 100*(d1-d2)/d2
        return common.reso1(d)

    def show(self):
        data = self.note[1][1][-1]
        self.text[0] = self.note[0][0] + '\n' + common.reso1(data[2]) + '\n' + self.format(data[2], data[3]) + '%'
        self.text[1] = common.reso1(data[1]) + '\n' + self.format(data[1], data[3]) + '%'
        self.text[2] = common.reso1(data[4]) + '\n' + self.format(data[4], data[3]) + '%'
        self.text[3] = common.reso1(data[5]) + '\n' + self.format(data[5], data[3]) + '%'
        if not self.note[0][1]:
            self.text[4] = 'None'
        else:
            self.text[4] = str(len(self.note[2])) + (' #' if self.note[0][2] else '  ')


class ListScreen(Screen):
    rows = []
    mints = stock.minites_data()
    #online = True
    sound = SoundLoader.load('./19.wav')
    mute = True
    codes = ''
    #trig_once = False
    text = ListProperty() # online_symbol

    def __init__(self, app, **kwargs):
        self.app = app
        self.fd = app.fd
        self.text.append(self.fd[0][1]) # online
        super().__init__(**kwargs)
        self.refresh_list()
        #
        interval = self.fd[0][0]
        self.event = Clock.schedule_interval(self.rounds, interval)
        if not self.text[0]: # online
            self.event.cancel()


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
        self.get_codes()

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
        #print('close:', self.rows[self.index].note, self.fd[1][self.index])
        #self.rows[self.index].note = self.fd[1][self.index]
        self.rows[self.index].show()
        self.get_codes()

    def del_note(self):
        self.close_note()
        del self.fd[1][self.index]
        self.refresh_list()

    def get_codes(self):
        #codes = 'sh000001,sz399006'
        t = ''
        for i in self.fd[1]:
            t += i[0][0] + ','
            self.codes = t[:-1]

    def rounds(self, dt):
        if not self.rows: return
        now = common.dt.datetime.now()
        if (  now.hour <= 8  or \
             (now.hour == 9  and now.minute < 25) or \
             (now.hour == 11 and now.minute > 30) or \
              now.hour == 12 or \
              now.hour >= 15    \
           ) and \
           dt: # dt = 0, trigger once
            return

        quota = self.mints.get_one(self.codes)
        history = False
        for i in range(len(quota)):
            name = quota[i][0]
            mq = quota[i][1:] # minites quotation
            t = self.fd[1][i]
            #print('==q==', t, mq)
            if name != t[0][0]: continue
            tm, Pr, Open, Close, Max, Min = mq
            t[1][1][-1] = mq
            if mq[0] != 0:
                if not eval(t[1][0]) if (len(t[2]) % 2) else eval(t[1][0]):
                    t[2].append(mq[0]) # Log
                    self.rows[i].note[0][2] = True # history
                    self.app.save_fd()
                    history = True

            self.rows[i].show()
            if self.rows[i].note[0][2]: history = True

        print('rounds ...', now, mq)
        #self.trig_once = False
        #if not self.online:
        #    self.event.cancel()
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
        self.text[0] = self.fd[0][1] # online
        self.event.cancel()
        if self.text[0]: # online
            interval = self.fd[0][0]
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
            return [[3.0, True], []]
        with open(self.fn) as fd:
            return json.load(fd)

    def save_fd(self):
        with open(self.fn, 'w') as fd:
            json.dump(self.fd, fd)


if __name__ == '__main__':

    #kv = Builder.load_file("./main.kv")
    MainApp().run()

#
