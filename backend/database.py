 
from sqlalchemy import create_engine
import sqlite3
from pathlib import Path

LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

def connect_database(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri == LOCALDB:
        dbfilepath = (Path(__file__).parent / "student.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return create_engine("sqlite:///", creator=creator)
    
    elif db_uri == MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            raise ValueError("MySQL credentials missing!")
        return create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}")
