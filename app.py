from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen

from cmdprompt import CommandApp
from message import WidgetCommand

from rssfeed import RSSApp
from weather import Weather
from todolist import ToDoListApp


class MainScreen(Screen):

    def compose(self) -> ComposeResult:
        with Horizontal(id="main-area"):
            yield RSSApp(id="rss")

            with Vertical(id="right-column"):
                yield Weather(id="weather")
                yield ToDoListApp(id="todo")

        yield CommandApp(id="cmd")

    def on_widget_command(self, message: WidgetCommand) -> None:
        

        try:
            widget = self.query_one(f"#{message.target}")
        except Exception as e:
            
            return

        

        if hasattr(widget, "handle_command"):
            

            widget.handle_command(
                message.command,
                *message.args,
                **message.kwargs
            )
        else:
            pass
            


class MainApp(App):

    CSS_PATH = "app.tcss"

    def on_mount(self) -> None:
        self.theme = "nord"
        self.push_screen(MainScreen())


if __name__ == "__main__":
    MainApp().run()