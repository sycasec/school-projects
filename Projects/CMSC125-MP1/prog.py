from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule

x = 30
y = 25
z = 69

r = Rule(title="blah", align="center")

stText = Text()
stText.append("Hello: ", style="bold")
stText.append(f"{x}", style="bold #00ff00")
stText.append("\n\nUsers: ", style = "bold")
stText.append(f"{y}", style="bold #ff8000")

console = Console()
console.print(r)
console.print(Panel.fit(stText), justify="center")
