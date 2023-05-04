processes = {
    'P1': {'arrival': 0, 'burst': 5},
    'P2': {'arrival': 2, 'burst': 3},
    'P3': {'arrival': 4, 'burst': 1},
    'P4': {'arrival': 5, 'burst': 2}
}
# Sort the processes by arrival time
sorted_processes = sorted(processes.items(), key=lambda x: x[1]['arrival'])

# Initialize the waiting times dictionary
waiting_times = {k: 0 for k in processes}

# Initialize the remaining time dictionary
remaining_time = {k: v['burst'] for k, v in sorted_processes}

# Initialize the Gantt chart
gantt_chart = []

# Initialize the current time
current_time = 0

# Loop until all processes have completed
while remaining_time:
    # Get a list of processes that have arrived and still have remaining time
    available_processes = [(k, v) for k, v in sorted_processes if k in remaining_time and v['arrival'] <= current_time]

    # If there are no available processes, increment the current time
    if not available_processes:
        current_time += 1
        gantt_chart.append('IDLE')
        continue

    # Sort the available processes by remaining time
    available_processes = sorted(available_processes, key=lambda x: x[1]['burst'])

    # Get the process with the shortest remaining time
    process, process_data = available_processes[0]

    # Update the waiting times for the other processes
    for k, v in remaining_time.items():
        if k != process and k in sorted_processes and sorted_processes[k]['arrival'] <= current_time:
            waiting_times[k] += 1

    # Add the current process to the Gantt chart
    gantt_chart.append(process)

    # Decrement the remaining time for the current process
    remaining_time[process] -= 1

    # If the current process has completed, remove it from the remaining time dictionary
    if remaining_time[process] == 0:
        del remaining_time[process]

    # Increment the current time
    current_time += 1


print('\nGantt Chart:')
for i in range(len(gantt_chart)-1):
    print('[' + str(gantt_chart[i][1]) + '] ' + gantt_chart[i][0], end=' -- ')
print('[' + str(gantt_chart[-1][1]) + '] ' + gantt_chart[-1][0])
print(f"wait::{waiting_times}")
