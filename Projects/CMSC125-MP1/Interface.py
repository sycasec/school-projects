import time
import os
from Logic import Controller
from rich import box
from rich.live import Live
from rich.text import Text
from rich.panel import Panel 
from rich.layout import Layout 
from rich.table import Table
from rich.console import Console, Group
from rich.align import Align
from rich.columns import Columns
from rich.prompt import IntPrompt, Confirm, InvalidResponse

def presimLoop(ctrl: Controller) -> list[int]:
    """presimulate loop without changing initial conditions"""
    ctrl.initSystem() 
    # ctrl.activateUnusedResources()
    final_loop = False
    timer = 0
    debugConsole = Console()
    local = generateLayout() 
    
    while True:
        timer += 1
        # local["header"].update(generateHeader([ctrl.max_res, ctrl.max_usr, ctrl.max_tim, 69]))
        # local["Resource"].update(generateResourceDisplay(ctrl))
        # local["Users"].update(generateUserDisplay(ctrl))
        # debugConsole.print(local)

        ctrl.updateTime()
        # ctrl.activateUnusedResources()
        if final_loop:
            break       
        if ctrl.allResourceEmpty():
            final_loop = True

    for user in ctrl.user_list:
        user.rearmRequests()

    return [ctrl.max_res, ctrl.max_usr, ctrl.max_tim, timer]


def generateLayout() -> Layout:
    """define display layout""" 
    layout = Layout(name = "root")

    layout.split(
        Layout(name="header", size=13),
        Layout(name="main", ratio=2),
    )

    layout["main"].split_row(
        Layout(name="Resource"),
        Layout(name="Users"),
    )

    return layout

#dd8ef5
#ff7270

def generateHeader(maxDeets: list[int]) -> Panel:
    header_message = Table.grid(padding=1)
    header_message.add_column(style="#dd8ef5", justify="center")
    header_message.add_column(no_wrap=True)
    header_message.add_row(
        "Maximum Resource Count:",
        f"[b #ff7270] [ {maxDeets[0]} ]"
    )
    header_message.add_row(
        "Maximum User Count:",
        f"[b #ff7270] [ {maxDeets[1]} ]"
    )
    header_message.add_row(
        "Maximum Time:",
        f"[b #ff7270] [ {maxDeets[2]} ]"
    )
    header_message.add_row(
        "Remaining Time:",
        f"[b #ff7270] [ {maxDeets[3]}s ]" 
    )

    header_panel = Panel(
        Align.center(
            Group("\n", Align.center(header_message)),
            vertical="top",
        ),
        box=box.ROUNDED,
        title="[b red]Laboratory Exercise 1 - Multiprogramming with Time-Sharing",
        border_style="bright_blue",
    )
    return header_panel

# NOTE: SPLIT RES AND COL INTO TWO TO GET THAT JUICY SPLIT

def generateResourceDisplay(ctrl: Controller) -> Panel:
    # ctrl.initSystem() must be called before this is updated!
    
    resTable = Table(title="Resources")
    resTable.add_column("Resources", justify="left", style="cyan")
    resTable.add_column("Serving", justify="center", style="")
    resTable.add_column("Time", justify="center")
    resTable.add_column("Queue", justify="center")
    resTable.add_column("Next", justify="left")

    for res in ctrl.res_list:
        resTable.add_row(
            f"{res.name}",
            f"{res.current_user.name if res.current_user else 'IDLE'}",
            ctrl.getResourceTime(res),
            ctrl.prettyPrint(res.queue),
            f"{res.queue[0].name if len(res.queue) > 0 else 'FREE'}"
        )
    resTable.title_style=("bold #dd8ef5")
    resTable.box = box.SIMPLE_HEAD 
    
    resPanel = Panel(
        Align.center(resTable),
        box=box.ROUNDED,
        border_style="green",
    )

    return resPanel

# INT OR NONE
def ETAhelper(eta:list) -> str:
    if not eta[1]:
        return "BUSY"
    return f"{eta[0]}s" 

