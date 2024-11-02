
import os
from dotenv import load_dotenv

def load_env_variables():
    if os.path.exists('.env'):
        load_dotenv('.env')
