class Message:
    def __init__(self, message_id, message_text, status="Pending"):
        self.message_id = message_id
        self.message_text = message_text
        self.status = status

    def to_dict(self):
        return {
            "Message_ID": self.message_id,
            "Message_Text": self.message_text,
            "Status": self.status
        }
