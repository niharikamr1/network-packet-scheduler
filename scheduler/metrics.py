class Metrics:
    def __init__(self):
        self.waiting_times = {}
        self.turnaround_times = {}
        self.completion_times = {}
        self.total_packets = 0
        self.total_time = 0

    def record_completion(self, packet, current_time):
        self.completion_times[packet.packet_id] = current_time
        
        # Turnaround Time = Completion Time - Arrival Time
        turnaround = current_time - packet.arrival_time
        self.turnaround_times[packet.packet_id] = turnaround
        
        # Waiting Time = Turnaround Time - Burst Time (Size/Service Time)
        # Assuming Service Time = Packet Size for simulation simplicity
        waiting = turnaround - packet.size
        self.waiting_times[packet.packet_id] = max(0, waiting)
        
        self.total_packets += 1
        self.total_time = max(self.total_time, current_time)

    def get_average_waiting_time(self):
        if not self.waiting_times: return 0
        return sum(self.waiting_times.values()) / len(self.waiting_times)

    def get_average_turnaround_time(self):
        if not self.turnaround_times: return 0
        return sum(self.turnaround_times.values()) / len(self.turnaround_times)

    def get_throughput(self):
        # Throughput = Total Packets / Total Time
        if self.total_time == 0: return 0
        return self.total_packets / self.total_time

