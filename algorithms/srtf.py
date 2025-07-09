def srtf(arrival_times, burst_times):
    if len(arrival_times) == len(burst_times):
        n = len(arrival_times)
    else:
        n = min(len(arrival_times), len(burst_times))

    completion_times = [0] * n
    waiting_times = [0] * n
    turnaround_times = [0] * n

    data = []
    for i in range(0, n):
        data.append((arrival_times[i], burst_times[i], i))

    # Sort by arrival time
    data.sort(key=lambda x: x[0])

    arrival_times_sorted = [data[i][0] for i in range(n)]
    burst_times_sorted = [data[i][1] for i in range(n)]
    process_indices = [data[i][2] for i in range(n)]

    current_time = 0
    completed = 0
    is_completed = [False] * n
    remaining_burst_times = burst_times_sorted.copy()

    while completed < n:
        shortest_remaining_time = float('inf')
        idx_to_run = -1
        for i in range(n):
            if arrival_times_sorted[i] <= current_time and not is_completed[i] and remaining_burst_times[i] < shortest_remaining_time:
                shortest_remaining_time = remaining_burst_times[i]
                idx_to_run = i

        if idx_to_run == -1:
            current_time = min([arrival_times_sorted[i] for i in range(n) if not is_completed[i]])
            continue

        # Run the process for one unit of time
        remaining_burst_times[idx_to_run] -= 1
        current_time += 1

        # Check if the process is completed
        if remaining_burst_times[idx_to_run] == 0:
            is_completed[idx_to_run] = True
            completed += 1

            completion_times[process_indices[idx_to_run]] = current_time
            waiting_times[process_indices[idx_to_run]] = completion_times[process_indices[idx_to_run]] - arrival_times[process_indices[idx_to_run]] - burst_times[process_indices[idx_to_run]]
            turnaround_times[process_indices[idx_to_run]] = completion_times[process_indices[idx_to_run]] - arrival_times[process_indices[idx_to_run]]

    avg_wt = sum(waiting_times) / n
    avg_tat = sum(turnaround_times) / n

    return arrival_times, burst_times, completion_times, waiting_times, turnaround_times, avg_wt, avg_tat

# Example usage:
arrival_times = [0, 2, 4, 6]
burst_times = [1, 3, 1, 5]

arrival_times, burst_times, completion_times, waiting_times, turnaround_times, avg_wt, avg_tat = srtf(arrival_times, burst_times)

