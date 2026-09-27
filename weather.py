import httpx
from rich.text import Text
from textual.widgets import Static


class Weather(Static):

    CSS_PATH = "weather.tcss"

    async def on_mount(self) -> None:
        await self.update_weather()
        self.border_title = "Weather"
        self.styles.padding = 1

    async def update_weather(self) -> None:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://wttr.in/London?0Q")
            response.raise_for_status()

        self.update(Text.from_ansi(response.text))