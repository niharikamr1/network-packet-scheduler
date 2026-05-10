from collections import defaultdict

class Reassembly:
    def __init__(self):
        pass
    
    def reassemble_messages(self, packets):
        """
        Reassembles messages from a list of Packet objects.
        Returns a dictionary: {Message_ID: Reconstructed_Text}
        """
        message_packets = defaultdict(list)
        
        # Group packets by Message ID
        for packet in packets:
            message_packets[packet.message_id].append(packet)
            
        reconstructed_messages = {}
        
        for msg_id, pkt_list in message_packets.items():
            # Sort by Arrival Time (which acts as sequence number from Segmenter)
            # Ensure we use int() if necessary, but Packet.arrival_time should be int
            pkt_list.sort(key=lambda p: p.arrival_time)
            
            # Concatenate data
            full_text = "".join([p.data for p in pkt_list])
            reconstructed_messages[msg_id] = full_text
            
        return reconstructed_messages
