import tkinter as tk
from tkinter import ttk

class MessagePanel(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Message Storage System", padx=10, pady=10)
        
        # Input Area
        input_frame = tk.Frame(self)
        input_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(input_frame, text="Enter Message:").pack(side="left")
        self.msg_entry = tk.Entry(input_frame)
        self.msg_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        self.add_btn = tk.Button(input_frame, text="Add Message", bg="#4CAF50", fg="white")
        self.add_btn.pack(side="right")
        
        # Message List Area
        list_frame = tk.Frame(self)
        list_frame.pack(fill="both", expand=True)
        
        columns = ("ID", "Text", "Status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Text", text="Message Text")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("ID", width=50)
        self.tree.column("Text", width=200)
        self.tree.column("Status", width=80)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

