import tkinter as tk
from tkinter import messagebox
from gui.message_panel import MessagePanel
from gui.queue_panel import QueuePanel
from gui.animation_panel import AnimationPanel
from gui.metrics_panel import MetricsPanel
from gui.control_panel import ControlPanel
from storage.data_manager import DataManager
from scheduler.priority_queue import PriorityQueue
from scheduler.sjf_scheduler import SJFScheduler

from animation.packet_animation import PacketAnimation

from server.reassembly import Reassembly

class MainWindow:
    def __init__(self, root):
        # ... existing init ...
        self.root = root
        self.root.title("Network Packet Scheduler")
        self.root.geometry("1400x900")
        
        # Backend Initialization
        self.data_manager = DataManager()
        self.pq = PriorityQueue()
        self.scheduler = SJFScheduler(self.pq)
        self.reassembler = Reassembly() # Initialize Reassembler
        
        # ... existing setup ...
        # (Rest of init)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=3)
        self.root.grid_rowconfigure(0, weight=1)
        
        self.setup_ui()
        self.animator = PacketAnimation(self.animation_panel.canvas)
        self.is_running = False
        self.simulation_speed = 1000 
        self.bind_events()
        
        # Load Existing Data
        self.load_initial_data()

    def load_initial_data(self):
        # 1. Load Messages
        messages = self.data_manager.get_all_messages()
        for msg in messages:
            self.message_panel.tree.insert("", "end", values=(msg.message_id, msg.message_text, msg.status))
            
        # 2. Load Packets
        packets = self.data_manager.get_all_packets()
        for p in packets:
            # If packet is 'Waiting', add to queue and schedule
            if p.status == "Waiting":
                self.scheduler.add_packet_to_queue(p)
                self.queue_panel.tree.insert("", "end", values=(p.packet_id, p.message_id, p.size, p.arrival_time, p.status))
                self.animator.create_packet(p)
                self.animator.place_in_queue(p.packet_id)
            elif p.status == "Received":
                 # If we wanted to show completed packets somewhere, allow logic here
                 # For animation, we typically don't persist completed state visuals unless we want to clutter the screen.
                 pass

    # ... existing methods ...

    def run_simulation_step(self, single_step=False):
        if not self.is_running and not single_step:
            return
            
        # 1. Check if queue has packets
        if not self.scheduler.pq.is_empty():
            # Get next packet without popping (peek) to visualize selection
            packet = self.scheduler.pq.peek()
            
            # Visualize Selection
            self.animator.update_status(packet.packet_id, "SJF Selection")
            self.root.update() # Force redraw
            
            # Simulate Processing (Animation)
            self.animator.animate_transmission(packet.packet_id, duration_ms=500)
            
            # Commit processing
            processed_packet = self.scheduler.pq.pop()
            self.animator.complete(processed_packet.packet_id)
            
            # Update Metrics
            results = self.scheduler.get_results()
            self.metrics_panel.update_metrics(results)
            
            # Update Queue Panel (Remove processed)
            for item in self.queue_panel.tree.get_children():
                vals = self.queue_panel.tree.item(item)['values']
                if vals[0] == processed_packet.packet_id:
                    self.queue_panel.tree.delete(item)
                    break
        
            # Check for Message Completion
            self.check_message_completion(processed_packet.message_id)
            
        if self.is_running and not single_step:
            self.root.after(self.simulation_speed, self.run_simulation_step)

    def check_message_completion(self, message_id):
        # 1. Check if any packets for this message are still in the Queue
        queued_packets = self.scheduler.pq.get_all_packets()
        pending_for_msg = [p for p in queued_packets if p.message_id == message_id]
        
        if not pending_for_msg:
            # 2. Retrieve all completed packets for this message
            # logic: filter from scheduler.completed_packets
            completed_pkts = [p for p in self.scheduler.completed_packets if p.message_id == message_id]
            
            # Check if we actually have packets (to avoid empty completion on init or errors)
            if completed_pkts:
                # 3. Reassemble
                # reassemble_messages returns a dict {msg_id: text}
                results = self.reassembler.reassemble_messages(completed_pkts)
                text = results.get(message_id, "Error Reassembling")
                
                # 4. Display Result
                print(f"Message {message_id} Reassembled: {text}")
                messagebox.showinfo("Message Reassembled", f"Message ID: {message_id}\n\nReconstructed Text:\n{text}")
                
                # Optional: Mark message as 'Completed' in MessagePanel if we add a column update logic
                # self.update_message_status(message_id, "Completed") (Not implemented yet)


    # ... setup_ui and bind_events unchanged ...
    def setup_ui(self):
        # Left Container
        left_frame = tk.Frame(self.root)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        left_frame.grid_rowconfigure(0, weight=0) # Control
        left_frame.grid_rowconfigure(1, weight=1) # Message
        left_frame.grid_rowconfigure(2, weight=1) # Queue
        left_frame.grid_columnconfigure(0, weight=1)
        
        # Right Container
        right_frame = tk.Frame(self.root)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        right_frame.grid_rowconfigure(0, weight=2) # Animation
        right_frame.grid_rowconfigure(1, weight=1) # Metrics
        right_frame.grid_columnconfigure(0, weight=1)

        # Initialize Panels
        self.control_panel = ControlPanel(left_frame)
        self.control_panel.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        self.message_panel = MessagePanel(left_frame)
        self.message_panel.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        
        self.queue_panel = QueuePanel(left_frame)
        self.queue_panel.grid(row=2, column=0, sticky="nsew")
        
        self.animation_panel = AnimationPanel(right_frame)
        self.animation_panel.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        self.metrics_panel = MetricsPanel(right_frame)
        self.metrics_panel.grid(row=1, column=0, sticky="nsew")

    def bind_events(self):
        # Message Panel Events
        self.message_panel.add_btn.config(command=self.add_message)
        
        # Control Panel Events
        self.control_panel.start_btn.config(command=self.start_simulation)
        self.control_panel.pause_btn.config(command=self.pause_simulation)
        self.control_panel.reset_btn.config(command=self.reset_simulation)
        self.control_panel.step_btn.config(command=self.step_simulation)

    def add_message(self):
        text = self.message_panel.msg_entry.get()
        if not text:
            messagebox.showwarning("Input Error", "Please enter a message!")
            return
            
        # Add to backend
        msg, packets = self.data_manager.add_message(text)
        
        # Update Message Panel
        self.message_panel.tree.insert("", "end", values=(msg.message_id, msg.message_text, msg.status))
        self.message_panel.msg_entry.delete(0, "end")
        
        # Add packets to Queue and Animation
        for p in packets:
            self.scheduler.add_packet_to_queue(p)
            self.queue_panel.tree.insert("", "end", values=(p.packet_id, p.message_id, p.size, p.arrival_time, p.status))
            
            # Create Visual
            self.animator.create_packet(p)
            # Move to Queue Visual
            self.animator.move_to_queue(p.packet_id)

    def start_simulation(self):
        if not self.is_running:
            self.is_running = True
            self.run_simulation_step()

    def pause_simulation(self):
        self.is_running = False

    def reset_simulation(self):
        self.is_running = False
        # Clear backend
        self.data_manager.delete_all_data()
        self.pq = PriorityQueue()
        self.scheduler = SJFScheduler(self.pq)
        
        # Clear UI
        self.message_panel.tree.delete(*self.message_panel.tree.get_children())
        self.queue_panel.tree.delete(*self.queue_panel.tree.get_children())
        self.queue_panel.tree.delete(*self.queue_panel.tree.get_children())
        # Clear metrics
        self.metrics_panel.clear_metrics()
        
        # Reset Animation (Clear canvas)
        self.animation_panel.canvas.delete("all")
        self.animation_panel.draw_network_topology()
        self.animator = PacketAnimation(self.animation_panel.canvas)

    def step_simulation(self):
        # Run one step
        self.run_simulation_step(single_step=True)

    def run_simulation_step(self, single_step=False):
        if not self.is_running and not single_step:
            return
            
        # 1. Check if queue has packets
        if not self.scheduler.pq.is_empty():
            # Get next packet without popping (peek) to visualize selection
            packet = self.scheduler.pq.peek()
            
            # Visualize Selection
            self.animator.update_status(packet.packet_id, "SJF Selection")
            self.root.update() # Force redraw
            
            # Simulate Processing (Animation)
            self.animator.animate_transmission(packet.packet_id, duration_ms=500)
            
            # Commit processing
            processed_packet = self.scheduler.process_packet()
            if processed_packet:
                self.animator.complete(processed_packet.packet_id)
                # Update CSV Status
                self.data_manager.update_packet_status(processed_packet.packet_id, "Received")
            
            # Update Metrics
            results = self.scheduler.get_results()
            self.metrics_panel.update_metrics(results)
            
            # Update Queue Panel (Remove processed)
            # Find item in treeview matching packet_id
            for item in self.queue_panel.tree.get_children():
                vals = self.queue_panel.tree.item(item)['values']
                if vals[0] == processed_packet.packet_id:
                    self.queue_panel.tree.delete(item)
                    break
                    
        if self.is_running and not single_step:
            self.root.after(self.simulation_speed, self.run_simulation_step)

