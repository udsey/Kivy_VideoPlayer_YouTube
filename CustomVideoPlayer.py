from kivy.metrics import sp
from kivy.properties import ObjectProperty, Clock
from kivy.uix.videoplayer import VideoPlayer
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar

Builder.load_file('CustomVideoPlayer.kv')

class CustomVideoPlayer(VideoPlayer):
    title = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.add_file_name_label)

    def set_time(self):
        seek = self.position / self.duration
        d = self.duration * seek
        minutes = int(d / 60)
        seconds = int(d - minutes)
        self.ids.button_box.ids.time.text = "%d:%02d" % (minutes, seconds)

    def add_file_name_label(self, *args):
        if not self.title:
            self.title = MDLabel(
                text=self.source,
                pos_hint={'top': 0.93},
                bold=True,
                adaptive_height=True,
                theme_text_color='Custom',
                text_color='white',
                x='24dp',
                )
        self.ids.container.add_widget(self.title)



class PlayerContainer(MDFloatLayout):
    pass


#_________________________Slider_______________________________________

class ProgressBarVideo(MDProgressBar):
    video = ObjectProperty()



#____________________Control Buttons___________________________________
class PlayerButtonBox(MDGridLayout):
    video = ObjectProperty()


class BasePlayerButton(MDIconButton):
    video = ObjectProperty()
    theme_icon_color = 'Custom'
    icon_color =  1, 1, 1, 0.85
    icon_size = sp(25)

class ButtonVideoStop(BasePlayerButton):
    def on_release(self, *args):
        self.video.state = 'stop'
        return True

class ButtonVideoPlayPause(BasePlayerButton):
    def on_release(self, *args):
        self.video.state = 'pause' if self.video.state == 'play' else 'play'
        return True


class ButtonVideoVolume(BasePlayerButton):
    pass

class ButtonVideoFullScreen(BasePlayerButton):
    pass

#______________________________________________________________________________________

class MainScreen(Screen):
    pass

class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Orange'
        return MainScreen()

if __name__ == '__main__':
    MyApp().run()