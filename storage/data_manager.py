import pandas as pd
from storage.csv_handler import CSVHandler
from models.message import Message
from segmentation.packet_segmenter import PacketSegmenter
from utils.constants import CSV_MESSAGES_PATH, CSV_PACKETS_PATH
from utils.helpers import generate_id

class DataManager:
    def __init__(self):
        self.msg_handler = CSVHandler(CSV_MESSAGES_PATH, ["Message_ID", "Message_Text", "Status"])
        self.pkt_handler = CSVHandler(CSV_PACKETS_PATH, ["Packet_ID", "Message_ID", "Data", "Size", "Arrival_Time", "Status"])
        self.segmenter = PacketSegmenter()

    def add_message(self, text):
        # 1. Generate Message ID
        existing_msgs = self.msg_handler.read_csv()
        new_id = f"M{len(existing_msgs) + 1}"
        
        # 2. Create Message Object
        message = Message(new_id, text)
        
        # 3. Save Message
        self.msg_handler.append_data(message.to_dict())
        
        # 4. Segment into Packets
        packets = self.segmenter.segment_message(message)
        
        # 5. Save Packets
        for packet in packets:
            self.pkt_handler.append_data(packet.to_dict())
            
        return message, packets

    def get_packets(self):
        return self.pkt_handler.read_csv()

    def delete_all_data(self):
        # Clear CSVs for reset
        pd.DataFrame(columns=self.msg_handler.headers).to_csv(self.msg_handler.file_path, index=False)
        pd.DataFrame(columns=self.pkt_handler.headers).to_csv(self.pkt_handler.file_path, index=False)

    def get_all_messages(self):
        # Convert dicts from CSV to Message objects
        df = self.msg_handler.read_csv()
        data = df.to_dict('records')
        return [Message(d['Message_ID'], d['Message_Text'], d['Status']) for d in data]

    def get_all_packets(self):
        # Convert dicts from CSV to Packet objects
        from models.packet import Packet
        df = self.pkt_handler.read_csv()
        data = df.to_dict('records')
        packets = []
        for d in data:
            try:
                p = Packet(
                    d['Packet_ID'], 
                    d['Message_ID'], 
                    d['Data'], 
                    int(d['Size']), 
                    int(d['Arrival_Time']), 
                    d['Status']
                )
                packets.append(p)
            except ValueError:
                continue # Skip malformed rows
                continue # Skip malformed rows
        return packets

    def update_packet_status(self, packet_id, new_status):
        """Updates the status of a specific packet in the CSV."""
        df = self.pkt_handler.read_csv()
        if 'Packet_ID' in df.columns:
            # Find row index where Packet_ID matches
            mask = df['Packet_ID'] == packet_id
            if mask.any():
                df.loc[mask, 'Status'] = new_status
                self.pkt_handler.write_csv(df)

