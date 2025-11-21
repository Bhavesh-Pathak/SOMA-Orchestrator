import sqlite3
import json
from datetime import datetime

class Memory:
    def __init__(self, db_path='memory.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        input TEXT,
                        results TEXT,
                        trace TEXT
                     )''')
        conn.commit()
        conn.close()

    def save_session(self, input_text, results, trace):
        timestamp = datetime.now().isoformat()
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO sessions (timestamp, input, results, trace) VALUES (?, ?, ?, ?)",
                  (timestamp, input_text, json.dumps(results), json.dumps(trace)))
        conn.commit()
        conn.close()