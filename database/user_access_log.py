import sqlite3
from datetime import datetime

class UserAccessLogger:
    def __init__(self, db_path="database/user_access_log.db"):
        self.db_path = db_path
        self.table_name = "user_access_log"
        self._initialize_table()

    def _connect(self):
        """Establish a connection to the SQLite database."""
        return sqlite3.connect(self.db_path)

    def _initialize_table(self):
        """Initialize the user access log table."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    ip_address TEXT,
                    article_id TEXT,
                    title TEXT,
                    abstract TEXT,
                    influential_citation_count TEXT,
                    action_type TEXT,
                    search_query TEXT,
                    timestamp TEXT
                )
            """)
            conn.commit()

    def log_action(self, ip_address, action_type, article_id=None, title=None, abstract=None,
                   influential_citation_count=None, search_query=None):
        """Insert a record of user action into the table."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = (ip_address, article_id, title, abstract, influential_citation_count, action_type, search_query, timestamp)

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO {self.table_name} 
                (ip_address, article_id, title, abstract, influential_citation_count, action_type, search_query, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
            conn.commit()
            
    def list_user_access_log(self, limit=0):
        """Fetch user access log from the table.
        
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

# Initialize logger
user_access_logger_model = UserAccessLogger()
