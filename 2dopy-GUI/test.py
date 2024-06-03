from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

from textual.containers import ScrollableContainer
from textual.widgets import Button, Footer, Header, Static

class TimeDisplay(Static):
    """A widget to display elapsed time."""


class Stopwatch(Static):
    """A stopwatch widget."""

    def compose(self) -> ComposeResult:
        """Create child widgets of a stopwatch."""
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")
        yield Button("Reset", id="reset")
        yield TimeDisplay("00:00:00.00")


class MainApp(App):
    CSS_PATH = "textual.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self):
        yield Header()
        yield Footer()
        yield ScrollableContainer(Stopwatch(), Stopwatch(), Stopwatch())
    
    def action_toggle_dark(self):
        self.dark = not self.dark

if __name__ == "__main__":
    app = MainApp()
    app.run()