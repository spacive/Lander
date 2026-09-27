from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Checkbox, Static
from textual.widget import Widget


class Item:
    def __init__(self, name):
        self.__name = str(name)
        self.__state = False

    def ChangeState(self, value):
        self.__state = value

    def Rename(self, newname):
        self.__name = newname

    def GetName(self):
        return self.__name

    def GetState(self):
        return self.__state


class ToDoListApp(Widget):

    CSS_PATH = "todolist.tcss"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.todolist = []

    def compose(self) -> ComposeResult:
        yield VerticalScroll(id="todo-list")

    def on_mount(self):
        self.border_title = "To-do List"
        self.RefreshList()

    def CreateItem(self, name):
        self.todolist.append(Item(name))
        self.RefreshList()

    def RefreshList(self):
        container = self.query_one("#todo-list")

        container.remove_children()

        for todo in self.todolist:
            container.mount(
                Checkbox(
                    todo.GetName(),
                    value=todo.GetState()
                )
            )

    def ClearList(self):
        self.todolist = [
            todo for todo in self.todolist
            if not todo.GetState()
        ]

        self.RefreshList()

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        checkboxes = list(self.query(Checkbox))

        try:
            index = checkboxes.index(event.checkbox)
        except ValueError:
            return

        self.todolist[index].ChangeState(event.value)

    def handle_command(self, command, *args, **kwargs):
        commands = {
            "create": self.CreateItem,
            "refresh": self.RefreshList,
            "clear": self.ClearList,
        }

        function = commands.get(command)

        if function is None:
            return

        function(*args, **kwargs)