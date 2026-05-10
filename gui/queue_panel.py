import tkinter as tk
from tkinter import ttk

class QueuePanel(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Priority Queue (SJF)", padx=10, pady=10)
        
        columns = ("PID", "MsgID", "Size", "Arrival", "Status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        self.tree.heading("PID", text="Packet ID")
        self.tree.heading("MsgID", text="Msg ID")
        self.tree.heading("Size", text="Size (Priority)")
        self.tree.heading("Arrival", text="Arrival")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("PID", width=60)
        self.tree.column("MsgID", width=50)
        self.tree.column("Size", width=80)
        self.tree.column("Arrival", width=60)
        self.tree.column("Status", width=80)
        
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Legend
        legend_frame = tk.Frame(self)
        legend_frame.pack(side="bottom", fill="x", pady=5)
        tk.Label(legend_frame, text="* Lower Size = Higher Priority", fg="gray").pack(side="left")

