from models.packet import Packet

class PacketSegmenter:
    def __init__(self, chunk_size=5): # Reduced chunk size for better visualization
        self.chunk_size = chunk_size

    def segment_message(self, message):
        text = message.message_text
        packets = []
        total_packets = (len(text) + self.chunk_size - 1) // self.chunk_size
        
        for i in range(total_packets):
            start = i * self.chunk_size
            end = min(start + self.chunk_size, len(text))
            chunk = text[start:end]
            
            packet_id = f"P{message.message_id}_{i+1}"
            size = len(chunk)
            arrival_time = i  # Simulating sequential arrival
            
            packet = Packet(
                packet_id=packet_id,
                message_id=message.message_id,
                data=chunk,
                size=size,
                arrival_time=arrival_time,
                status="Waiting"
            )
            packets.append(packet)
            
        return packets
