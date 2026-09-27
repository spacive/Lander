from textual.message import Message


class WidgetCommand(Message):

    def __init__(
        self,
        target: str,
        command: str,
        args: tuple = (),
        kwargs: dict | None = None,
    ) -> None:
        super().__init__()

        self.target = target
        self.command = command
        self.args = args
        self.kwargs = kwargs or {}