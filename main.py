from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.video import Video
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from pytube import YouTube



class YouTubePlayerApp(App):
    def build(self):
        
        youtube_url = 'http://youtube.com/watch?v=2lAe1cqCOXo'
        
        
        layout = BoxLayout(orientation='vertical')
        source = self.get_youtube_video_url(youtube_url)
        video = VideoPlayer(source=source, state='play', options={'allow_stretch': True})
        layout.add_widget(video)
        return layout

    def get_youtube_video_url(self, youtube_url):
        yt = YouTube(youtube_url)
        video_stream = yt.streams.filter(res='720p').first()
        return video_stream.url

if __name__ == '__main__':
    YouTubePlayerApp().run()

