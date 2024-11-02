import sqlite3
from datetime import datetime

class User:
    def __init__(self):
        self.db_path = "database/user.db"
        self.table_name = "user_log"
        self._initialize_user_table()

    def _connect(self):
        """Establish a connection to the SQLite database."""
        return sqlite3.connect(self.db_path)

    def _initialize_user_table(self):
        """Initialize the user table with predefined columns if it doesn't exist."""
        user_columns = {
            "ip_address": "TEXT PRIMARY KEY",
            "access_time": "TEXT",
            "accessed_article_id": "TEXT",
            "user_agent": "TEXT"  # For additional info like browser and OS
        }
        with self._connect() as conn:
            cursor = conn.cursor()
            col_defs = ", ".join([f"[{col}] {dtype}" for col, dtype in user_columns.items()])
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({col_defs})")
            conn.commit()

    def upsert_user_access(self, ip_address, user_agent):
        """Insert or update a record of user access in the user table based on IP address."""
        access_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._connect() as conn:
            cursor = conn.cursor()
            # Use INSERT OR REPLACE to perform the upsert
            query = f"""
                INSERT INTO {self.table_name} (ip_address, access_time, user_agent)
                VALUES (?, ?, ?)
                ON CONFLICT(ip_address) DO UPDATE SET
                    access_time=excluded.access_time,
                    user_agent=excluded.user_agent
            """
            cursor.execute(query, (ip_address, access_time, user_agent))
            conn.commit()
            
    def read_user_access(self, limit=0):
        """Fetch user access from the table.
        
        Args:
            limit (int): The number of records to fetch.
            
        Returns:
            list: A list of dictionaries with column names as keys and row values.
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            if not limit:
                cursor.execute(f"SELECT * FROM {self.table_name}")
            else:
                cursor.execute(f"SELECT * FROM {self.table_name} LIMIT {limit}")
            results = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            return [dict(zip(column_names, row)) for row in results]
        
    def read_random_ip_addresses(self, limit=0):
        """Fetch random IP addresses from the table.
        
        Args:
            limit (int): The number of records to fetch.
            
        Returns:
            list: A list of IP addresses.
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            
            # Select only the ip_address column and order by random
            if not limit:
                cursor.execute(f"SELECT ip_address FROM {self.table_name} ORDER BY RANDOM()")
            else:
                cursor.execute(f"SELECT ip_address FROM {self.table_name} ORDER BY RANDOM() LIMIT {limit}")
            
            # Fetch all results
            results = cursor.fetchall()
            
            # Extract only the IP addresses from the results
            return [row[0] for row in results]

user_model = User()