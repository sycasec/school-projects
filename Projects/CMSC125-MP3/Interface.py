import time
import os
import sys

from Logic import MemoryAllocator
from rich import box
from rich.live import Live
from rich.text import Text
from rich.panel import Panel 
from rich.layout import Layout 
from rich.table import Table
from rich.console import Console, Group
from rich.align import Align
from rich.columns import Columns
from rich.prompt import IntPrompt, Prompt, Confirm 


from copy import deepcopy

def generateLayout() -> Layout:
    """define display layout""" 
    layout = Layout(name = "root")

    layout.split_column(
        Layout(name="header", size=17),
        Layout(name="main", ratio=2),
    )

    layout["main"].split_row(
        Layout(name="Memory"),
        Layout(name="Jobs"),
    )

    return layout


class Interface:

    def __init__(self):
        self.ma = MemoryAllocator()
        self.total_frag_list = []
        self.total_util_list = []
        self.total_wait_list = []
        self.execution_time = 0
        self.colors = {
            "green": "#a6e22e",
            "blue":"#66d9ef",
            "purple":"#8f32e4",
            "red":"#f4155a",
            "pink": "#f200f4",
            "teal": "#00B19F",
            "yellow": "#f2ed00",
            "amber": "#FBC02D"
        }

    # HELPER METHODS 
    def error_message(self, errmsg):
        eTxt = Text()
        eTxt.append(f"ERROR! -> {errmsg}", style="bold #bf2e35")
        return eTxt


    def read_file(self, memfile, jobfile):
        self.ma.read_from_file(memfile, jobfile)

    def get_job_time(self, jobID):
        if jobID == -1:
            return jobID
        return self.ma.get_jobs()[jobID]['time']

    # ANALYSIS FUNCTIONS

    def get_average_throughput(self):
        total_done = self.ma.get_done()
        total_time = self.execution_time

        return total_done / total_time

    def get_total_average_fragmentation(self):
        return sum(self.total_frag_list) / len(self.total_frag_list)

    def get_total_average_utilization(self):
        return sum(self.total_util_list) / len(self.total_util_list)     

    # MAIN METHODS

    def generateMemoryLayout(self) -> Panel:
        m_table = Table(title=f"[{self.colors['red']}]Memory List", style=self.colors["teal"])
        m_table.add_column("Memory #", justify="right")
        m_table.add_column("Job", justify="right")
        m_table.add_column("Size", justify="center")
        m_table.add_column("Adjusted Size", justify="center")
        m_table.add_column("Time Left", justify="right")

        for m_id, m_data in self.ma.get_blocks().items():
            m_table.add_row(
                f"{m_id}",
                f"{m_data['job']}",
                f"{m_data['size']}",
                f"{m_data['a_size']}",
                f"{self.get_job_time(m_data['job'])}"
            )
        
        m_Panel = Panel(
            Align.center(m_table),
            box=box.ROUNDED,
            border_style=self.colors["red"]
        )

        return m_Panel 

    def generateJobLayout(self) -> Panel:
        j_table = Table(title=f"[{self.colors['blue']}]Title", style=self.colors["purple"])
        j_table.add_column("Job #", justify="right")
        j_table.add_column("Size", justify="center")
        j_table.add_column("Status", justify="center")
        j_table.add_column("Time", justify="center")
        j_table.add_column("Wait Time", justify="center")
        j_table.add_column("Time Left", justify="right")

        for j_id, j_data in self.ma.get_jobs().items():
            j_table.add_row(
                f"{j_id}",
                f"{j_data['size']}",
                f"{j_data['status']}",
                f"{j_data['wait']}",
                f"{self.ma.jobs_copy[j_id]['time']}",
                f"{j_data['time']}"
            )

        j_Panel = Panel(
            Align.center(j_table),
            box=box.ROUNDED,
            border_style=self.colors["yellow"]
        )

        return j_Panel

    def generateStatsLayout(self) -> Panel:
        stringed_frag = "["
        for v in self.ma.get_fragmentation():
            stringed_frag += f" {v*100:.2f}%"
        stringed_frag += " ]"

        header_message = Table.grid(padding=1)
        header_message.add_column(style=f"{self.colors['amber']}", justify="right")
        header_message.add_column(no_wrap=True)

        header_message.add_row(
            "Average Fragmentation (Across all Blocks):",
            f"[b #ff7270] [ {(self.ma.get_average_fragmentation())*100:.2f}% ]"
        )

        header_message.add_row(
            "Individual Fragmentation:",
            f"[b #ff7270] {stringed_frag}"
        )

        header_message.add_row(
            "Average Memory Utilization:",
            f"[b {self.colors['teal']}] {self.ma.get_utilization() * 100:.2f}"
        )

        header_message.add_row(
            "Fat Jobs:",
            f"[b {self.colors['red']}] {self.ma.fat_jobs()}"
        )

        header_message.add_row(
            "Total Time Left:",
            f"[b {self.colors['green']}] {self.ma.get_total_time()}"
        )

        header_message.add_row(
            "Running Time:",
            f"[b {self.colors['green']}] {self.execution_time}"
        )

        header_message.add_row(
            "Wait Queue:",
            f"[b {self.colors['green']}] {self.ma.waitQueue} :: {len(self.ma.waitQueue)} jobs"
        )

        header_panel = Panel(
            Align.center(
                Group("\n", Align.center(header_message)),
                vertical="top",
            ),
            box=box.ROUNDED,
            title="[b red]Machine Problem 3 - Memory Management",
            border_style=f"{self.colors['purple']}",
        )
        return header_panel  

    def generateAppDisplay(self):
        local = generateLayout()
        local["header"].update(self.generateStatsLayout())
        local["Memory"].update(self.generateMemoryLayout())
        local["Jobs"].update(self.generateJobLayout()) 
        return local

    def generateAnalysis(self) -> Panel:
        analysis_data = Table.grid(padding=1)
        analysis_data.add_column(style=f"{self.colors['amber']}", justify="center")
        analysis_data.add_column(no_wrap=True)

        analysis_data.add_row(
            "Total Average Fragmentation (Across all Blocks):",
            f"[b #ff7270] [ {(self.get_total_average_fragmentation())*100:.2f}% ]"
        )

        analysis_data.add_row(
            "Total Average Memory Utilization (Across all Blocks):",
            f"[b {self.colors['teal']}] {self.get_total_average_utilization() * 100:.2f}"
        )

        analysis_data.add_row(  # NOT DONE
            "Total Throughput:",
            f"[b {self.colors['teal']}] {self.get_average_throughput():.2f} jobs/second"
        )

        analysis_data.add_row(  # NOT DONE
            "Average Waiting Time:",
            f"[b {self.colors['amber']}] {self.ma.get_average_wait()}s"
        )

        analysis_data.add_row(  # NOT DONE
            "Max Wait Queue Length:",
            f"[b {self.colors['green']}] {max(self.total_wait_list)}"
        ) 

        analysis_data.add_row(
            "Fat Jobs:",
            f"[b {self.colors['red']}] {self.ma.fat_jobs()}"
        )

        analysis_panel = Panel(
            Align.center(
                Group("\n", Align.center(analysis_data)),
                vertical="top",
            ),
            box=box.ROUNDED,
            title="[b red]Machine Problem 3 - Analysis Panel",
            border_style=f"{self.colors['purple']}",
        )
        return analysis_panel


    def liveLoop(self, method, e_time):
        if method == "WF":
            self.ma.blocks = self.ma.generate_sorted_blocks(reverse=True)
        elif method == "BF":
            self.ma.blocks = self.ma.generate_sorted_blocks()

        self.ma.allocateJobs()
        

        with Live(self.generateAppDisplay(), refresh_per_second=4, screen=False) as live:
            while True:
                self.ma.firstFit()
                live.update(self.generateAppDisplay())
                self.execution_time += 1
                time.sleep(e_time)

                self.total_frag_list.append(self.ma.total_avg_frag_helper())
                if (self.ma.get_utilization() * 100) > 0:
                    self.total_util_list.append(self.ma.get_utilization())
                self.total_wait_list.append(len(self.ma.waitQueue))

                if self.ma.get_total_time() < 0 :
                    break

                if self.ma.get_done() == (len(self.ma.jobs) - self.ma.fat_jobs()):
                    break

        console = Console()
        console.print(self.generateAnalysis(), justify="center")




