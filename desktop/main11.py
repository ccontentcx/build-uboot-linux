from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.network.urlrequest import UrlRequest
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.utils import platform
import os

# Register the font
LabelBase.register(
    name="my_font",
    fn_regular=os.path.join(os.path.dirname(__file__), "assets", "fonts", "msyhl.ttc")
)

class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = "https://jsonplaceholder.typicode.com/todos/1"
        self.label = None
        self.data = "Fetching data..."

    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.label = Label(
            text=self.data,
            font_name="my_font",
            font_size=30,
            halign='center',
            valign='middle',
            size_hint=(1, 1)
        )
        layout.add_widget(self.label)
        self.fetch_data()
        return layout

    def fetch_data(self):
        self.label.text = "Fetching data..."
        UrlRequest(
            url=self.url,
            on_success=self.on_success,
            on_failure=self.on_failure,
            on_error=self.on_error
        )

    def on_success(self, request, result):
        self.data = str(result)
        self.label.text = self.data

    def on_failure(self, request, result):
        self.label.text = f"Failed to fetch data: {result}"

    def on_error(self, request, error):
        self.label.text = f"Error: {error}"

    def on_resume(self):
        if platform == 'android':
            Clock.schedule_once(lambda dt: self.fetch_data(), 0)

if __name__ == '__main__':
    MyApp().run()