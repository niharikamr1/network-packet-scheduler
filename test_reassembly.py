from server.reassembly import Reassembly
from models.packet import Packet
import random

def test_reassembly():
    print("Testing Server Reassembly...")
    
    reassembler = Reassembly()
    
    # Create test packets for two messages
    # Message 1: "Hello World" -> "Hello " (0), "World" (1)
    p1_1 = Packet("P_M1_1", "M1", "Hello ", 6, 0)
    p1_2 = Packet("P_M1_2", "M1", "World", 5, 1)
    
    # Message 2: "Network Security" -> "Net" (0), "work " (1), "Sec" (2), "urity" (3)
    p2_1 = Packet("P_M2_1", "M2", "Net", 3, 0)
    p2_2 = Packet("P_M2_2", "M2", "work ", 5, 1)
    p2_3 = Packet("P_M2_3", "M2", "Sec", 3, 2)
    p2_4 = Packet("P_M2_4", "M2", "urity", 5, 3)
    
    # Combine and shuffle to simulate network disorder
    all_packets = [p1_1, p1_2, p2_1, p2_2, p2_3, p2_4]
    random.shuffle(all_packets)
    
    print(f"Input: {len(all_packets)} mixed packets.")
    
    # Reassemble
    results = reassembler.reassemble_messages(all_packets)
    
    print("\nResults:")
    for msg_id, text in results.items():
        print(f"{msg_id}: {text}")
        
    # Verification
    expected = {
        "M1": "Hello World",
        "M2": "Network Security"
    }
    
    success = True
    for msg_id, expected_text in expected.items():
        if results.get(msg_id) != expected_text:
            print(f"FAILURE for {msg_id}: Expected '{expected_text}', Got '{results.get(msg_id)}'")
            success = False
            
    if success:
        print("\nSUCCESS: All messages reassembled correctly.")

if __name__ == "__main__":
    test_reassembly()
