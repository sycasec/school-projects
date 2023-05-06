from rich.console import Console as cs
from rich.text import Text
from rich.panel import Panel

c = cs()
t1 = Text("Hello World")
t2 = Text("Goodbye World")
c.print(Panel.fit([t1,t2]))

