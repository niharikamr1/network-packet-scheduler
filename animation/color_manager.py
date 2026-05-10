class ColorManager:
    COLORS = {
        "Packet Creation": "#2196F3", # Blue
        "Queue Waiting": "#FFEB3B",   # Yellow
        "SJF Selection": "#FF9800",   # Orange
        "VPN Transmission": "#9C27B0",# Purple
        "Packet Received": "#4CAF50", # Green
        "Text": "black"
    }

    @staticmethod
    def get_color(status):
        return ColorManager.COLORS.get(status, "gray")
