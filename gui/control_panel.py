import tkinter as tk

class ControlPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f0f0", pady=5)
        
        self.start_btn = tk.Button(self, text="▶ Start Simulation", bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
        self.start_btn.pack(side="left", padx=5)
        
        self.pause_btn = tk.Button(self, text="⏸ Pause", bg="#FFC107", fg="black")
        self.pause_btn.pack(side="left", padx=5)
        
        self.reset_btn = tk.Button(self, text="🔄 Reset", bg="#F44336", fg="white")
        self.reset_btn.pack(side="left", padx=5)
        
        self.step_btn = tk.Button(self, text="⏯ Single Step", bg="gray", fg="white")
        self.step_btn.pack(side="left", padx=5)

