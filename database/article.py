import sqlite3

class Article:
    def __init__(self):
        self.db_path = "database/arxiv-metadata-oai-snapshot.db"
        self.table_name = "article"
        self._initialize_table()

    def _connect(self):
        """Establish a connection to the SQLite database."""
        return sqlite3.connect(self.db_path)

    def _initialize_table(self):
        """Initialize the article table with predefined columns if it doesn't exist."""
        columns = {
            "id": "TEXT PRIMARY KEY",
            "submitter": "TEXT",
            "authors": "TEXT",
            "title": "TEXT",
            "comments": "TEXT",
            "journal_ref": "TEXT",
            "doi": "TEXT",
            "report_no": "TEXT",
            "categories": "TEXT",
            "license": "TEXT",
            "abstract": "TEXT",
            "versions": "TEXT",
            "update_date": "TEXT",
            "authors_parsed": "TEXT"
        }

        with self._connect() as conn:
            cursor = conn.cursor()
            col_defs = ", ".join([f"[{col}] {dtype}" for col, dtype in columns.items()])
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({col_defs})")
            conn.commit()

    def insert_article(self, article_data):
        """Insert a single article record into the table.
        
        Args:
            article_data (dict): A dictionary containing article details.
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            columns = ", ".join(article_data.keys())
            placeholders = ", ".join("?" for _ in article_data)
            query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, tuple(article_data.values()))
            conn.commit()

    def read_articles(self, limit=0):
        """Fetch articles from the table.
        
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

    def update_article(self, updates, condition):
        """Update records in the article table based on a condition.
        
        Args:
            updates (dict): Columns and their new values, e.g., {"title": "new_title"}.
            condition (str): The condition for updating records, e.g., "id = 1".
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            set_clause = ", ".join([f"{col} = ?" for col in updates.keys()])
            query = f"UPDATE {self.table_name} SET {set_clause} WHERE {condition}"
            cursor.execute(query, tuple(updates.values()))
            conn.commit()

    def delete_article(self, condition):
        """Delete records from the article table based on a condition.
        
        Args:
            condition (str): The condition for deleting records, e.g., "id = 1".
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {self.table_name} WHERE {condition}")
            conn.commit()

article = Article()