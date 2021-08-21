from sqlalchemy import create_engine
from datetime import datetime
import logging
import requests

logging.basicConfig(level=logging.INFO)


def update_new_data(api_url: str, db_name: str, table_name: str, connection_string: str):
    response = requests.get(api_url)
    if response.status_code == 200:
        json = response.json()
    else:
        return None
    
    covid_data = json['update']['harian']
    
    engine = create_engine(connection_string)
    conn = engine.connect()
    
    query_select_lastscrapingid = f'''SELECT max(id) FROM last_scratch;'''
    get_scraping_id = conn.execute(query_select_lastscrapingid)
    scraping_id = list(get_scraping_id)[0][0]
    
    query_select = f'''SELECT id FROM {table_name};'''
    get_id = conn.execute(query_select)
    list_id = [id[0] for id in get_id]
    
    for data in covid_data:
        if data['key'] not in list_id:
            list_id.append(data['key'])
            
            id = data['key']
            date = datetime.fromisoformat(data['key_as_string'][:-1]).strftime('%Y-%m-%d %H:%M:%S')
            cases = data['jumlah_positif']['value']
            recover = data['jumlah_sembuh']['value']
            recovery = data['jumlah_dirawat']['value']
            death = data['jumlah_meninggal']['value']
            cases_cum = data['jumlah_positif_kum']['value']
            recover_cum = data['jumlah_sembuh_kum']['value']
            recovery_cum = data['jumlah_dirawat_kum']['value']
            death_cum = data['jumlah_meninggal_kum']['value']
            
            query_insert = f'''INSERT INTO {table_name} VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
            value = (id, date, death, recover, cases, recovery, death_cum, recover_cum, cases_cum, recovery_cum, scraping_id)  
            conn.execute(query_insert, value)
            
    conn.close()
    logging.info(f"Update new data covid from API to postgres database:'{db_name}', table:'{table_name}'...")