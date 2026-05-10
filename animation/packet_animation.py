from animation.color_manager import ColorManager

class PacketAnimation:
    def __init__(self, canvas):
        self.canvas = canvas
        self.packet_objects = {} # Map packet_id -> canvas_tag
        
        # Coordinates
        self.start_x = 100
        self.start_y = 150
        self.end_x = 700
        self.end_y = 150
        self.queue_x = 100
        self.queue_y = 250

    def create_packet(self, packet):
        # Draw a rectangle representing the packet (Box)
        tag = f"pkt_{packet.packet_id}"
        color = ColorManager.get_color("Packet Creation")
        
        # Fixed Box Size for better visibility of text
        width = 40
        height = 30
        
        # Start at Client Node
        x, y = self.start_x, self.start_y
        
        item_id = self.canvas.create_rectangle(
            x - width/2, y - height/2, x + width/2, y + height/2,
            fill=color, outline="black", tags=tag
        )
        
        # Label: ID\nSize
        label_text = f"{packet.packet_id}\nS:{packet.size}"
        text_id = self.canvas.create_text(x, y, text=label_text, tags=tag, font=("Arial", 7, "bold"))
        
        self.packet_objects[packet.packet_id] = {
            "item": item_id,
            "text": text_id,
            "x": x,
            "y": y,
            "width": width, 
            "height": height
        }

    def move_to_queue(self, packet_id):
        # Move visual to queue area
        if packet_id not in self.packet_objects: return
        
        obj = self.packet_objects[packet_id]
        
        # Simple spacing in queue
        queue_offset = len(self.packet_objects) * 25 % 300 # Rough visual stacking
        target_x = 70 + queue_offset
        target_y = self.queue_y
        
        self.animate_move(packet_id, target_x, target_y, "Queue Waiting")

    def place_in_queue(self, packet_id):
        # Instant move (for initial load)
        if packet_id not in self.packet_objects: return
        obj = self.packet_objects[packet_id]
        
        queue_offset = len(self.packet_objects) * 25 % 300 
        target_x = 70 + queue_offset
        target_y = self.queue_y
        
        # Update Coords
        dx = target_x - obj["x"]
        dy = target_y - obj["y"]
        
        self.canvas.move(obj["item"], dx, dy)
        self.canvas.move(obj["text"], dx, dy)
        
        obj["x"] = target_x
        obj["y"] = target_y
        self.update_status(packet_id, "Queue Waiting")

    def animate_transmission(self, packet_id, duration_ms):
        # Move from Queue/Start to End (Server)
        if packet_id not in self.packet_objects: return
        
        # 1. Move to start of Tunnel (if not there)
        # self.animate_move(packet_id, 150, 150, "SJF Selection")
        
        # 2. Animate across tunnel
        self.animate_move(packet_id, self.end_x, self.end_y, "VPN Transmission", steps=50)

    def update_status(self, packet_id, status):
        if packet_id not in self.packet_objects: return
        obj = self.packet_objects[packet_id]
        color = ColorManager.get_color(status)
        self.canvas.itemconfig(obj["item"], fill=color)

    def animate_move(self, packet_id, target_x, target_y, status_during_move, steps=50):
        if packet_id not in self.packet_objects: return
        obj = self.packet_objects[packet_id]
        
        current_x, current_y = obj["x"], obj["y"]
        dx = (target_x - current_x) / steps
        dy = (target_y - current_y) / steps
        
        self.update_status(packet_id, status_during_move)
        
        import time
        for _ in range(steps):
            self.canvas.move(obj["item"], dx, dy)
            self.canvas.move(obj["text"], dx, dy)
            self.canvas.update() # Force redraw
            time.sleep(0.02) # 20ms per step -> 1 second total for 50 steps
        
        obj["x"] = target_x
        obj["y"] = target_y
        
    def complete(self, packet_id):
        self.update_status(packet_id, "Packet Received")

