
import os
from dotenv import load_dotenv
from database.json_to_sqlite import init_data
from database.sqlite_to_csv import export_to_csv

def load_env_variables():
    if os.path.exists('.env'):
        load_dotenv('.env')
