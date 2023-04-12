import random
import time
from rich import box
from rich.prompt import IntPrompt, Confirm, InvalidResponse
from rich.panel import Panel
from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich.text import Text


class Resource:
    def __init__(self, res_number:int):
        self.queue = [] 
        self.current_user = None
        self.name = f"Resource {res_number:02d}"
        self.use_time = None
        self.number = res_number
        self.is_available = True
        
    def deactivateResource(self):
        self.current_user = None
        self.use_time = None
        self.is_available = True
        
    def startJob(self):
        userChanged = False
        for user in self.queue:
            if not user.working:
                self.current_user = user
                userChanged = True
                break

        if userChanged and self.current_user:
            self.current_user.toggleWorking()
            # print(f"DBG::TW-SJ")
            self.queue.pop(self.queue.index(self.current_user))
            # print(f"DBG::{self.queue}::{self.current_user}")
            self.is_available = False
            self.use_time = self.current_user.resource_requests[self]
        else:
            self.deactivateResource()
        # if not self.current_user.working:
        #     self.current_user.toggleWorking()

    def appendPriorityQueue(self, user_request):
        self.queue.append(user_request)

    def getPriorityQ(self):
        return self.queue



class User:
    # resource_list is a list of tuples
    # [(resource_actual, use_time), ... (resource_actual, use_time)]
    def __init__(self, user_number: int, resource_list_copy: list[Resource], max_res:int, max_tim:int):
        self.number = user_number
        self.name = f"User {user_number:02d}"
        self.resource_requests:dict = {}  # [resource_number, use_time]
        self.working = False
        self.generateRequests(resource_list_copy, max_res, max_tim)

    def generateRequests(self, resource_list: list[Resource], max_res:int, max_tim:int): 
        max_requests = random.randint(1, max_res)
        user_request_temp = {}

        resources_reqs = random.choices(resource_list, k=max_requests)
        for key in resources_reqs:
            user_request_temp[key] = random.randint(1, max_tim)
        
        self.resource_requests = user_request_temp

    def isAllDone(self, resource_list: list[Resource]):
        for res in resource_list:
            if self in res.queue:
                return False
        if self.working:
            return False
        return True

    def toggleWorking(self):
        if self.working:
            self.working = False
        else:
            self.working = True

    def getUserRequests(self) -> dict:
        return self.resource_requests 



