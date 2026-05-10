from scheduler.metrics import Metrics

class SJFScheduler:
    def __init__(self, priority_queue):
        self.pq = priority_queue
        self.metrics = Metrics()
        self.current_time = 0
        self.execution_log = [] # List of (Packet, StartTime, EndTime)
        self.completed_packets = [] # List of Packet objects for reassembly

    def add_packet_to_queue(self, packet):
        self.pq.push(packet)

    def run_scheduler(self):
        """
        Simulates the processing of all packets in the priority queue.
        """
        while not self.pq.is_empty():
            self.process_packet()

    def process_packet(self):
        if self.pq.is_empty():
            return None
            
        packet = self.pq.pop()
        
        # Simulate processing
        # If the system was idle, jump to packet arrival
        start_time = max(self.current_time, packet.arrival_time)
        
        # Processing time = Packet Size
        burst_time = packet.size
        end_time = start_time + burst_time
        
        # Update system time
        self.current_time = end_time
        
        # Update packet status
        packet.status = "Received"
        
        # Record metrics
        self.metrics.record_completion(packet, end_time)
        
        # Log execution
        self.execution_log.append({
            "Packet_ID": packet.packet_id,
            "Start_Time": start_time,
            "End_Time": end_time,
            "Size": packet.size
        })
        
        self.completed_packets.append(packet)
        return packet
            
    def get_results(self):
        return {
            "avg_waiting_time": self.metrics.get_average_waiting_time(),
            "avg_turnaround_time": self.metrics.get_average_turnaround_time(),
            "throughput": self.metrics.get_throughput(),
            "execution_log": self.execution_log
        }
