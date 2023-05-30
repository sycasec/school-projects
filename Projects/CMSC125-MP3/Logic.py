#!/usr/bin/env python

from copy import deepcopy

class MemoryAllocator:
    def __init__(self):
        self.jobs = {}
        self.blocks = {}
        self.waitQueue = []

    # HELPER FUNCTIONS

    def read_from_file(self, memfile, jobfile):
        self.read_from_memfile(memfile)
        self.read_from_jobfile(jobfile)

    def read_from_memfile(self, memfile):
        with open(memfile, 'r') as file:
            for line in file:
                data = [int(d) for d in line.strip().split()] 
                self.blocks[data[0]] = {"size": data[1], "job": -1, "a_size": data[1]}

        self.blocks_copy = deepcopy(self.blocks)

    def read_from_jobfile(self, jobfile):
        with open(jobfile, 'r') as file:
            for line in file:
                data = line.strip().split()
                data = [int(d) for d in line.strip().split()] 
                self.jobs[data[0]] = {"time": data[1], "size": data[2], "status": "ready", "wait": 0}
        
        self.jobs_copy = deepcopy(self.jobs)

    def is_mem_available_ff(self, mem_id, job_size) -> bool:
        if self.blocks[mem_id]["job"] == -1 and job_size <= self.blocks[mem_id]["size"]:
            return True
        return False

    def get_wait_queue(self):
        return [{id:self.jobs[id]} for id in self.waitQueue]
    
    def get_blocks(self):
        return deepcopy(self.blocks)

    def get_jobs(self):
        return deepcopy(self.jobs)

    def get_fragmentation(self):
        frag_list = []
        for m_id, m_data in self.get_blocks().items():
            frag_list.append(m_data['a_size'] / m_data['size'])
        return frag_list

    def get_average_fragmentation(self):
        # frags = list(filter(lambda f: f != .1, self.get_fragmentation()))
        return sum(self.get_fragmentation()) / len(self.blocks)

    def total_avg_frag_helper(self): 
        frags = list(filter(lambda f: f != .1, self.get_fragmentation()))
        return sum(frags) / len(frags)

    def get_average_wait(self):
        total_wait = sum(j['wait'] for j in self.get_jobs().values())
        return total_wait / len(self.jobs) 

    def get_utilization(self):
        total_internal_fragmentation = sum(m['a_size'] for m in self.get_blocks().values())
        total_block_size = sum(m['size'] for m in self.get_blocks().values())
        total_utilization = (total_block_size - total_internal_fragmentation) / total_block_size
        return total_utilization

    def get_total_time(self):
        return sum(j['time'] for j in self.get_jobs().values()) 

    def create_ready_queue(self):
        self.ready_queue = [{j:self.jobs[j]} for j in self.jobs]


    def generate_sorted_blocks(self, reverse=False):
        blocks_copy = deepcopy(self.blocks)
        if reverse:
            return dict(sorted(blocks_copy.items(), key=lambda i: -i[1]['size']))
        return dict(sorted(blocks_copy.items(), key=lambda i: i[1]['size']))
            
    def deallocate_job(self, job_id:int):
        """
        PARAMS - JobID
        locate block JobID is bound to 
        $ MemoryBlock[BlockID]['job'] = -1
        $ MemoryBlock[BlockID]['a_size'] = SIZE
        $ Jobs[JobID]['status'] = DONE
        """

        for blockID, blockDATA in self.get_blocks().items():
            if blockDATA['job'] == job_id:
                self.blocks[blockID]['job'] = -1
                self.blocks[blockID]['a_size'] = blockDATA['size']
                self.jobs[job_id]['status'] = "done"
                break
    
    def get_memory_sizes(self):
        return [ self.blocks[id]['size'] for id in self.blocks.keys() ]

    def fat_jobs(self):
        fj = 0
        for jobID, jobDATA in self.get_jobs().items():
            if jobDATA['status'] == "ready":
                if jobDATA['size'] > max(self.get_memory_sizes()):
                    fj += 1
        return fj

    def get_done(self):
        d = 0
        for jID, jDATA in self.get_jobs().items():
            if jDATA['status'] == 'done':
                d += 1
        return d

    def halt_condition(self) -> bool:
        if self.get_total_time() < 1:
            return True
        return False

    # EXECUTION FUNCTIONS
    # NOTES
    # Only one job can occupy Memory!
    def assignJobtoMemory(self, mem_id, job_id, size):
        """
        PARAMS - MemoryID, JobID, JobSIZE, JobTIME

        Loosely associates job with Memory
        add to blocks[MemoryID] Job data (ID, SIZE, TIME)
        """
        previous_data = self.blocks[mem_id]
        self.blocks[mem_id]["job"] = job_id
        self.blocks[mem_id]["a_size"] =  previous_data["size"] - size
        self.jobs[job_id]["status"] = "run"

    def allocateJobs(self):
        for job_id, job_data in self.get_jobs().items():
            size = job_data["size"]

            if job_data["status"] == "ready":
                # ASSIGN TO MEMORY
                for mem_id, mem_data in self.get_blocks().items():
                    if self.is_mem_available_ff(mem_id, size):
                        self.assignJobtoMemory(mem_id, job_id, size)
                        break
                    else:
                        continue

                if self.jobs[job_id]["status"] == "ready" and job_id not in self.waitQueue:
                    self.waitQueue.append(job_id)

    def firstFit(self):
        for job_id, job_data in self.get_jobs().items():
            size = job_data["size"]
            time = job_data["time"]

            if job_data["status"] == "ready":
                # ASSIGN TO MEMORY
                for mem_id, mem_data in self.get_blocks().items():
                    if self.is_mem_available_ff(mem_id, size):
                        if job_id in self.waitQueue:
                            self.waitQueue.remove(job_id)
                        self.assignJobtoMemory(mem_id, job_id, size)
                        break
                    else:
                        continue

                if self.jobs[job_id]["status"] == "ready" and job_id not in self.waitQueue:
                    self.waitQueue.append(job_id)

                elif self.jobs[job_id]["status"] == "ready" and job_id in self.waitQueue:
                    self.jobs[job_id]["wait"] += 1

            elif job_data["status"] == "run":
                # CHECK IF TIME DONE                
                self.jobs[job_id]["time"] -= 1
                time -= 1
                if time < 1:
                    # DEALLOCATE, CHANGE STATUS "DONE"
                    self.deallocate_job(job_id)
                    self.jobs[job_id]["status"] = "done"


def test_print(tm: MemoryAllocator):
    for k, v in tm.blocks.items():
        print(f"{k}::{v}")

    for k,v in tm.jobs.items():
        print(f"{k}::{v}")

def print_listed_dict(ld):
    for item in ld:
        print(f"{item}")
    
def tests(): 
    tm = MemoryAllocator()

    tm.read_from_file("mem_list1.txt", "job_list1.txt")
    # test_print(tm)
    # tm.initialFirstFit()
    # test_print(tm)
    # print("wait queue")

    # print_listed_dict(tm.create_ready_queue())
    tm.create_ready_queue()

    # for j in tm.get_wait_queue():
        # print(j)
    # for m in tm.get_mem_list():
    #     print(m)

    
    
if __name__ == "__main__":
    tests()