class Controller:
    def __init__(self, max_res:int, max_usr:int, max_tim:int):
        self.n_users = random.randint(1, max_usr)
        self.n_res = random.randint(1, max_res)
        self.user_list = []
        self.res_list = []

        for rn in range(1,self.n_res+1):
            self.res_list.append(Resource(rn))

        for un in range(1,self.n_users+1):
            self.user_list.append(User(un, self.res_list.copy(), max_res, max_tim))
                    

    def appendResourceQueue(self, user: User):
        for res in self.res_list:
            if res in user.resource_requests:
                res.queue.append(user)

    def allResourceEmpty(self):
        for res in self.res_list:
            if not res.is_available or len(res.queue) > 0:
                return False
        return True

    def initSystem(self):
        for user in self.user_list:
            for res in self.res_list:
                if res in user.resource_requests:
                    res.queue.append(user)

        for res in self.res_list:
            res.startJob()


    def systemLoop(self, prog_secs: int):
        """
        main system loop
        """

        self.initSystem()
        self.activateUnusedResources()
        loopConsole = Console()
        
        
        # resTable.border_style=('#b0a4ff')

        statusText = Text(justify="center")
        statusText.append("Lab Exercise 1")
        statusText.append("\n\nTotal Resources: ", style="bold")
        statusText.append(f"{self.n_res}", style="bold #00ff00")
        statusText.append("\n\nTotal Users: ", style="bold")
        statusText.append(f"{self.n_users}", style="bold #ff8000")
        mainPanel = Panel(statusText)

        
        c = 0 
        while True:
            loopConsole.clear() 
            #self.activateUnusedResources() 
            
            # A LOT OF SHIT
            resTable = Table(title="Resources Table")
            resTable.add_column("Resources", justify="left", style="cyan")
            resTable.add_column("Current User", justify="center", style="")
            resTable.add_column("Time Left", justify="center")
            resTable.add_column("Queue", justify="center")
            resTable.add_column("Next User", justify="left")

            for res in self.res_list:
                resTable.add_row(
                    f"{res.name}",
                    f"{res.current_user.name if res.current_user else 'IDLE'}",
                    self.getResourceTime(res),
                    f"{[u.number for u in res.queue]}",
                    f"{res.queue[0].name if len(res.queue) > 0 else 'FREE'}"
                )

            usrTable = Table(title="Users") 
            usrTable.title_style=("bold #ff9670")
            usrTable.add_column("User #", justify="center", no_wrap=True)
            usrTable.add_column("Status", justify="center", no_wrap=True)
            usrTable.add_column("Requests", justify="center")

            for u in self.user_list:
                usrTable.add_row(
                    f"{u.name}",
                    f"{self.checkUserStatus(u)}",
                    f"{[k.number for k in u.resource_requests.keys()]}"
                )

            usrTable.box = box.SIMPLE_HEAD
            usrTable.border_style=("#ff7270")
            resTable.title_style=("bold")
            usrpanel = Panel.fit(usrTable)
            usrpanel.border_style=("#ff70b3")
            
            centeredRt = Align.center(resTable)
            resPanel = Panel.fit(centeredRt)
            resPanel.border_style=('#a4e7ff')
            
            # A LOT OF SHIT ENDS

            loopConsole.print(mainPanel, justify="center")
            loopConsole.print(resPanel, justify="center")
            loopConsole.print(usrpanel, justify="center")
                
            time.sleep(prog_secs)
            self.updateTime()
            if c == 1:
                break
            if self.allResourceEmpty():
                c += 1
    

    def updateTime(self):
        for res in self.res_list:
            if res.current_user:
                res.use_time -= 1
                if res.use_time == 0:
                    res.current_user.toggleWorking()
                    # print(f"DBG::UPDATE_TIME-TW()")
                    if len(res.queue) > 0:
                        res.startJob()
                    else:
                        res.deactivateResource()
            if res.is_available and len(res.queue) > 0:
                res.startJob()



    def checkUserStatus(self, user: User):
        if user.isAllDone(self.res_list):
            return "All Done!"
        elif user.working:
            return "Working"
        elif not user.working:
            return "Waiting"

    def getResourceTime(self, res):
        if not res.use_time:
            return 'IDLE'
        else:
            return f"{res.use_time}s"

    
    def debugDisplay(self):
        table = Table(title="DEBUG")
        table.add_column("")
    
    def findLongestUsetime(self, resource: Resource):
        if len(resource.queue) > 0:
             return max(resource.queue, key=lambda user: user.resource_requests[resource])
        return None

    def findMaxResQueue(self) -> Resource:
        resource_has_max_pq = max(self.res_list, key=lambda r: len(r.queue))
        return resource_has_max_pq

    def findEarliestQueue(self, usr: User):
        q_idx = {}
        for res in self.res_list:
            print(f"DBG::{q_idx}::{usr}::{[u.name for u in res.queue]}")
            if usr in res.queue:
                q_idx[res] = res.queue.index(usr)
        if q_idx:
            return min(q_idx, key=q_idx.get)
        return None


    def areUsersBusy(self):
        stats = [u.working for u in self.user_list]
        if False in stats:
            return False
        return True


    # THIS THING IS SO BUGGY I MIGHT AS WELL NOT.
    def activateUnusedResources(self): 
        # print(f"DBG::ENTERED_FUNCTION")
        unused_res = []
        for res in self.res_list:
            if not res.current_user:
                unused_res.append(res)

        
        # print(f"DBG::UNUSED_RES::{[r.number for r in unused_res]}")
        if self.allResourceEmpty():
            return
        # if len(unused_res) > 0:
        #     for r in unused_res:
        while len(unused_res) > 0:
            r = unused_res.pop(0)
            # print(f"DBG::CURR_R={r.name}::URLEN={len(unused_res)}")
            if self.areUsersBusy(): break
            for usr in self.user_list:
                # print(f"DBG::USR#={usr.name}::STAT={usr.working}")
                if not usr.working:
                    # find res where usr is in min queue and remove
                    res_ref = self.findEarliestQueue(usr)
                    if res_ref:
                        res_ref.queue.remove(usr)

                        # remove user's request for original resource
                        # add new request for unused resource
                        time = usr.resource_requests[res_ref]
                        usr.resource_requests[r] = time
                        del usr.resource_requests[res_ref]
                        r.queue.insert(0, usr)
                        r.startJob()
                        break
                    else:
                        return
                
     

    def forceUsers(self, amt_users:int):
        self.n_users = amt_users

    def forceResources(self, amt_res:int):
        self.n_res = amt_res


    def getResourceStat(self, resource_number:int) -> bool:
        return self.res_list[resource_number - 1].is_available

if __name__ == "__main__":
    tempConsole = Console()
    tempConsole.clear()
    pTxt = Text()
    uTxt = Text()
    tTxt = Text()
    pTxt.append("Maximum amount of ")
    pTxt.append(" resources ", style="bold #03DAC5")
    pTxt.append("(enter a number between [b]1[/b] and [b]30[/b]) - default")

    uTxt.append("Maximum amount of ")
    uTxt.append(" users ", style="bold #dd8ef5")
    uTxt.append("(enter a number between [b]1[/b] and [b]30[/b]) - default")

    tTxt.append("Maximum amount of")
    tTxt.append(" time ", style="bold #812ff5")
    tTxt.append("(enter a number between [b]1[/b] and [b]30[/b]) - default")

    while True:
        c_resn = IntPrompt.ask(pTxt, default=30)
        if 1 <= c_resn <= 30:
            break
        InvalidResponse(f"You entered: {c_resn} - please choose between 1-30")

    while True:
        c_usrn = IntPrompt.ask(uTxt, default=30)
        if 1 <= c_usrn <= 30:
            break    
        InvalidResponse(f"You entered: {u_resn} - please choose between 1-30")

    while True:
        c_time = IntPrompt.ask(tTxt, default=30)
        if 1 <= c_time <= 30:
            break
        InvalidResponse(f"You entered: {c_time} - please choose between 1-30")

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
        command.systemLoop(1)
    else:
        eTxt = Text(justify="center")
        eTxt.append("execution halted : user input [n]")
        eP = Panel.fit(eTxt)
        eP.border_style = ('#bf2e35')
        console.print(Panel.fit(eTxt), justify="center")
