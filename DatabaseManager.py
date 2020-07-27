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
                            Id INTEGER PRIMARY KEY AUTOINCREMENT,
                            Name TEXT NOT NULL,
                            Extention TEXT NOT NULL
                    );""")
            self.__conn.commit()
            self.__cur.execute("""CREATE TABLE IF NOT EXISTS Sender (
                            Id INTEGER PRIMARY KEY AUTOINCREMENT,
                            ProviderId INTEGER NOT NULL,
                            Name TEXT NOT NULL,
                            Address TEXT NOT NULL
                    );""")
            self.__conn.commit()
            self.__cur.execute("""CREATE TABLE IF NOT EXISTS Email (
                            Id INTEGER PRIMARY KEY AUTOINCREMENT,
                            SenderId INTEGER NOT NULL,
                            EmailIndex INTEGER,
                            Path TEXT,
                            Subject TEXT,
                            RecievedAt TIMESTAMP NOT NULL
                    );""")
            self.__conn.commit()
            self.__cur.execute("""CREATE TABLE IF NOT EXISTS EmailDetail (
                            Id INTEGER PRIMARY KEY AUTOINCREMENT,
                            EmailId INTEGER NOT NULL,
                            ProcessedAt TIMESTAMP NOT NULL
                    );""")
            self.__conn.commit()
            self.__cur.execute("""CREATE TABLE IF NOT EXISTS Variable (
                            Id INTEGER PRIMARY KEY AUTOINCREMENT,
                            EmailIndex INTEGER
                    );""")
            self.__conn.commit()
            if self.GetCurrentIndex() == None:
                self.__cur.execute("""INSERT INTO Variable (EmailIndex) VALUES (0)""")
                self.__conn.commit()
        except Exception as e:
            print(e)

    def CloseConnection(self):
        self.__conn.close()

    def GetCurrentIndex(self):
        self.__cur.execute("""SELECT EmailIndex FROM Variable""")
        try:
            return self.__cur.fetchone()[0]
        except TypeError:
            return None

    def GetProvider(self, name):
        self.__cur.execute("""SELECT Id FROM Provider WHERE Name LIKE ?""", (name,))
        return [row for row in self.__cur]
    
    def GetSender(self, name):
        self.__cur.execute("""SELECT Id FROM Sender WHERE Name LIKE ?""", (name,))
        return [row for row in self.__cur]

    def SaveProvider(self, name, extention):
        self.__cur.execute("""INSERT INTO Provider (Name, Extention) VALUES (?,?)""", (name, extention))
        self.__conn.commit()
        return self.__cur.lastrowid

    def SaveSender(self, proId, name, address):
        self.__cur.execute("""INSERT INTO Sender (ProviderId, Name, Address) VALUES (?,?,?)""", (proId, name, address))
        self.__conn.commit()
        return self.__cur.lastrowid

    def SaveEmail(self, sendId, path, subject, recievedAt):
        self.__cur.execute("""INSERT INTO Email (SenderId, EmailIndex, Path, Subject, RecievedAt) VALUES (?,?,?,?,?)""", (sendId, path, subject, recievedAt))
        self.__conn.commit()
        return self.__cur.lastrowid
    
    def SaveEmailDetail(self, emailId, processedAt):
        self.__cur.execute("""INSERT INTO EmailDetail (EmailId, ProcessedAt) VALUES (?,?)""", (emailId, processedAt))
        self.__conn.commit()
        return self.__cur.lastrowid

    def SaveIndex(self, index):
        self.__cur.execute("""UPDATE Variable SET EmailIndex = ?""", (index,))
        self.__conn.commit()

    def FetchEmail(self):
        self.__cur.execute("""SELECT * FROM Email""")
        return [row for row in self.__cur]
        