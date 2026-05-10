from storage.data_manager import DataManager
import pandas as pd
import os

def test_segmentation():
    print("Testing Packet Segmentation...")
    
    # Initialize DataManager
    dm = DataManager()
    
    # Clear previous data
    dm.delete_all_data()
    
    # Add a test message
    test_msg = "Hello World, this is a test message for segmentation."
    print(f"Adding message: '{test_msg}'")
    
    message, packets = dm.add_message(test_msg)
    
    print(f"Message ID: {message.message_id}")
    print(f"Generated {len(packets)} packets.")
    
    # Verify Packets
    print("\nGenerated Packets:")
    for p in packets:
        print(f"ID: {p.packet_id}, Data: '{p.data}', Size: {p.size}, Arrival: {p.arrival_time}")
        
    # Verify CSV Content
    print("\nVerifying CSV Content:")
    saved_packets = dm.get_packets()
    print(saved_packets)
    
    if len(saved_packets) == len(packets):
        print("\nSUCCESS: Packets saved correctly.")
    else:
        print("\nFAILURE: Packet count mismatch in CSV.")

if __name__ == "__main__":
    test_segmentation()
