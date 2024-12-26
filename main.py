import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from fcfs import run_fcfs
from srt import run_srt
from rr import run_rr

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Scheduler Simulator")

        # Frame for process input
        self.process_frame = ttk.LabelFrame(root, text="Add Process")
        self.process_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(self.process_frame, text="Process ID").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self.process_frame, text="Arrival Time").grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.process_frame, text="Burst Time").grid(row=0, column=2, padx=5, pady=5)

        self.process_id_entry = ttk.Entry(self.process_frame, width=10)
        self.arrival_time_entry = ttk.Entry(self.process_frame, width=10)
        self.burst_time_entry = ttk.Entry(self.process_frame, width=10)

        self.process_id_entry.grid(row=1, column=0, padx=5, pady=5)
        self.arrival_time_entry.grid(row=1, column=1, padx=5, pady=5)
        self.burst_time_entry.grid(row=1, column=2, padx=5, pady=5)

        ttk.Button(self.process_frame, text="Add Process", command=self.add_process).grid(row=1, column=3, padx=5, pady=5)
        ttk.Button(self.process_frame, text="Clear Processes", command=self.clear_processes).grid(row=1, column=4, padx=5, pady=5)

        # Process list
        self.process_list = []
        self.process_tree = ttk.Treeview(root, columns=("Arrival", "Burst"), show="headings")
        self.process_tree.grid(row=1, column=0, padx=10, pady=10)
        self.process_tree.heading("Arrival", text="Arrival Time")
        self.process_tree.heading("Burst", text="Burst Time")

        # Buttons for scheduling
        self.buttons_frame = ttk.Frame(root)
        self.buttons_frame.grid(row=2, column=0, pady=10)

        ttk.Button(self.buttons_frame, text="FCFS", command=lambda: self.choose_action("FCFS")).grid(row=0, column=0, padx=5)
        ttk.Button(self.buttons_frame, text="SRT", command=lambda: self.choose_action("SRT")).grid(row=0, column=1, padx=5)
        ttk.Button(self.buttons_frame, text="RR", command=self.run_rr).grid(row=0, column=3, padx=5)

    def add_process(self):
        try:
            process_id = self.process_id_entry.get()
            arrival_time = int(self.arrival_time_entry.get())
            burst_time = int(self.burst_time_entry.get())

            if not process_id:
                raise ValueError("Process ID cannot be empty")

            self.process_list.append({
                "process_id": process_id,
                "arrival_time": arrival_time,
                "burst_time": burst_time,
            })
            self.process_tree.insert("", "end", values=(arrival_time, burst_time))
            self.process_id_entry.delete(0, tk.END)
            self.arrival_time_entry.delete(0, tk.END)
            self.burst_time_entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def clear_processes(self):
        self.process_list = []
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)

    def choose_action(self, algorithm, quantum=None):
        if not self.process_list:
            messagebox.showerror("Error", "No processes added.")
            return

        action_window = tk.Toplevel(self.root)
        action_window.title(f"{algorithm} Actions")

        ttk.Button(action_window, text="Show Gantt Chart", command=lambda: self.show_gantt_chart(algorithm, quantum)).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(action_window, text="Calculations", command=lambda: self.show_calculations(algorithm, quantum)).grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(action_window, text="CPU Utilization", command=lambda: self.show_utilization(algorithm, quantum)).grid(row=0, column=2, padx=10, pady=10)

    
    def show_utilization(self, algorithm, quantum=None):
        results = self.run_algorithm(algorithm, quantum)
        gantt_chart = results[0]

        # Calculate CPU Utilization
        busy_time = sum(end - start for _, start, end in gantt_chart)
        total_time = max(end for _, _, end in gantt_chart)
        utilization = (busy_time / total_time) * 100 if total_time > 0 else 0

        utilization_window = tk.Toplevel(self.root)
        utilization_window.title(f"{algorithm} Utilization")

        ttk.Label(utilization_window, text=f"CPU Utilization: {utilization:.2f}%").grid(row=0, column=0, padx=10, pady=10)
    def run_algorithm(self, algorithm, quantum=None):
        if algorithm == "FCFS":
            return run_fcfs(self.process_list)
        elif algorithm == "SRT":
            return run_srt(self.process_list)
        elif algorithm == "RR":
            return run_rr(self.process_list, quantum)

    def show_gantt_chart(self, algorithm, quantum=None):
        results = self.run_algorithm(algorithm, quantum)
        gantt_chart = results[0]

        merged_intervals = []
        for pid, start, end in gantt_chart:
            if merged_intervals and merged_intervals[-1][0] == pid and merged_intervals[-1][2] == start:
                merged_intervals[-1][2] = end
            else:
                merged_intervals.append([pid, start, end])

        fig, ax = plt.subplots(figsize=(8, 1))
        for pid, start, end in merged_intervals:
            ax.barh(y=0, width=end - start, left=start, align='center', color='skyblue', edgecolor='black')
            ax.text((start + end) / 2, 0, pid, ha='center', va='center', fontsize=10, color='black')

        ax.set_yticks([])
        ax.set_xlim(0, max(end for _, _, end in merged_intervals))
        ax.set_xlabel("Time")
        ax.set_title(f"Gantt Chart - {algorithm}")

        plt.tight_layout()
        plt.show()

    def show_calculations(self, algorithm, quantum=None):
        results = self.run_algorithm(algorithm, quantum)
        avg_waiting, avg_turnaround = results[2], results[3]

        calc_window = tk.Toplevel(self.root)
        calc_window.title(f"{algorithm} Calculations")

        ttk.Label(calc_window, text=f"Average Waiting Time: {avg_waiting:.2f}").grid(row=0, column=0, padx=10, pady=10)
        ttk.Label(calc_window, text=f"Average Turnaround Time: {avg_turnaround:.2f}").grid(row=1, column=0, padx=10, pady=10)

    def run_rr(self):
        if not self.process_list:
            messagebox.showerror("Error", "No processes added.")
            return

        quantum_window = tk.Toplevel(self.root)
        quantum_window.title("Quantum Input")

        ttk.Label(quantum_window, text="Enter Quantum:").grid(row=0, column=0, padx=10, pady=10)
        quantum_entry = ttk.Entry(quantum_window)
        quantum_entry.grid(row=0, column=1, padx=10, pady=10)

        def submit_quantum():
            try:
                quantum = int(quantum_entry.get())
                if quantum <= 0:
                    raise ValueError("Quantum must be a positive integer.")
                quantum_window.destroy()

                self.choose_action("RR", quantum)
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(quantum_window, text="Submit", command=submit_quantum).grid(row=1, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()

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