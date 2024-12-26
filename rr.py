def run_rr(process_list, quantum):
    process_list = sorted(process_list, key=lambda x: x["arrival_time"])
    time = 0
    queue = process_list[:]
    gantt_chart = []
    finish_times = {}
    waiting_time = 0
    turnaround_time = 0
    remaining_burst = {p["process_id"]: p["burst_time"] for p in process_list}
    completed = set()
    first_response = {}

    while queue:
        process = queue.pop(0)
        pid = process["process_id"]

        if time < process["arrival_time"]:
            time = process["arrival_time"]

        if pid not in first_response:
            first_response[pid] = time

        if remaining_burst[pid] > quantum:
            start = time
            time += quantum
            remaining_burst[pid] -= quantum
            end = time
            queue.append(process)
        else:
            start = time
            time += remaining_burst[pid]
            end = time
            remaining_burst[pid] = 0
            finish_times[pid] = end
            completed.add(pid)

            turnaround_time += end - process["arrival_time"]
            waiting_time += end - process["arrival_time"] - process["burst_time"]

        gantt_chart.append((pid, start, end))

    avg_waiting = waiting_time / len(process_list)
    avg_turnaround = turnaround_time / len(process_list)

    return gantt_chart, finish_times, avg_waiting, avg_turnaround
