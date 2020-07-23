import os
import json
import sqlite3

class DatabaseManager():
    
    db = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'emailDb.db')

    def __init__(self):
        try:
            conn = sqlite3.connect(self.db)
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS Provider (
                            Id INTEGER PRIMARY KEY,
                            Name TEXT NOT NULL,
                            Extention TEXT NOT NULL
                    );""")
            conn.commit()
            cur.execute("""CREATE TABLE IF NOT EXISTS Sender (
                            Id INTEGER PRIMARY KEY,
                            ProviderId INTEGER NOT NULL,
                            Name TEXT NOT NULL,
                            Address TEXT NOT NULL
                    );""")
            conn.commit()
            cur.execute("""CREATE TABLE IF NOT EXISTS Email (
                            Id INTEGER PRIMARY KEY,
                            SenderId INTEGER NOT NULL,
                            Path TEXT,
                            Subject TEXT,
                            Content TEXT,
                            RecievedAt TIMESTAMP NOT NULL
                    );""")
            conn.commit()
            cur.execute("""CREATE TABLE IF NOT EXISTS EmailDetails (
                            Id INTEGER PRIMARY KEY,
                            EmailId INTEGER NOT NULL,
                            ProcessedAt TIMESTAMP NOT NULL
                    );""")
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)

