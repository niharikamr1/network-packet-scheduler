import heapq

class PriorityQueue:
    def __init__(self):
        self.queue = []
        self.counter = 0 # Unique sequence count to break ties if arrival times are identical

    def push(self, packet):
        # Priority Tuple: (Packet Size, Arrival Time, Sequence, Packet Object)
        # Python's heapq is a min-heap, so smaller size comes first.
        # If sizes are equal, smaller arrival time comes first (FCFS).
        # We add a counter to ensure stable sorting if arrival times are also identical.
        entry = (packet.size, packet.arrival_time, self.counter, packet)
        heapq.heappush(self.queue, entry)
        self.counter += 1

    def pop(self):
        if not self.is_empty():
            # Return the packet object (4th element in tuple)
            return heapq.heappop(self.queue)[3]
        return None

    def is_empty(self):
        return len(self.queue) == 0

    def peek(self):
        if not self.is_empty():
            return self.queue[0][3]
        return None
    
    def get_all_packets(self):
        # Return a list of packets currently in queue (unsorted/heap order)
        return [entry[3] for entry in self.queue]

