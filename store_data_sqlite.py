import pandas as pd
import sqlite3


csv_file = "energy_dataset.csv"  # Ensure this file exists
df = pd.read_csv(csv_file)


conn = sqlite3.connect("energy_data.db")
cursor = conn.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS energy_usage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        energy_consumption REAL
    )
""")


df.to_sql("energy_usage", conn, if_exists="replace", index=False)


print("\n✅ Data Successfully Stored in SQLite Database!")
print("\n🔹 First 5 Rows from Database:")
print(pd.read_sql("SELECT * FROM energy_usage LIMIT 5", conn))


conn.close()
