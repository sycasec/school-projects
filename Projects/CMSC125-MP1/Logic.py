import random
import time

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
                if self.current_user:
                    del self.current_user.resource_requests[self]
                self.current_user = user
                userChanged = True
                break

        if userChanged and self.current_user:
            self.current_user.toggleWorking()
            self.queue.pop(self.queue.index(self.current_user))
            self.is_available = False
            # print(f"DBG::{self.current_user.name}::{self.current_user.resource_requests}")
            self.use_time = self.current_user.resource_requests[self]
        else:
            self.deactivateResource()

    def appendPriorityQueue(self, user_request):
        self.queue.append(user_request)

    def getPriorityQ(self):
        return self.queue



class User:
    def __init__(self, user_number: int, resource_list_copy: list[Resource], max_res:int, max_tim:int):
        self.number = user_number
        self.name = f"User {user_number:02d}"
        self.resource_requests:dict = {}  
        self.requests_backup = {}
        self.working = False
        self.generateRequests(resource_list_copy, max_res, max_tim)

    def generateRequests(self, resource_list: list[Resource], max_res:int, max_tim:int): 
        max_requests = random.randint(1, max_res)
        user_request_temp = {}

        resources_reqs = random.choices(resource_list, k=max_requests)
        for key in resources_reqs:
            user_request_temp[key] = random.randint(1, max_tim)
        
        self.resource_requests = user_request_temp
        self.requests_backup = user_request_temp.copy()

    def rearmRequests(self):
        self.resource_requests = self.requests_backup

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
        self.max_res = max_res
        self.max_usr = max_usr
        self.max_tim = max_tim
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

    def prettyPrint(self, queue: list, iR=True):
        if len(queue) > 3:
            return f"{'User' if iR else 'Res':}: {queue[0].number if iR else queue[0]}, {queue[1].number if iR else queue[1]}, {queue[2].number if iR else queue[2]}..."
        elif len(queue) == 0:
            return "FREE"
        else:
            return f"{'User' if iR else 'Res'}: {', '.join(str(i.number) for i in queue) if iR else ', '.join(str(i) for i in queue)}"

 
    def updateTime(self):
        for res in self.res_list:
            if res.use_time == 0:
                res.current_user.toggleWorking()
                # print(f"DBG::UPDATE_TIME-TW()")
                if len(res.queue) > 0:
                    res.startJob()
                else:
                    res.deactivateResource()
            if res.current_user:
                res.use_time -= 1
            
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
            # print(f"DBG::{q_idx}::{usr}::{[u.name for u in res.queue]}")
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

    # for some reason this works now
    def activateUnusedResources(self): 
        # loop through all unused resources 
        # by checking if they have no current user
        unused_res = []
        for res in self.res_list:
            if not res.current_user:
                unused_res.append(res)

        
        if self.allResourceEmpty():
            return
        while len(unused_res) > 0:
            r = unused_res.pop(0)
            if self.areUsersBusy(): break
            for usr in self.user_list:
                if not usr.working:
                    # find the resource which has the shortest wait time for USR
                    res_ref = self.findEarliestQueue(usr)
                    if res_ref:
                        res_ref.queue.remove(usr)

                        # remove user's request for original resource
                        # add new request for unused resource
                        time = usr.resource_requests[res_ref]
                        del usr.resource_requests[res_ref]
                        usr.resource_requests[r] = time
                        r.queue.insert(0, usr)
                        r.startJob()
                        break
                    else:
                        return
                
    
    # USER GETTING ETA IS NOT WORKING
    def getUserWaitingETA(self, user: User):
        min_wait_time = 0
        min_wait_Res = None
        
        if not user.working:
            for res in self.res_list:
                total_wait_time = 0
                
                if user not in res.queue:
                    continue

                if res.current_user and res.use_time:
                    total_wait_time += res.use_time

                for usr in res.queue:
                    if usr is not user:
                        total_wait_time += usr.resource_requests[res]
                    elif usr is user:
                        break
                
                if min_wait_time == 0 or (min_wait_time > 0 and total_wait_time < min_wait_time):
                    min_wait_time = total_wait_time
                    min_wait_Res = res

        return [min_wait_time, min_wait_Res]
