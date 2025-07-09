def fcfs(arrival_times, burst_times):
    # Check if arrival_times and burst_times have the same length
    if len(arrival_times) == len(burst_times):
        n = len(arrival_times)
    else:
        n = min(len(arrival_times), len(burst_times))

    # Initialize lists for completion, waiting, and turnaround times
    completion_times = [0]*n
    waiting_times = [0]*n
    turnaround_times = [0]*n

    # Create a list of tuples with arrival and burst times
    data = []
    for i in range(0, n):
        data.append((arrival_times[i], burst_times[i], i))  # Store original index

    # Sort data by arrival time
    sorted_data = sorted(data, key=lambda x: x[0])

    # Initialize lists to store sorted arrival and burst times
    sorted_arrival_times = [0]*n
    sorted_burst_times = [0]*n

    # Store sorted arrival and burst times
    for i in range(n):
        sorted_arrival_times[i] = sorted_data[i][0]
        sorted_burst_times[i] = sorted_data[i][1]

    # print("Sorted Arrival Times:", sorted_arrival_times)
    # print("Sorted Burst Times:", sorted_burst_times)

    # Initialize current time
    current_time = 0

    # Calculate completion, waiting, and turnaround times
    for i in range(n):
        if current_time < sorted_arrival_times[i]:
            current_time = sorted_arrival_times[i]

        completion_times[sorted_data[i][2]] = current_time + sorted_burst_times[i]  # Use original index
        waiting_times[sorted_data[i][2]] = completion_times[sorted_data[i][2]] - sorted_arrival_times[i] - sorted_burst_times[i]
        turnaround_times[sorted_data[i][2]] = completion_times[sorted_data[i][2]] - sorted_arrival_times[i]

        current_time = completion_times[sorted_data[i][2]]

    # Calculate average waiting and turnaround times
    avg_wt = sum(waiting_times) / n
    avg_tat = sum(turnaround_times) / n

    return arrival_times, burst_times, completion_times, waiting_times, turnaround_times, round(avg_wt,2), round(avg_tat,2)