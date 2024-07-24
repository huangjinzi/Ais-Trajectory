from sqlalchemy import create_engine
import pandas as pd
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

def get_db_connection():
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    return engine

def fetch_ais_data():
    query = """
    SELECT create_time, mmsi, lon, lat, sog, cog
    FROM sws_ais_data 
    WHERE create_time::date = '2022-10-21'
    --AND mmsi = '413845356'
    """
    engine = get_db_connection()
    df = pd.read_sql(query, engine)
    return df
