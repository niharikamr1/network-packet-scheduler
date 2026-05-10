import pandas as pd
import os

class CSVHandler:
    def __init__(self, file_path, headers):
        self.file_path = file_path
        self.headers = headers
        if not os.path.exists(file_path):
            df = pd.DataFrame(columns=headers)
            df.to_csv(file_path, index=False)

    def read_csv(self):
        try:
            return pd.read_csv(self.file_path)
        except Exception as e:
            print(f"Error reading {self.file_path}: {e}")
            return pd.DataFrame(columns=self.headers)

    def write_csv(self, df):
        try:
            df.to_csv(self.file_path, index=False)
        except Exception as e:
            print(f"Error writing to {self.file_path}: {e}")
            
    def append_data(self, new_data_dict):
        df = self.read_csv()
        new_row = pd.DataFrame([new_data_dict])
        df = pd.concat([df, new_row], ignore_index=True)
        self.write_csv(df)

