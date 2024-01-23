from kivy.app import App
from kivy.lang import Builder
from pytube import YouTube
from kivy.uix.screenmanager import  Screen

Builder.load_file("main.kv")



class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

    def play_video(self):
        sourse = self.ids.inpt.text
        if sourse:
            url, title = self.get_youtube_video_url(sourse)
            self.ids.video_player.source = url
            print(title)
            self.ids.lbl.text = title

    def get_youtube_video_url(self, youtube_url):
        yt = YouTube(youtube_url)
        title = yt.title
        video_stream = yt.streams.filter(res='720p').first()
        return video_stream.url, title




        #self.ids.video_player.source = url



class MyApp(App):
    def build(self):

        return MainScreen()





if __name__ == '__main__':
    MyApp().run()

