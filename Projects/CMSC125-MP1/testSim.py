from time import sleep

from rich.table import Column
from rich.progress import Progress, BarColumn, TextColumn, track
from rich.table import Table
from rich.console import Console

test_tb = Table(title="Testing progress")

test_tb.add_column('Task')
test_tb.add_column('Progress')
with Progress() as progress:
    task1 = progress.add_task("Task 1", total=100)
    task2 = progress.add_task("Task 2", total=200)

    while not progress.finished:

        # Update the progress bar for each task
        progress.update(task1, advance=1)
        progress.update(task2, advance=2)

        # Update the table with the progress bar values
        test_tb.add_row(
            ["Task 1", progress.get_task_percent(task1)],
        )

console = Console()
console.print(test_tb)
        # import logging
# from rich.logging import RichHandler

# logging.basicConfig(
        #     level="NOTSET",:wq
#     format="%(message)s",
#     datefmt="[%X]",
#     handlers=[RichHandler(rich_tracebacks=True)]
# )

# log = logging.getLogger("rich")
# try:
#     print(1 / 0)
# except Exception:
#     log.exception("unable print!")

# import random
# import time

# from rich.live import Live
# from rich.table import Table


# def generate_table() -> Table:
#     """Make a new table."""
#     table = Table()
#     table.add_column("ID")
#     table.add_column("Value")
#     table.add_column("Status")

#     for row in range(random.randint(2, 6)):
#         value = random.random() * 100
#         table.add_row(
#             f"{row}", f"{value:3.2f}", "[red]ERROR" if value < 50 else "[green]SUCCESS"
#         )
#     return table


# with Live(generate_table(), refresh_per_second=4) as live:
#     for _ in range(40):
#         time.sleep(0.4)
#         live.update(generate_table())


