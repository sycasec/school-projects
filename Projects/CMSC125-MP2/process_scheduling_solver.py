from Logic import ProcessControlBoard
from rich.text import Text
from rich.panel import Panel 
from rich.layout import Layout 
from rich.table import Table
from rich.console import Console, Group
from rich.align import Align
from rich.columns import Columns
from rich.prompt import IntPrompt, Confirm, InvalidResponse
from rich import box
import sys

#a6e22e
#66d9ef
#be84ff
#f82558


def generateLayout() -> Layout:
    """define display layout""" 
    layout = Layout(name = "root")

    layout.split_row(
        Layout(name="process_list", size=35),
        Layout(name="main", ratio=2)
    )

    layout["main"].split_column(
        Layout(name="gantt_display"),
        Layout(name="tables"),
    )

    return layout

class Interface:
    def __init__(self):
        self.pcb = ProcessControlBoard()

    def read_file(self, filename):
        self.file = filename
        self.pcb.read_from_csv(filename)

    def generateProcessPanel(self) -> Panel:
        p_table = Table()
        p_table.add_column("P#", justify="center")
        p_table.add_column("A", justify="center")
        p_table.add_column("BT", justify="center")
        p_table.add_column("PRI", justify="center")

        for row in self.pcb.get_process_dict_as_list():
            p_table.add_row(
                f"{row[0]},",
                f"{row[1]},",
                f"{row[2]},",
                f"{row[3]}",
            )
    
    def generate_gantt_tops(self) -> str:    
        g_t = "╭"
        # for 
        pass

    def generateGanttPanel(self) -> Panel:
         
        # print("╭────┬┬────╮")
        # print("│ 01 ││ 10 │")
        # print("╰────┴┴────╯")
        # print("00   05   16")
        gantt_tops = "╭" 
        gantt_p = Panel(
            Align.center()
        )

    def generateCalculationsPanel(self) -> Panel:
        pass

    def generateMainDisplay(self):
        lt = generateLayout()
        lt['process_dict'].update(self.generateProcessPanel())
        lt['gantt_display'].udpate(self.generateGanttPanel())
        lt['tables'].update(self.generateCalculationsPanel())

if __name__ == "__main__":
    app = Interface()
    if len(sys.argv) > 1:
        app.read_file(sys.argv[1])
    else:
        # PROMPT FOR FILENAME
        pass

