def sjf(arrival_times, burst_times):
    if len(arrival_times) == len(burst_times):
        n = len(arrival_times)
    else:
        n = min(len(arrival_times), len(burst_times))

    # Initialize lists for completion, waiting, and turnaround times
    completion_times = [0] * n
    waiting_times = [0] * n
    turnaround_times = [0] * n

    # Create a list of tuples with arrival and burst times, and original index
    data = []
    for i in range(0, n):
        data.append((arrival_times[i], burst_times[i], i))

    # Sort data by burst time, then by arrival time if burst times are equal
    data.sort(key=lambda x: (x[1], x[0]))

    # Initialize lists to store sorted arrival and burst times
    sorted_arrival_times = [data[i][0] for i in range(n)]
    sorted_burst_times = [data[i][1] for i in range(n)]
    process_indices = [data[i][2] for i in range(n)]

    print("Sorted Arrival Times:", sorted_arrival_times)
    print("Sorted Burst Times:", sorted_burst_times)

    # Initialize current time
    current_time = 0
    completed = 0
    is_completed = [False] * n

    while completed < n:
        shortest_burst_time = float('inf')
        idx_to_run = -1
        for i in range(n):
            if sorted_arrival_times[i] <= current_time and not is_completed[i] and sorted_burst_times[i] < shortest_burst_time:
                shortest_burst_time = sorted_burst_times[i]
                idx_to_run = i

        if idx_to_run == -1:
            current_time = min([sorted_arrival_times[i] for i in range(n) if not is_completed[i]])
            continue

        is_completed[idx_to_run] = True
        completed += 1

        completion_times[process_indices[idx_to_run]] = current_time + sorted_burst_times[idx_to_run]  # Use original index
        waiting_times[process_indices[idx_to_run]] = completion_times[process_indices[idx_to_run]] - sorted_arrival_times[idx_to_run] - sorted_burst_times[idx_to_run]
        turnaround_times[process_indices[idx_to_run]] = completion_times[process_indices[idx_to_run]] - sorted_arrival_times[idx_to_run]

        current_time = completion_times[process_indices[idx_to_run]]

    # Calculate average waiting and turnaround times
    avg_wt = sum(waiting_times) / n
    avg_tat = sum(turnaround_times) / n

    return arrival_times, burst_times, completion_times, waiting_times, turnaround_times, avg_wt, avg_tat
