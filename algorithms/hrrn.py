def hrrn(arrival_times, burst_times):
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

    while completed < n:
        max_response_ratio = 0
        idx_to_run = -1
        for i in range(n):
            if arrival_times_sorted[i] <= current_time and not is_completed[i]:
                waiting_time = current_time - arrival_times_sorted[i]
                response_ratio = (waiting_time + burst_times_sorted[i]) / burst_times_sorted[i]
                if response_ratio > max_response_ratio:
                    max_response_ratio = response_ratio
                    idx_to_run = i

        if idx_to_run == -1:
            current_time = min([arrival_times_sorted[i] for i in range(n) if not is_completed[i]])
            continue

        # Run the process to completion
        current_time += burst_times_sorted[idx_to_run]
        is_completed[idx_to_run] = True
        completed += 1

        completion_times[process_indices[idx_to_run]] = current_time
        waiting_times[process_indices[idx_to_run]] = completion_times[process_indices[idx_to_run]] - arrival_times[process_indices[idx_to_run]] - burst_times[process_indices[idx_to_run]]
        turnaround_times[process_indices[idx_to_run]] = completion_times[process_indices[idx_to_run]] - arrival_times[process_indices[idx_to_run]]

    avg_wt = sum(waiting_times) / n
    avg_tat = sum(turnaround_times) / n

    return arrival_times, burst_times, completion_times, waiting_times, turnaround_times, avg_wt, avg_tat