def generateUserDisplay(ctrl: Controller) -> Panel:
    usrTable = Table(title="Users")
    usrTable.title_style=("bold #ff9670")
    usrTable.add_column("Users", justify="center")
    usrTable.add_column("Status", justify="center")
    usrTable.add_column("Resource Requests", justify="center")
    usrTable.add_column("Wait Time", justify="center")

    for u in ctrl.user_list:
        usrTable.add_row(
            f"{u.name}",
            f"{ctrl.checkUserStatus(u)}",
            ctrl.prettyPrint([k.number for k in u.resource_requests.keys()], False),
            f"{ETAhelper(ctrl.getUserWaitingETA(u))}",
        )

    usrTable.box = box.SIMPLE_HEAD
    usrTable.border_style=("#ff7270")
    
    usrPanel = Panel(
        Align.center(usrTable),
        box=box.ROUNDED,
        border_style="red",
    )

    return usrPanel 

def generateMainDisplay(ctrl: Controller, maxDeets: list[int]):      
    local = generateLayout() 
    local["header"].update(generateHeader(maxDeets))
    local["Resource"].update(generateResourceDisplay(ctrl))
    local["Users"].update(generateUserDisplay(ctrl))
    return local 
    

def liveLoop(ctrl: Controller):
    deets = presimLoop(ctrl)
    layout = generateLayout()
    ctrl.initSystem()
    # ctrl.activateUnusedResources()
    extra_loop = False
    with Live(generateMainDisplay(ctrl, deets), refresh_per_second=4, screen=False) as live:
        while True:
            live.update(generateMainDisplay(ctrl, deets))
            time.sleep(1)
            deets[3] -= 1
            ctrl.updateTime()
            # ctrl.activateUnusedResources()
            if extra_loop:
                break
            if ctrl.allResourceEmpty():
                extra_loop = True

# ctrl = Controller(10,10,10)
# liveLoop(ctrl)
#
# main = ()
# t = Console()
# t.print(generateHeader([30,30,30,69]))
#

def main():
    tempConsole = Console()
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    pTxt = Text()
    uTxt = Text()
    tTxt = Text()
    pTxt.append("Maximum amount of ")
    pTxt.append(" resources ", style="bold #03DAC5")
    pTxt.append("(enter a number between 1 and 30) - default")

    uTxt.append("Maximum amount of ")
    uTxt.append(" users ", style="bold #dd8ef5")
    uTxt.append("(enter a number between 1 and 30) - default")

    tTxt.append("Maximum amount of")
    tTxt.append(" time ", style="bold #812ff5")
    tTxt.append("(enter a number between 1 and 30) - default")

    def genErr(errmsg):
        eTxt = Text()
        eTxt.append(f"ERROR! value entered is out of bounds -> {errmsg}", style="bold #bf2e35")
        return eTxt

    while True:
        c_resn = IntPrompt.ask(pTxt, default=30)
        if 1 <= c_resn <= 30:
            break
        tempConsole.print(genErr(c_resn))

    while True:
        c_usrn = IntPrompt.ask(uTxt, default=30)
        if 1 <= c_usrn <= 30:
            break    
        tempConsole.print(genErr(c_usrn))

    while True:
        c_time = IntPrompt.ask(tTxt, default=30)
        if 1 <= c_time <= 30:
            break
        tempConsole.print(genErr(c_time))

    dTxt = Text(justify="center")
    dTxt.append("Total Resources: ")
    dTxt.append(f"{c_resn}\n\n", style="bold #03DAC5")
    dTxt.append("Total Users: ")
    dTxt.append(f"{c_usrn}\n\n", style="bold #dd8ef5")
    dTxt.append("Total Time: ")
    dTxt.append(f"{c_time}", style="bold #812ff5")
    dp = Panel.fit(dTxt)
    dp.border_style=('#66ed73')

    tempConsole.print(dp, justify="center")
    if Confirm.ask("\n\n[b]Proceed with these settings?[/b]", default=True):
        command = Controller(c_resn, c_usrn, c_time)
        liveLoop(command)
    else:
        eTxt = Text(justify="center")
        eTxt.append("execution halted : user input [n]")
        eP = Panel.fit(eTxt)
        eP.border_style = ('#bf2e35')
        tempConsole.print(eP, justify="center")

if __name__ == "__main__":
    main()
