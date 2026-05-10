class Packet:
    def __init__(self, packet_id, message_id, data, size, arrival_time, status="Waiting"):
        self.packet_id = packet_id
        self.message_id = message_id
        self.data = data
        self.size = size
        self.arrival_time = arrival_time
        self.status = status

    def to_dict(self):
        return {
            "Packet_ID": self.packet_id,
            "Message_ID": self.message_id,
            "Data": self.data,
            "Size": self.size,
            "Arrival_Time": self.arrival_time,
            "Status": self.status
        }
