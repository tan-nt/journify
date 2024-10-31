import json
import sqlite3
import os

json_file_path = "database/arxiv-metadata-oai-snapshot.json"  # Replace with your JSON file path
sqlite_db_path = "database/arxiv-metadata-oai-snapshot.db"    # Replace with your desired database path

def json_to_sqlite(json_file_path='', sqlite_db_path='', table_name='article', max_read_line=10):
    with open(json_file_path, 'r') as f:
        data = [json.loads(line.strip()) for _, line in zip(range(max_read_line), f)]
        
    print('max_read_line=', max_read_line)
    
    if not data:
        raise Exception(f"{json_file_path} data path is epty")
    
    if data:
        conn = sqlite3.connect(sqlite_db_path)
        cursor = conn.cursor()

        columns = ", ".join(f"[{key}] TEXT" for key in data[0].keys())
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")

        for record in data:
            values = tuple(str(value) if value is not None else "" for value in record.values())
            placeholders = ", ".join("?" for _ in values)
            cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", values)

        conn.commit()
        conn.close()
        print(f"JSON data has been successfully converted to SQLite database. {len(data)} rows is inserted in the SQLite DB")

def init_data():
    if os.path.exists(json_file_path):
        json_to_sqlite(json_file_path, sqlite_db_path, 'article', 1000)
    else:
        print(f"JSON file not found at {json_file_path}.")
        
def query_all_data():
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM article LIMIT 10")  
    results = cursor.fetchall()
    res = [print(row) for row in results]
    conn.close()
    return res
