from sqlalchemy import create_engine
import logging

logging.basicConfig(level=logging.INFO)


def reset_last_scratch(db_name: str, table_name: str, connection_string: str):
    engine = create_engine(connection_string)
    conn = engine.connect()
    
    query_update = f'''UPDATE {table_name} SET active='False' WHERE active='True';'''
    conn.execute(query_update)
    conn.close()

    logging.info(f"Reset status last get API postgres database:'{db_name}', table:'{table_name}'...")