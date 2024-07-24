from sqlalchemy import create_engine, inspect
import pandas as pd

engine = create_engine('postgresql://postgres:huangl@localhost:5432/sz-sws')

# query = "SELECT * FROM accident LIMIT 5;"

# 定义 SQL 查询
query = """
    SELECT create_time, mmsi, lon, lat, sog, cog
    FROM sws_ais_data 
    WHERE create_time::date = '2022-10-21'
    AND mmsi = '413845356'
"""

df = pd.read_sql(query, engine)

print(df)
