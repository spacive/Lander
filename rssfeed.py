import httpx
import feedparser
from readability import Document
from markdownify import markdownify
from textual.theme import Theme
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Header, Footer, ListView, ListItem, Label, Markdown, Static
from textual.widget import Widget 



RSS_URL = "https://feeds.bbci.co.uk/news/england/rss.xml"


async def fetch_feed(url: str):
    headers = {
        "User-Agent": "RSS Reader/1.0"
    }

    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()

    return feedparser.parse(response.text)


async def fetch_article(url: str) -> str:
    headers = {
        "User-Agent": "RSS Reader/1.0"
    }

    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()

   
    document = Document(response.text)
    article_html = document.summary()

    return markdownify(article_html)

class RSSApp(Widget):

    CSS_PATH = "rssfeed.tcss"

    articles = []

    def compose(self) -> ComposeResult:
        
        with Horizontal():
            yield ListView(id="articles")
            yield Markdown(
                "Select an article.",
                id="viewer"
            )

        

    async def on_mount(self):
        self.border_title = "News Feed"
        self.theme = "nord"
        list_view = self.query_one("#articles", ListView)

        try:
            feed = await fetch_feed(RSS_URL)

            self.articles = feed.entries

            for article in self.articles:
                title = article.get(
                    "title",
                    "Untitled article"
                )

                await list_view.append(
                    ListItem(Label(title))
                )

            list_view.focus()

        except Exception as error:
            viewer = self.query_one("#viewer", Markdown)

            viewer.update(
                f"# Failed to load feed\n\n"
                f"`{error}`"
            )

    async def on_list_view_selected(
        self,
        event: ListView.Selected
    ):
        index = event.list_view.index
        article = self.articles[index]

        title = article.get(
            "title",
            "Untitled article"
        )

        url = article.get("link")

        viewer = self.query_one("#viewer", Markdown)

        
        viewer.update(
            f"# {title}\n\n"
            "Loading article..."
        )

        try:
            content = await fetch_article(url)

            viewer.update(
                f"# {title}\n\n{content}"
            )

        except Exception as error:
            viewer.update(
                f"# {title}\n\n"
                f"Could not load the article.\n\n"
                f"`{error}`"
            )


if __name__ == "__main__":
    RSSApp().run()