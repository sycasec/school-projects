
class PCB:
    def __init__(self):
        self.process_list = []
        self.headers = []
    
    def read_from_csv(self, file_name):
        with open(file_name, 'r') as file:
            self.headers = file.readline().strip().split(',')
            for line in file:
                break_commas = line.strip().split(',')
                self.process_list.append([int(i) for i in break_commas])

    def srpt_solver(self):
        """
        schedule process_list by srpt
        """
        p_list = self.process_list.copy()
        p_queue = []


    def generate_gantt_tlist(self):
        """
        generate a list of time to display under process boxes
        processes will be displayed in pseudo gantt boxes
        this function will generate the list of time intervals to be printed
        e.g. 0, 10, 11, 15 ...
        """
        pass

    def generate_gantt_plist(self):
        """
        generate a list of processes to display 
        processes should already be in order
        e.g. RR: Process 1, Process 2, Process 3 ...
        """
        pass

    def test_display_plist(self):
        for item in self.process_list:
            print(item)

if __name__ == "__main__":
    f1 = "Process_1 - process1.csv.csv"
    f2 = "Process_2 - process2.csv.csv"
    x = PCB()
    x.read_from_csv(f1)
    x.test_display_plist()
