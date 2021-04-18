# --- import libraries 
import sqlite3
import datetime
import pandas as pd
import numpy as np
from database import create_tables

# create connection
conn = sqlite3.connect("./data.db")

df = pd.read_csv('gapminder_clean.csv', index_col=[0])

print(df.columns)
create_tables()
df.to_sql('gapminder', conn, if_exists='append', index=False)