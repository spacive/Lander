from textual.app import ComposeResult
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Input

from message import WidgetCommand


class CommandInput(Input):

    class Command(Message):
        def __init__(self, command: str) -> None:
            self.command = command
            super().__init__()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        command = self.value.strip()

        self.value = ""

        if command:
            self.post_message(self.Command(command))


class CommandApp(Widget):

    def compose(self) -> ComposeResult:
        yield CommandInput(
            placeholder="enter command:",
            id="command_input"
        )

    def on_command_input_command(self, message: CommandInput.Command) -> None:
        self.handle_command(message.command)

    def handle_command(self, command: str) -> None:
        

        parts = command.split(maxsplit=2)

        if len(parts) < 2:
            
            return

        target = parts[0]
        command_name = parts[1]

        args = ()
        if len(parts) == 3:
            args = (parts[2],)

      

        self.post_message(
            WidgetCommand(
                target,
                command_name,
                args
            )
        )