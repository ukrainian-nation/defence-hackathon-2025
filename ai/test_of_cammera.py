# Requires Kivy and PyOBJUS (Android only)
from kivy.app import App
from kivy.uix.camera import Camera

class CameraApp(App):
    def build(self):
        return Camera(play=True, index=0)

CameraApp().run()