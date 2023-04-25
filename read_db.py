import sqlite3
import pandas as pd


# Create a SQL connection to our SQLite database
con = sqlite3.connect("apps/db.sqlite3")

df = pd.read_sql_query("SELECT * from Users", con)

# Be sure to close the connection
con.close()
