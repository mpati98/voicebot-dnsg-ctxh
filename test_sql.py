import sqlite3
import pandas as pd

con = sqlite3.connect("apps/db.sqlite3")
df = pd.read_sql_query("SELECT * from Events", con)
df = df.drop(['oauth_github'], axis=1)
print(df.head())
print(df.eventName.values[-1])