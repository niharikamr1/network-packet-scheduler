import tkinter as tk

class AnimationPanel(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="VPN Transmission Visualization", padx=10, pady=10)
        
        self.canvas = tk.Canvas(self, bg="white", height=300)
        self.canvas.pack(fill="both", expand=True)
        
        # Static Design Elements
        self.draw_network_topology()

    def draw_network_topology(self):
        w = 800 # Nominal width, will resize dynamically in real app logic if needed
        h = 300
        
        # Client Node
        self.canvas.create_oval(50, 100, 150, 200, fill="#E3F2FD", outline="#2196F3", width=2)
        self.canvas.create_text(100, 150, text="Client\n(Segmentation)", justify="center")
        
        # Server Node
        self.canvas.create_oval(650, 100, 750, 200, fill="#E8F5E9", outline="#4CAF50", width=2)
        self.canvas.create_text(700, 150, text="Server\n(Reassembly)", justify="center")
        
        # Improved VPN Tunnel Visual (Solid, slightly transparent if canvas supports it, but here solid light purple)
        self.canvas.create_rectangle(150, 110, 650, 190, fill="#E1BEE7", outline="#9C27B0", width=2) 
        self.canvas.create_text(400, 150, text="VPN Tunnel\n(Transmission)", fill="#4A148C", font=("Arial", 10, "bold"))
        
        # Queue Area (Visual representation)
        self.canvas.create_rectangle(50, 220, 350, 280, outline="gray", dash=(4, 4))
        self.canvas.create_text(200, 210, text="Waiting Queue Buffer", fill="gray")
