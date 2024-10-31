import json
import sqlite3
import re, os

json_file_path = "database/arxiv-metadata-oai-snapshot.json"  # Replace with your JSON file path
sqlite_db_path = "database/arxiv-metadata-oai-snapshot.db"    # Replace with your desired database path

def clean_value(value):
    """Clean and normalize individual data values for SQLite."""
    if value is None:
        return ""
    if isinstance(value, str):
        # Remove newline characters and extra whitespace
        value = value.replace("\n", " ").strip()
        # Escape any remaining problematic characters
        value = re.sub(r"[^a-zA-Z0-9\s.,:_-]", "", value)
    else:
        # Serialize complex types (e.g., lists or dicts) to JSON strings
        value = json.dumps(value)
    return str(value)

def json_to_sqlite(json_file_path, sqlite_db_path, table_name='article', max_read_line=10):
    data = []
    with open(json_file_path, 'r') as f:
        for _, line in zip(range(max_read_line), f):
            record = json.loads(line.strip())
            # Clean and serialize each field
            cleaned_record = {key: clean_value(value) for key, value in record.items()}
            data.append(cleaned_record)
    
    if not data:
        raise Exception(f"{json_file_path} data path is empty")
    
    # Connect to SQLite database and create the table if it doesn't exist
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()

    # Define table columns based on JSON keys, with all columns set to TEXT
    columns = ", ".join(f"[{key}] TEXT" for key in data[0].keys())
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")

    # Insert each record from cleaned JSON data into the table
    for record in data:
        values = tuple(record.values())  # Values are already cleaned
        placeholders = ", ".join("?" for _ in values)

        # Debug SQL statement for logging
        sql_statement = f"INSERT INTO {table_name} VALUES ({placeholders})"
        sql_with_values = sql_statement.replace("?", "{}").format(*[repr(value) for value in values])
        try:
            cursor.execute(sql_statement, values)
        except sqlite3.IntegrityError as e:
            print(f"Error inserting record: {sql_with_values}\nError: {e}")
            continue  # Skip problematic rows

    conn.commit()
    conn.close()
    print(f"JSON data has been successfully converted to SQLite database. {len(data)} rows inserted.")

def init_data():
    if os.path.exists(json_file_path):
        json_to_sqlite(json_file_path, sqlite_db_path, 'article', int(os.environ.get("ARTCILE_DATA_LINE") or "1000"))
    else:
        print(f"JSON file not found at {json_file_path}.")
        
def query_all_data(limit=0):
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()
    if not limit:
        cursor.execute("SELECT * FROM article")  
    else:
        cursor.execute("SELECT * FROM article LIMIT 10")  
    results = cursor.fetchall()
    conn.close()
    return results
