import kivy
kivy.require('1.8.0')
from kivy.modules import inspector
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from valuearea import ValueAera
from slider_state import Slider
from kivy.app import App

class AttackSlider(Slider):
    def __init__(self,**kwargs):
        super(AttackSlider, self).__init__(**kwargs)

class Controller(FloatLayout):
     pass

class EnvApp(App):

    def build(self):
        fl = FloatLayout()
        inspector.create_inspector(Window, fl)
        ctrl=Controller()
        return ctrl

if __name__ == '__main__':
    EnvApp().run()
