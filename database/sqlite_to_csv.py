from database.json_to_sqlite import query_all_data
import pandas as pd

csv_file_path = "database/arxiv_data.csv"  # Desired CSV file path

def export_to_csv(csv_file_path=csv_file_path):
    df = pd.DataFrame(query_all_data())
    df.to_csv(csv_file_path, index=False)
    print(f"Data successfully exported to {csv_file_path}")

