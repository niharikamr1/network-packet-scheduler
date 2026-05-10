from scheduler.priority_queue import PriorityQueue
from scheduler.sjf_scheduler import SJFScheduler
from models.packet import Packet
from scheduler.metrics import Metrics

def test_sjf_scheduling():
    print("Testing SJF Scheduler...")
    
    pq = PriorityQueue()
    scheduler = SJFScheduler(pq)
    
    # Create test packets
    # P1: Size 10, Arrival 0
    # P2: Size 5, Arrival 1
    # P3: Size 5, Arrival 2
    # P4: Size 20, Arrival 3
    
    packets = [
        Packet("P1", "M1", "Data1", 10, 0),
        Packet("P2", "M1", "Data2", 5, 1),
        Packet("P3", "M1", "Data3", 5, 2),
        Packet("P4", "M1", "Data4", 20, 3)
    ]
    
    print("Adding packets to queue...")
    for p in packets:
        scheduler.add_packet_to_queue(p)
        print(f"Added {p.packet_id} (Size: {p.size}, Arrival: {p.arrival_time})")
        
    print("\nRunning Scheduler...")
    scheduler.run_scheduler()
    
    results = scheduler.get_results()
    log = results["execution_log"]
    
    print("\nExecution Order:")
    for entry in log:
        print(f"{entry['Packet_ID']} -> Start: {entry['Start_Time']}, End: {entry['End_Time']}")
        
    print("\nMetrics:")
    print(f"Avg Waiting Time: {results['avg_waiting_time']}")
    print(f"Avg Turnaround Time: {results['avg_turnaround_time']}")
    print(f"Throughput: {results['throughput']}")

    # Expected Order Analysis:
    # Time 0: P1 available. Executes 0-10.
    # Time 10: P2, P3, P4 available.
    # Sizes: P2=5, P3=5, P4=20.
    # P2 and P3 tied. P2 arrived first (1 < 2). P2 executes 10-15.
    # Time 15: P3, P4 available.
    # P3 executes 15-20.
    # Time 20: P4 executes 20-40.
    
    expected_order = ["P1", "P2", "P3", "P4"]
    actual_order = [entry['Packet_ID'] for entry in log]
    
    if actual_order == expected_order:
        print("\nSUCCESS: Execution order matches expected SJF logic.")
    else:
        print(f"\nFAILURE: Execution order mismatch. Expected {expected_order}, Got {actual_order}")

if __name__ == "__main__":
    test_sjf_scheduling()