def main():
    app = Interface()
    tc = Console()

    memfile_name = ""
    jobfile_name = ""
    method = ""
    e_time = 1


    if len(sys.argv) == 3:

        if os.path.isfile(sys.argv[1]) and os.path.isfile(sys.argv[2]):
            memfile_name = sys.argv[1]
            jobfile_name = sys.argv[2]
            app.read_file(memfile_name, jobfile_name)

        else:
            tc.print(app.error_message(f"files not found, {sys.argv[1]} or {sys.argv[2]} does not exist!")) 
            return   

    elif len(sys.argv) == 4:
        if sys.argv[3] in ["BF, FF, WF"]:
            method = sys.argv[3]
        else:
            tc.print(app.error_message(f"method={sys.argv[3]} is not supported! Please choose from [BF, WF, FF]"))

    elif len(sys.argv) == 5:
        
        if int(sys.argv[4]) < 0 or int(sys.argv[4]) > 3:
            tc.print(app.error_message(f"e_time={sys.argv[4]} is not supported! please enter within [0, 3] only!")) 

        else:
            e_time = int(sys.argv[3])

    else:
        # PROMPT FOR FILENAME
        fTxt = Text()
        fTxt.append("Please enter path to")
        fTxt.append(" memory list file ", style=f"bold {app.colors['red']}")
        fTxt.append("- default=")
        while True:
            fname = Prompt.ask(fTxt, default="./mem_list1.txt") 
            if os.path.isfile(fname):
                memfile_name = fname
                break
            tc.print(app.error_message(f"file not found, {fname} does not exist!")) 

        jTxt = Text()
        jTxt.append("Please enter path to")
        jTxt.append(" job list file ", style=f"bold {app.colors['blue']}")
        jTxt.append("- default=")
        while True:
            fname = Prompt.ask(jTxt, default="./job_list1.txt") 
            if os.path.isfile(fname):
                jobfile_name = fname
                break
            tc.print(app.error_message(f"file not found, {fname} does not exist!"))       

        mTxt = Text()
        mTxt.append("Please select")
        mTxt.append(" allocation method ", style=f"bold {app.colors['green']}")
        method = Prompt.ask(mTxt, choices=["FF", "BF", "WF"])

        tTxt = Text()
        tTxt.append("Please enter ")
        tTxt.append(" execution e_time ", style="bold #dd8ef5")
        tTxt.append("(enter a number between 0 and 3) - default")
        while True:
            e_time = IntPrompt.ask(tTxt, default=1)
            if 0 <= e_time <= 3 and isinstance(e_time, int):
                break
            tc.print(app.error_message(f"e_time={e_time} is not supported! please enter within [0, 3] only!"))

    dp = Text(justify="center")
    dp.append("Memory List Filename: ")
    dp.append(f"{memfile_name}", style=f"bold {app.colors['red']}")
    dp.append("\n\n")
    dp.append("Joblist Filename: ")
    dp.append(f"{jobfile_name}", style=f"bold {app.colors['blue']}")
    dp.append("\n\n")
    dp.append("Method: ")
    dp.append(f"{method}", style=f"bold {app.colors['green']}")
    dp.append("\n\nExecution Time: ")
    dp.append(f"{e_time}")

    dpan = Panel.fit(dp)
    dpan.border_style=('#66ed73')

    tc.print(dpan, justify="center")
    if Confirm.ask("\n\n[b]Proceed with these settings?[/b]", default=True):
        # READ FROM FILE
        app.read_file(memfile_name, jobfile_name)
        # SELECT METHOD WITH EXECUTION TIME
        app.liveLoop(method, e_time)
        # INITITATE LIVE LOOP
        pass

    else:
        eTxt = Text(justify="center")
        eTxt.append("execution halted : user input [n]")
        eP = Panel.fit(eTxt)
        eP.border_style = ('#bf2e35')
        tc.print(eP, justify="center")

if __name__ == "__main__":
    main()
