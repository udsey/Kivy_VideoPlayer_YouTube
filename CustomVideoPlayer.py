#https://www.youtube.com/watch?v=v8e-ukTAg5o&t=1916s

from kivy.animation import Animation
from kivy.core.window import Window
from kivy.metrics import sp, dp
from kivy.properties import ObjectProperty, Clock, BooleanProperty
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
    full_screen = BooleanProperty(False)
    title = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.mouse_pos_handler)
        Clock.schedule_once(self.add_file_name_label)


    def mouse_pos_handler(self, window_sdl, mouse_pos):
        expr = False

        if self.state == 'play' and not self.full_screen:
            expr = True
        if self.state == 'play' and self.full_screen:
            expr = True

        if expr:
            Clock.unschedule(self.hide_button_box())
            Clock.schedule_once(self.hide_button_box, 20)
            self.show_button_box()



    def hide_button_box(self, *args):

        def remove_button_box(*args):
            self.ids.button_box.height = 0

        button_box = self.ids.button_box

        for instance in [button_box.ids.btn_stop,
                         button_box.ids.btn_play_pause,
                         button_box.ids.btn_full_screen,
                         button_box.ids.volume_container,
                         button_box.ids.btn_volume,
                         button_box.ids.time,
                         button_box.ids.progress_container,
                         self.title]:
            Animation(opacity=0, d=0.2).start(instance)

        anim = Animation(opacity=0, d=0.2)
        anim.bind(on_complete=remove_button_box)
        anim.start(button_box.ids.progress_container)

    def show_button_box(self, *args):

        def add_button_box(*args):
            self.ids.button_box.height = dp(56)

        button_box = self.ids.button_box

        for instance in [button_box.ids.btn_stop,
                         button_box.ids.btn_play_pause,
                         button_box.ids.btn_full_screen,
                         button_box.ids.volume_container,
                         button_box.ids.btn_volume,
                         button_box.ids.time,
                         button_box.ids.progress_container,
                         self.title]:
            Animation(opacity=1, d=0.2).start(instance)
        anim = Animation(opacity=1, d=0.2)
        anim.bind(on_complete=add_button_box)
        anim.start(button_box.ids.progress_container)

    def set_time(self):
        seek = self.position / self.duration
        d = self.duration * seek
        minutes = int(d / 60)
        seconds = int(d - minutes * 60)
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

    def _play_started(self, instance, value):
        super()._play_started(instance, value)
        self.add_file_name_label()

    def on_state(self, instance, value):
        super().on_state(instance, value)
        if value == 'play':
            Clock.schedule_once(self.hide_button_box, 10)
        else:
            Clock.unschedule(self.hide_button_box)

    def on_full_screen(self, instance, value):
        def on_full_screen(*args):
            self.full_screen = value
            Animation(size_hint=(1, 1 if value else 0.3), d=0.2).start(self)

        Clock.schedule_once(on_full_screen, 0.4)


class PlayerContainer(MDFloatLayout):
    pass


#_________________________Slider_______________________________________

class ProgressBarVideo(MDProgressBar):
    video = ObjectProperty()

    def on_touch_down(self, touch):
        print('down')
        if not self.collide_point(*touch.pos):
            return
        touch.grab(self)
        self._update_seek(touch.x)
        return True

    def _update_seek(self, x):
        if  self.width == 0:
            return
        x = max(self.x, min(self.right, x)) - self.x
        self.video.seek(x / float(self.width))

    def on_touch_move(self, touch):
        print('move')
        if touch.grab_current is not self:
            return
        self._update_seek(touch.x)
        return True
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
    def on_release(self, *args):
        if not self.video.full_screen:
            self.video.full_screen = True
        else:
            self.video.full_screen = False
        return True

#______________________________________________________________________________________


class MainScreen(Screen):
    pass

class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Orange'
        return MainScreen()

if __name__ == '__main__':
    MyApp().run()