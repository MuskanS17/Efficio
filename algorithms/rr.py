from typing import List, Dict, Tuple

def rr(arrival_time: List[int], burst_time: List[int], time_quantum: int) -> Tuple[List[Dict], List[Dict]]:
    """
    Round Robin Scheduling Algorithm Implementation.

    Parameters:
    - arrival_time: List of arrival times for each process.
    - burst_time: List of burst times for each process.
    - time_quantum: Time quantum for the Round Robin algorithm.

    Returns:
    - solved_processes_info: List of dictionaries containing solved process information.
    - gantt_chart_info: List of dictionaries representing the Gantt chart.
    """

    # Generate process names
    processes_info = []
    for index, (at, bt) in enumerate(zip(arrival_time, burst_time)):
        job = f"P{index + 1}" if len(arrival_time) <= 26 else chr(ord('A') + index)
        processes_info.append({
            "job": job,
            "at": at,
            "bt": bt,
        })

    # Sort processes by arrival time
    processes_info.sort(key=lambda x: x['at'])

    # Initialize variables
    solved_processes_info = []
    gantt_chart_info = []
    ready_queue = []
    current_time = processes_info[0]['at']
    unfinished_jobs = processes_info.copy()

    # Initialize remaining time dictionary
    remaining_time = {process['job']: process['bt'] for process in processes_info}

    # Add the first job to the ready queue
    ready_queue.append(unfinished_jobs[0])

    while sum(remaining_time.values()) > 0 and unfinished_jobs:
        if not ready_queue and unfinished_jobs:
            # If the ready queue is empty and there are unfinished jobs, add the first unfinished job to the queue
            ready_queue.append(unfinished_jobs[0])
            current_time = ready_queue[0]['at']

        # Select the next process to execute
        process_to_execute = ready_queue[0]

        if remaining_time[process_to_execute['job']] <= time_quantum:
            # If the remaining time is less than or equal to the time quantum, execute until finished
            remaining_t = remaining_time[process_to_execute['job']]
            remaining_time[process_to_execute['job']] -= remaining_t
            prev_current_time = current_time
            current_time += remaining_t

            gantt_chart_info.append({
                "job": process_to_execute['job'],
                "start": prev_current_time,
                "stop": current_time,
            })
        else:
            remaining_time[process_to_execute['job']] -= time_quantum
            prev_current_time = current_time
            current_time += time_quantum

            gantt_chart_info.append({
                "job": process_to_execute['job'],
                "start": prev_current_time,
                "stop": current_time,
            })

        # Find processes that arrive during this cycle and add them to the ready queue
        process_to_arrive_in_this_cycle = [p for p in processes_info if p['at'] <= current_time and p != process_to_execute and p not in ready_queue and p in unfinished_jobs]
        ready_queue.extend(process_to_arrive_in_this_cycle)

        # Move the executed process to the end of the queue
        ready_queue.append(ready_queue.pop(0))

        # If the process has finished executing
        if remaining_time[process_to_execute['job']] == 0:
            # Remove the finished process from unfinished jobs and the ready queue
            unfinished_jobs.remove(process_to_execute)
            if process_to_execute in ready_queue:
                ready_queue.remove(process_to_execute)

            # Add the solved process info
            solved_processes_info.append({
                **process_to_execute,
                'ft': current_time,
                'tat': current_time - process_to_execute['at'],
                'wat': current_time - process_to_execute['at'] - process_to_execute['bt'],
            })

    # Sort the solved processes by arrival time and then by job name
    solved_processes_info.sort(key=lambda x: (x['at'], x['job']))

    at=[]
    bt=[]
    ct=[]
    wt=[]
    tat=[]
    
    for i in solved_processes_info:
       at.append(i['at'])
       bt.append(i['bt'])
       ct.append(i['ft'])
       wt.append(i['wat'])
       tat.append(i['tat'])
      

    avg_wt=sum(wt)/len(solved_processes_info)
    avg_tat=sum(tat)/len(solved_processes_info)

    # return solved_processes_info, gantt_chart_info
    return at,bt,ct,wt,tat, avg_wt, avg_tat

