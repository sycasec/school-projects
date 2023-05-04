from copy import deepcopy

class ProcessControlBoard:
    def __init__(self):
        self.process_dict = {}
        self.headers = []

    def read_from_csv(self, filename):
        self.file = filename
        with open(filename, 'r') as file:
            self.headers = file.readline().split(',')
            for line in file:
                values = [int(i) for i in line.strip().split(',')]
                self.process_dict[values[0]] = {'arrival': values[1], 'burst': values[2], 'prio': values[3], 'wait': -1}

    def get_process_dict_as_list(self) -> list:
        p_list = []
        for item in self.process_dict:
            p_list.append(item)
            p_list.append(self.process_dict[item]['arrival'])
            p_list.append(self.process_dict[item]['burst'])
            p_list.append(self.process_dict[item]['prio'])

        return p_list

    def srpt_solver(self, p_dict):
        ready_q = []
        copy_dict = deepcopy(p_dict) 

        curr_time = 0
        g_list = []
        t_list = []
        completed = {}
        while len(p_dict) > 0:
            for p in p_dict:
                if p_dict[p]['arrival'] == curr_time and p not in ready_q:
                    ready_q.append(p)
            if len(ready_q) > 0:
                shortest = ready_q[0]
                for p in ready_q:
                    if p_dict[p]['burst'] < p_dict[shortest]['burst']:
                        shortest = p

                if len(g_list) == 0 or g_list[-1] != shortest:
                    g_list.append(shortest)
                    t_list.append(curr_time)

                p_dict[shortest]['burst'] -= 1
                
                if p_dict[shortest]['burst'] == 0:
                    completed[shortest] ={
                        'finish': curr_time + 1,
                        'turnaround': (curr_time + 1) - p_dict[shortest]['arrival'],
                        'wait': ((curr_time + 1) - p_dict[shortest]['arrival']) - copy_dict[shortest]['burst']
                    }

                    del p_dict[shortest]
                    ready_q.remove(shortest)

            curr_time +=1 
        t_list.append(curr_time)

        return dict(sorted(completed.items())), g_list, t_list
                

    def rr_solver(self, p_dict:dict, quantum:int) -> (dict, list, list):
        copy_dict = deepcopy(p_dict)
        curr_time = 0
        completed = {}
        g_list = []
        t_list = [0]
        c_p = -1

        while len(p_dict) > 0:
            for p in copy_dict:
                for k, v in p_dict.items(): print(k, v, sep="::")
                print(f"time={curr_time}")
                if p in p_dict.keys() and p_dict[p]['burst'] > 0:
                    c_p = p
                else:
                    continue

                p_dict[c_p]['burst'] -= quantum
                curr_time += quantum
                if p_dict[c_p]['burst'] <= 0:
                    if p_dict[c_p]['burst'] < 0: 
                        curr_time += p_dict[c_p]['burst']
                    completed[c_p] = {
                        'finish': curr_time,
                        'turnaround': curr_time,
                        'wait': curr_time - copy_dict[c_p]['burst']
                    }
                    del p_dict[c_p]
                
                g_list.append(c_p)
                t_list.append(curr_time)

        return dict(sorted(completed.items())), g_list, t_list

    def fcfs_solver(self, p_dict:dict) -> (dict, list ,list):
        # copy_dict = deepcopy(p_dict)
        curr_time = 0
        completed = {}
        g_list = []
        t_list = [0]
        p_q = [p for p in p_dict.keys()]
        p_q.sort(key=lambda p: p_dict[p]['arrival'], reverse=True)

        while len(p_q) > 0:
            c_p = p_q.pop()
            # p_dict[c_p]['burst'] -= file
            curr_time += p_dict[c_p]['burst']
            
            completed[c_p] = {
                'finished': curr_time,
                'turnaround': curr_time,
                'wait': t_list[-1],
            }
            g_list.append(c_p)
            t_list.append(curr_time)
        
        return dict(sorted(completed.items())), g_list, t_list

    def sjf_solver(self, p_dict: dict) -> (dict, list, list):
        curr_time = 0
        completed = {}
        g_list = []
        t_list = [0]
        p_q = [p for p in p_dict.keys()]
        p_q.sort(key=lambda p: p_dict[p]['burst'], reverse=True) 
        for i in range(len(p_q) - 1):
            if p_dict[p_q[i]]['burst'] == p_dict[p_q[i+1]]['burst']:
                if p_dict[p_q[i]]['arrival'] < p_dict[p_q[i+1]]['arrival']:
                    p_q[i], p_q[i+1] = p_q[i+1], p_q[i] 

        while len(p_q) > 0:
            c_p = p_q.pop()
            curr_time += p_dict[c_p]['burst']
            
            completed[c_p] = {
                'finished': curr_time,
                'turnaround': curr_time,
                'wait': t_list[-1],
            }
            g_list.append(c_p)
            t_list.append(curr_time)
        
        return dict(sorted(completed.items())), g_list, t_list

    def prio_solver(self, p_dict: dict) -> dict:
        curr_time = 0
        completed = {}
        g_list = []
        t_list = [0]
        p_q = [p for p in p_dict.keys()]
        p_q.sort(key=lambda p: p_dict[p]['prio'], reverse=True)
        for i in range(len(p_q) - 1):
            if p_dict[p_q[i]]['prio'] == p_dict[p_q[i+1]]['prio']:
                if p_q[i] < p_q[i+1]:
                    p_q[i], p_q[i+1] = p_q[i+1], p_q[i]
        # print(f"deb::{p_q}")
        while len(p_q) > 0:
            c_p = p_q.pop()
            curr_time += p_dict[c_p]['burst']
            
            completed[c_p] = {
                'finished': curr_time,
                'turnaround': curr_time,
                'wait': t_list[-1],
            }
            g_list.append(c_p)
            t_list.append(curr_time)
        
        return dict(sorted(completed.items())), g_list, t_list       


    def generate_gantt_list(self, method:str):
        pass
        # p_dict = self.process_dict.copy()


    def test_displayProcessList(self):
        print(self.headers)
        for item in self.process_dict:
            print(item, self.process_dict[item], sep='::') 

    def test_rr(self):
        x, g, t = self.rr_solver(deepcopy(self.process_dict), quantum = 4)
        for k, v in x.items(): print(k, v, sep="::")
    
    def test_fcfs(self):
        x, g, t = self.fcfs_solver(deepcopy(self.process_dict))
        for k, v in x.items(): print(k, v, sep="::")

    def test_sjf(self):
        x, g, t = self.sjf_solver(deepcopy(self.process_dict))
        for k, v in x.items(): print(k, v, sep="::")

    def test_prio(self):
        x, g, t = self.prio_solver(deepcopy(self.process_dict))
        for k, v in x.items(): print(k, v, sep="::")


if __name__ == "__main__":
    file1 = "Process_1 - process1.csv.csv"
    file2 = "Process_2 - process2.csv.csv"
    tfile = "test.csv"
    pfile = "pptest.csv"
    test_pcb = ProcessControlBoard()
    test_pcb.read_from_csv(pfile)
    # test_pcb.test_rr()
    # test_pcb.test_fcfs()
    # test_pcb.test_sjf()
    test_pcb.test_prio()
    test_pcb.test_displayProcessList()

