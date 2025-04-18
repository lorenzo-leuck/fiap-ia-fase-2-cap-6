import os
import sqlite3
from db import DatabaseManager

if os.path.exists("db.sqlite"):
    os.remove("db.sqlite")
    print("Banco de dados existente removido para teste limpo")

db_manager = DatabaseManager()

conn = sqlite3.connect("farmtech_solutions.sqlite")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print(f"Tabelas criadas no banco de dados:")
for table in tables:
    print(f"- {table[0]}")

conn.close()
