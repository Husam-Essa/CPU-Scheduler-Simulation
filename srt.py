def run_srt(process_list):
    process_list = sorted(process_list, key=lambda x: x["arrival_time"])
    time = 0
    gantt_chart = []
    finish_times = {}
    waiting_time = 0
    turnaround_time = 0
    remaining_burst = {p["process_id"]: p["burst_time"] for p in process_list}
    completed = set()

    while len(completed) < len(process_list):
        ready_processes = [p for p in process_list if p["arrival_time"] <= time and p["process_id"] not in completed]
        if not ready_processes:
            time += 1
            continue

        # Select the process with the shortest remaining time
        current = min(ready_processes, key=lambda x: remaining_burst[x["process_id"]])
        start = time
        time += 1
        remaining_burst[current["process_id"]] -= 1

        # If the process is complete
        if remaining_burst[current["process_id"]] == 0:
            completed.add(current["process_id"])
            finish_times[current["process_id"]] = time
            turnaround_time += time - current["arrival_time"]
            waiting_time += time - current["arrival_time"] - current["burst_time"]

        gantt_chart.append((current["process_id"], start, time))

    avg_waiting = waiting_time / len(process_list)
    avg_turnaround = turnaround_time / len(process_list)

    return gantt_chart, finish_times, avg_waiting, avg_turnaround

