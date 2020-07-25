import os
import json
import sqlite3

class DatabaseManager():
    
    db = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'emailDb.db')
        
    def __init__(self):
        try:
            self.__conn = sqlite3.connect(self.db)
            self.__cur = self.__conn.cursor()
            self.__cur.execute("""CREATE TABLE IF NOT EXISTS Provider (
                            Id INTEGER PRIMARY KEY,
                            Name TEXT NOT NULL,
                            Extention TEXT NOT NULL
                    );""")
            self.__conn.commit()
            self.__cur.execute("""CREATE TABLE IF NOT EXISTS Sender (
                            Id INTEGER PRIMARY KEY,
                            ProviderId INTEGER NOT NULL,
                            Name TEXT NOT NULL,
                            Address TEXT NOT NULL
                    );""")
            self.__conn.commit()
            self.__cur.execute("""CREATE TABLE IF NOT EXISTS Email (
                            Id INTEGER PRIMARY KEY,
                            SenderId INTEGER NOT NULL,
                            Path TEXT,
                            Subject TEXT,
                            Content TEXT,
                            RecievedAt TIMESTAMP NOT NULL
                    );""")
            self.__conn.commit()
            self.__cur.execute("""CREATE TABLE IF NOT EXISTS EmailDetail (
                            Id INTEGER PRIMARY KEY,
                            EmailId INTEGER NOT NULL,
                            ProcessedAt TIMESTAMP NOT NULL
                    );""")
            self.__conn.commit()
        except Exception as e:
            print(e)

    def CloseConnection(self):
        self.__conn.close()

    def GetProvider(self, name):
        self.__cur.execute("""SELECT Id FROM Provider WHERE Name LIKE ?""", (name,))
        return [row[0] for row in self.__cur]
    
    def GetSender(self, name):
        self.__cur.execute("""SELECT Id FROM Sender WHERE Name LIKE ?""", (name,))
        return [row[0] for row in self.__cur]

    def SaveProvider(self, name, extention):
        self.__cur.execute("""INSERT INTO Provider VALUES (?,?)""", (name, extention))
        self.__conn.commit()

    def SaveSender(self, proId, name, address):
        self.__cur.execute("""INSERT INTO Sender VALUES (?,?,?)""", (proId, name, address))
        self.__conn.commit()

    def SaveEmail(self, sendId, path, subject, content, recievedAt):
        self.__cur.execute("""INSERT INTO Email VALUES (?,?,?,?,?)""", (sendId, path, subject, content, recievedAt))
        self.__conn.commit()
    
    def SaveEmailDetail(self, emailId, processedAt):
        self.__cur.execute("""INSERT INTO EmailDetail VALUES (?,?)""", (emailId, processedAt))
        self.__conn.commit()

    def FetchEmail(self):
        self.__cur.execute("""SELECT * FROM Email""")
        return [row for row in self.__cur]
        