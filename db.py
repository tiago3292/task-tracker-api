import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "tasks.db")

def db_connect():
	conn = sqlite3.connect("tasks.db")
	conn.row_factory = sqlite3.Row
	return conn

def init_db():
	conn = db_connect()
	cursor = conn.cursor()

	cursor.execute("""
		CREATE TABLE IF NOT EXISTS tasks (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			task TEXT NOT NULL,
			done BOOLEAN NOT NULL CHECK (Done IN (0, 1)) DEFAULT 0
		)
	""")

	conn.commit()
	conn.close()