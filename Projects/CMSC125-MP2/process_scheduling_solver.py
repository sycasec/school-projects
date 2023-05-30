from Logic import ProcessControlBoard
from rich.text import Text
from rich.panel import Panel 
from rich.layout import Layout 
from rich.table import Table
from rich.console import Console, Group
from rich.align import Align
from rich.columns import Columns
from rich.prompt import IntPrompt, Prompt, Confirm 
from rich import box
from rich import print as rp
from rich.live import Live

from copy import deepcopy
import sys
import os




def generateLayout() -> Layout:
    """define display layout""" 
    layout = Layout(name = "root")

    layout.split_row(
        Layout(name="process_dict", size=35),
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
        self.g_sym = {
            'top_op': "╭",
            'mid_op': "│",
            'bot_op': "╰",
            'tb_mid': "────",
            'md_mid': self.wrap_num,
            'tp_btw': "┬",
            'bt_btw': "┴",
            'tp_cls': "╮",
            'md_cls': "│",
            'bt_cls': "╯",
        }

    def read_file(self, filename):
        self.file = filename
        self.pcb.read_from_csv(filename)

    def wrap_num(self, num) -> str:
        return f" {num:02d} "

    def generateProcessPanel(self, avg_turn, avg_wait) -> Panel:
        # p_table = Table()
        # p_table.add_column("P#", justify="center")
        # p_table.add_column("A", justify="center")
        # p_table.add_column("BT", justify="center")
        # p_table.add_column("PRI", justify="center")
        #
        # for row in self.pcb.get_process_dict_as_list():
        #     p_table.add_row(
        #         f"{row[0]},",
        #         f"{row[1]},",
        #         f"{row[2]},",
        #         f"{row[3]}",
        #     )
        # p_table.box = box.SIMPLE_HEAD

        sPmsg = Table.grid(padding=1)
        sPmsg.add_column(style="#a6e22e", justify="center")
        sPmsg.add_column(no_wrap=True)
        sPmsg.add_row(
            "Avg Turnaround Time:",
            f"[b #ff7270] {avg_turn}"
        )
        sPmsg.add_row(
            "Avg Waiting Time:",
            f"[b #ff9999] {avg_wait}"
        )

        sPmsg.border_style=("#ff7270")
        
        p_Panel = Panel(
            Align.center(sPmsg),
            box=box.ROUNDED,
            padding=[3,0,0,0],
            border_style="#f82558",
        )
  
        return p_Panel
    
    
    def generateGanttPanel(self, g_list, t_list) -> Panel:
         
        tc = Console()
        # print("╭────┬┬────┬┬────╮")
        # print("│ 01 ││ 10 ││ 69 │")
        # print("╰────┴┴────┴┴────╯")
        # print("00   05    16   24")
        gText = Text(justify = "center")
        gText.append(self.g_sym['top_op'])
        gText.append(f"{(self.g_sym['tb_mid'] + (self.g_sym['tp_btw']*2)) * (len(g_list) - 1)}")
        gText.append(f"{(self.g_sym['tb_mid'] + self.g_sym['tp_cls'])}\n")

        for n in g_list:
            gText.append(f"{self.g_sym['mid_op']}")
            gText.append(f"{self.g_sym['md_mid'](n)}", style="bold #a6e22e")
            gText.append(f"{self.g_sym['mid_op']}")
        gText.append('\n')

        gText.append(self.g_sym['bot_op'])
        gText.append(f"{(self.g_sym['tb_mid'] + (self.g_sym['bt_btw']*2)) * (len(g_list) - 1)}")
        gText.append(f"{(self.g_sym['tb_mid'] + self.g_sym['bt_cls'])}") 
        gText.append('\n')
        gText.append(f"{t_list[0]:02d}   {t_list[1]:02d}")
        for i in range(2,len(t_list)-1):
            gText.append(f"{' '*3 if t_list[i-1] > 99 else ' '*4}{t_list[i]:02d}")
        gText.append(f"{' '*3 if t_list[-2] < 100 else ' ' * 2}{t_list[-1]:02d}")

        gantt_p = Panel(
            Align.center(gText),
            box=box.ROUNDED,
            padding=[10,10,10,10],
            border_style = "#66d9ef"
        )

        return gantt_p
    
    def generateRRGantt(self, g_list, t_list) -> Panel:
        tc = Console()
        gText = Text(justify = "center")
        gl = len(g_list)
        tl = len(t_list)
        g_index = 0 
        t_index = 0
        # pass
        while gl > 30:
            gText.append(self.g_sym['top_op'])
            gText.append(f"{(self.g_sym['tb_mid'] + (self.g_sym['tp_btw']*2)) * (29)}")
            gText.append(f"{(self.g_sym['tb_mid'] + self.g_sym['tp_cls'])}\n")
            
            for i in range(30):
                gText.append(f"{self.g_sym['mid_op']}")
                gText.append(f"{self.g_sym['md_mid'](g_list[g_index])}", style="bold #a6e22e")
                gText.append(f"{self.g_sym['mid_op']}")
                g_index += 1
            gText.append('\n')
            
            gText.append(self.g_sym['bot_op'])
            gText.append(f"{(self.g_sym['tb_mid'] + (self.g_sym['bt_btw']*2)) * 29}")
            gText.append(f"{(self.g_sym['tb_mid'] + self.g_sym['bt_cls'])}") 
            gText.append('\n')

            gText.append(f"{t_list[t_index]:02d}   {t_list[t_index+1]:02d}")
            for i in range(t_index + 2, t_index + 30):
                gText.append(f"{' '*3 if t_list[i-1]>99 else ' '*4}{t_list[i]:02d}")
            gText.append(f"{' '*3 if t_list[t_index+29] < 100 else ' ' * 2}{t_list[t_index+30]:02d}")
            gText.append('\n\n')
            t_index += 30 

            tl -= 30
            gl -= 30
            # break
        
        if gl > 0:
            gText.append(self.g_sym['top_op'])
            gText.append(f"{(self.g_sym['tb_mid'] + (self.g_sym['tp_btw']*2)) * (gl-1)}")
            gText.append(f"{(self.g_sym['tb_mid'] + self.g_sym['tp_cls'])}\n")

            for i in range(gl):
                gText.append(f"{self.g_sym['mid_op']}")
                gText.append(f"{self.g_sym['md_mid'](g_list[g_index])}", style="bold #a6e22e")
                gText.append(f"{self.g_sym['mid_op']}")
                g_index += 1
            gText.append('\n') 

            gText.append(self.g_sym['bot_op'])
            gText.append(f"{(self.g_sym['tb_mid'] + (self.g_sym['bt_btw']*2)) * (gl-1)}")
            gText.append(f"{(self.g_sym['tb_mid'] + self.g_sym['bt_cls'])}") 
            gText.append('\n')

            if tl > 3:
                gText.append(f"{t_list[t_index]:02d}   {t_list[t_index+1]:02d}")
                # print(t_list[t_index+8])
                # print(f"deb::{tl + t_index}=tl({tl})+({t_index})::start={t_list[t_index]}::end={t_list[-1]},{t_list.index(t_list[-1])}")
                for i in range(t_index + 2, t_index + tl - 1):
                    # print(i)
                    gText.append(f"{' '*3 if t_list[i-1]>99 else ' '*4}{t_list[i]:02d}")
                gText.append(f"{' '*3 if t_list[t_index+tl-2] < 100 else ' ' * 2}{t_list[t_index+tl-1]:02d}")
            # else:



        gantt_p = Panel(
            Align.center(gText),
            box=box.ROUNDED,
            padding=[3,10,0,10],
            border_style = "#66d9ef"
        )

        return gantt_p
 




    def generateCalculationsPanel(self, method:str, completed:dict) -> Panel:
        c_table = Table(title=method)
        c_table.add_column("Process", justify="right")
        c_table.add_column("Arrival Time", justify="center")
        c_table.add_column("Burst Time", justify="center")
        c_table.add_column("Finish Time", justify="center")
        c_table.add_column("Turnaround Time", justify="center")
        c_table.add_column("Waiting Time", justify="center")
        for p in completed.keys():
            c_table.add_row(
                f"Process {p}",
                f"{self.pcb.pd_copy[p]['arrival']}",
                f"{self.pcb.pd_copy[p]['burst']}",
                f"{completed[p]['finished']}",
                f"{completed[p]['turnaround']}",
                f"{completed[p]['wait']}",
            )
        # c_table.box=box.SIMPLE_HEAD
        # c_table.columns.style="cyan"
        
        for i in c_table.columns:
            i.style="cyan"

        c_table.row_styles=["none", "dim"]

        c_panel = Panel(
            Align.center(c_table),
            box=box.ROUNDED,
            border_style = "#a6e22e"
        )  

        return c_panel

    def generateMainDisplay(self, method:str, quantum:int):
        lt = generateLayout()
        tc = Console()
        # >>>>>> TESTING <<<<<<
        # p1 = "Process_1 - process1.csv.csv"
        # tfile = "test.csv"
        # self.pcb.read_from_csv(tfile)
        # table, g_list, t_list = self.pcb.rr_solver(deepcopy(self.pcb.process_dict), quantum=4) 
        # tc.print(self.generateGanttPanel(g_list, t_list))

        # >>>> TESTING END <<<<
        match method:
            case "FCFS":
                table, g_list, t_list = self.pcb.fcfs_solver(deepcopy(self.pcb.process_dict))
                lt['gantt_display'].update(self.generateGanttPanel(g_list, t_list))
            case "SJF":
                table, g_list, t_list = self.pcb.sjf_solver(deepcopy(self.pcb.process_dict))
                lt['gantt_display'].update(self.generateGanttPanel(g_list, t_list))
            case "SRPT":
                table, g_list, t_list = self.pcb.srpt_solver(deepcopy(self.pcb.process_dict))
                lt['gantt_display'].update(self.generateGanttPanel(g_list, t_list))
            case "PRIO":
                table, g_list, t_list = self.pcb.prio_solver(deepcopy(self.pcb.process_dict))
                lt['gantt_display'].update(self.generateGanttPanel(g_list, t_list))
            case "RR":
                table, g_list, t_list = self.pcb.rr_solver(deepcopy(self.pcb.process_dict), quantum)
                lt['gantt_display'].update(self.generateRRGantt(g_list, t_list))

        avg_turn = sum([table[i]['turnaround'] for i in table.keys()])/len(table.keys())
        avg_wait = sum([table[i]['wait'] for i in table.keys()])/len(table.keys())

        # print(f"deb::avgturn={avg_turn}::avgwait={avg_wait}")

        lt['process_dict'].update(self.generateProcessPanel(avg_turn, avg_wait))
        lt['tables'].update(self.generateCalculationsPanel(f"{method}", table))
        tc.print(lt)

    def eval_control(self, file, method):
        fcopy = deepcopy(file)

        m_dict = {
            "FCFS": self.pcb.fcfs_solver,
            "SJF": self.pcb.sjf_solver,
            "SRPT": self.pcb.srpt_solver,
            "PRIO": self.pcb.prio_solver,
            "RR": self.pcb.rr_solver,
        }

        x, g, t = m_dict[method](fcopy)
        return x, g, t
 

    def evaluate(self):
        process_file_copy = deepcopy(self.pcb.process_dict)
        fcfs_dict, fcfs_g, fcfs_t = self.eval_control(process_file_copy, "FCFS") 
        sjf_dict, sjf_g, sjf_t = self.eval_control(process_file_copy, "SJF") 
        srpt_dict, srpt_g, srpt_t = self.eval_control(process_file_copy, "SRPT") 
        prio_dict, prio_g, prio_t = self.eval_control(process_file_copy, "PRIO") 
        rr_dict, rr_g, rr_t = self.eval_control(process_file_copy, "RR") 

        rTable = Table(title="Method Evaluation")
        rTable.add_column("Method", justify="right")
        rTable.add_column("Avg. Turnaround", justify="center")
        rTable.add_column("Avg. Wait", justify="center")
        rTable.add_row(
            "FCFS",
            f"{sum([fcfs_dict[i]['turnaround'] for i in fcfs_dict.keys()])/len(fcfs_dict.keys())}",
            f"{sum([fcfs_dict[i]['wait'] for i in fcfs_dict.keys()])/len(fcfs_dict.keys())}"
        )
        rTable.add_row(
            "SJF",
            f"{sum([sjf_dict[i]['turnaround'] for i in sjf_dict.keys()])/len(sjf_dict.keys())}",
            f"{sum([sjf_dict[i]['wait'] for i in sjf_dict.keys()])/len(sjf_dict.keys())}"
        )
        rTable.add_row(
            "SRPT",
            f"{sum([srpt_dict[i]['turnaround'] for i in srpt_dict.keys()])/len(srpt_dict.keys())}",
            f"{sum([srpt_dict[i]['wait'] for i in srpt_dict.keys()])/len(srpt_dict.keys())}"
        )
        rTable.add_row(
            "PRIO",
            f"{sum([prio_dict[i]['turnaround'] for i in prio_dict.keys()])/len(prio_dict.keys())}",
            f"{sum([prio_dict[i]['wait'] for i in prio_dict.keys()])/len(prio_dict.keys())}"
        )
        rTable.add_row(
            "RR",
            f"{sum([rr_dict[i]['turnaround'] for i in rr_dict.keys()])/len(rr_dict.keys())}",
            f"{sum([rr_dict[i]['wait'] for i in rr_dict.keys()])/len(rr_dict.keys())}"
        )
        rTable.columns[0].style="#be84ff"
        rTable.columns[1].style="#66d9ef"
        rTable.columns[2].style="#f82558"

        # ePanel = Panel(
        #     Align.center(rTable),
        #     box=box.ROUNDED,
        #     border_style = "#a6e22e"
        # )
        ePanel = Panel.fit(Align.center(rTable))
        ePanel.box=box.ROUNDED
        ePanel.border_style=("#a6e22e")

        return ePanel


    
    # def main(self):
    #     with Live(self.generateMainDisplay(), refresh_per_second=4, screen=False) as live:
    #         while True:
    #             live.update(self.generateMainDisplay())
    #             break


def eval(filename:str):
    app = Interface()
    console = Console()
    
    app.read_file(filename)
    console.print(app.evaluate(), justify="center")



def main():
    app = Interface()
    mc = Console()

    def genErr(errmsg):
        eTxt = Text()
        eTxt.append(f"ERROR! -> {errmsg}", style="bold #bf2e35")
        return eTxt

    if len(sys.argv) > 1:
        if os.path.isfile(sys.argv[1]):
            fname = sys.argv[1]
            app.read_file(sys.argv[1])
        elif sys.argv[1] == "--eval":
            eval(sys.argv[2])
            return
        else:
            mc.print(genErr(f"file not found, {sys.argv[1]} does not exist!")) 
            return   

    else:
        # PROMPT FOR FILENAME
        fTxt = Text()
        fTxt.append("Please enter path to")
        fTxt.append(" filename ", style="bold #dd8ef5")
        fTxt.append("- default=")
        while True:
            fname = Prompt.ask(fTxt, default="./Process_1.csv") 
            if os.path.isfile(fname):
                app.read_file(fname)
                break
            mc.print(genErr(f"file not found, {fname} does not exist!")) 
        
    mTxt = Text()
    mTxt.append("Please select")
    mTxt.append(" scheduling method ", style="bold #812ff5")
    method = Prompt.ask(mTxt, choices=["FCFS", "SJF", "SRPT", "PRIO", "RR"])
    quantum = 0

    if method == "RR":
        rrTxt = Text()
        rrTxt.append("Please enter quantum, default=")
        while True:
            quantum = IntPrompt.ask(rrTxt, default=4)
            if quantum > 1:
                break
            mc.print(genErr("please enter a positive quantum."))

    dp = Text(justify="center")
    dp.append("Filename: ")
    dp.append(f"{fname}", style="bold #a6e22e")
    dp.append("\n\n")
    dp.append("Method: ")
    dp.append(f"{method}", style="bold #66d9ef")
    dp.append("\n\nQuantum: ")
    dp.append(f"{quantum}")

    dpan = Panel.fit(dp)
    dpan.border_style=('#66ed73')

    mc.print(dpan, justify="center")
    if Confirm.ask("\n\n[b]Proceed with these settings?[/b]", default=True):
        app.generateMainDisplay(method, quantum)
    else:
        eTxt = Text(justify="center")
        eTxt.append("execution halted : user input [n]")
        eP = Panel.fit(eTxt)
        eP.border_style = ('#bf2e35')
        mc.print(eP, justify="center") 

#a6e22e
#66d9ef
#be84ff
#f82558

if __name__ == "__main__":
    main()
