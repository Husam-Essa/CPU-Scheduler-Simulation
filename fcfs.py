def run_fcfs(process_list):
    sorted_processes = sorted(process_list, key=lambda x: x["arrival_time"])
    time = 0
    gantt_chart = []
    finish_times = {}
    waiting_time = 0
    turnaround_time = 0

    for process in sorted_processes:
        if time < process["arrival_time"]:
            time = process["arrival_time"]
        start = time
        time += process["burst_time"]
        end = time

        gantt_chart.append((process["process_id"], start, end))
        finish_times[process["process_id"]] = end

        # Calculate waiting and turnaround times
        waiting_time += start - process["arrival_time"]
        turnaround_time += end - process["arrival_time"]

    avg_waiting = waiting_time / len(process_list)
    avg_turnaround = turnaround_time / len(process_list)

    return gantt_chart, finish_times, avg_waiting, avg_turnaround
