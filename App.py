from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput

class App(GridLayout):
    def __init__(self, **kwargs):
        super(App,self).__init__(**kwargs)
        self.cols = 2
        

class CompilerApp(App):
    def build(self):
        textinput = TextInput(text='Hello World')
        return textinput


if __name__ == '__main__':
    CompilerApp().run()