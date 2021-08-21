from sqlalchemy import create_engine
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)


def get_new_update(db_name: str, table_name: str, connection_string: str):
    engine = create_engine(connection_string)
    conn = engine.connect()
    
    last_get = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    active = 'True'
    value = (last_get, active)
    
    query_insert = f'''INSERT INTO {table_name} (last_get,active) VALUES (%s, %s);'''
    conn.execute(query_insert, value)
    conn.close()

    logging.info(f"Update new status last get API postgres database:'{db_name}', table:'{table_name}'...")