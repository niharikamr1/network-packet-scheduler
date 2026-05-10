import tkinter as tk
from tkinter import ttk
from animation.color_manager import ColorManager

class MetricsPanel(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Performance Metrics & Gantt Chart", padx=10, pady=10)
        
        # Metrics Table
        stats_frame = tk.Frame(self)
        stats_frame.pack(side="left", fill="y", padx=(0, 10))
        
        self.metrics_tree = ttk.Treeview(stats_frame, columns=("Metric", "Value"), show="headings", height=5)
        self.metrics_tree.heading("Metric", text="Metric")
        self.metrics_tree.heading("Value", text="Value")
        self.metrics_tree.column("Metric", width=150)
        self.metrics_tree.column("Value", width=100)
        self.metrics_tree.pack(fill="both", expand=True)
        
        # Initialize rows
        self.metrics_tree.insert("", "end", iid="avg_wait", values=("Avg Waiting Time", "0.00"))
        self.metrics_tree.insert("", "end", iid="avg_turn", values=("Avg Turnaround Time", "0.00"))
        self.metrics_tree.insert("", "end", iid="throughput", values=("Throughput", "0.00"))
        
        # Gantt Chart Area
        gantt_frame = tk.LabelFrame(self, text="Gantt Chart (Transmission Order)")
        gantt_frame.pack(side="right", fill="both", expand=True)
        
        self.gantt_canvas = tk.Canvas(gantt_frame, bg="white")
        self.gantt_canvas.pack(fill="both", expand=True)
        
        # Gantt State
        self.gantt_x = 10 
        self.gantt_y = 20
        self.bar_height = 40

    def clear_metrics(self):
        self.metrics_tree.item("avg_wait", values=("Avg Waiting Time", "0.00"))
        self.metrics_tree.item("avg_turn", values=("Avg Turnaround Time", "0.00"))
        self.metrics_tree.item("throughput", values=("Throughput", "0.00"))
        self.gantt_canvas.delete("all")

    def update_metrics(self, scheduler_results):
        print(f"DEBUG: Updating Metrics. Results: {scheduler_results}")
        # Update Table
        self.metrics_tree.item("avg_wait", values=("Avg Waiting Time", f"{scheduler_results['avg_waiting_time']:.2f}"))
        self.metrics_tree.item("avg_turn", values=("Avg Turnaround Time", f"{scheduler_results['avg_turnaround_time']:.2f}"))
        self.metrics_tree.item("throughput", values=("Throughput", f"{scheduler_results['throughput']:.4f}"))
        
        # Update Gantt Chart
        self.draw_gantt_chart(scheduler_results['execution_log'])

    def draw_gantt_chart(self, execution_log):
        self.gantt_canvas.delete("all")
        
        start_x = 10
        y = 20
        scale = 10 # Pixels per time unit (adjustable)
        
        if not execution_log: return
        
        # Adjust scale if drawing gets too wide
        total_time = execution_log[-1]['End_Time']
        canvas_width = self.gantt_canvas.winfo_width()
        if total_time * scale > canvas_width - 20 and total_time > 0:
             scale = (canvas_width - 20) / total_time
        
        for entry in execution_log:
            pid = entry['Packet_ID']
            # We use 'Start_Time' logic from scheduler, assuming 0-based relative to simulation start
            # or cumulative. The log has absolute start/end.
            
            x1 = start_x + (entry['Start_Time'] * scale)
            x2 = start_x + (entry['End_Time'] * scale)
            
            color = ColorManager.get_color("SJF Selection") # Standard color for executed block
            
            # Draw Bar
            self.gantt_canvas.create_rectangle(x1, y, x2, y + self.bar_height, fill=color, outline="black")
            
            # Draw Label
            mid = (x1 + x2) / 2
            self.gantt_canvas.create_text(mid, y + self.bar_height/2, text=pid, fill="white", font=("Arial", 8, "bold"))
            
            # Draw Time Markers
            self.gantt_canvas.create_text(x1, y + self.bar_height + 10, text=str(entry['Start_Time']), font=("Arial", 7))
            self.gantt_canvas.create_text(x2, y + self.bar_height + 10, text=str(entry['End_Time']), font=("Arial", 7))


