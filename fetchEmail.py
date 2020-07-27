import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import json
import datetime
import sqlite3
from DatabaseManager import DatabaseManager

class EmailFetch():

    __db = DatabaseManager()
    __settings = {}

    def __init__(self):
        self.getSettings()
        self.imapConnect()
        status, messages = self.__imap.select("INBOX")
        messagesCount = int(messages[0])

        curIndex = self.__db.GetCurrentIndex()
        for i in range(curIndex, messagesCount, 1):
            res, msg = self.__imap.fetch(str(i), "(RFC822)")
            self.getMail(msg)

        self.__db.SaveIndex(messagesCount)
        self.imapDisconnect()
        self.__db.CloseConnection()

    def getMail(self, msg):
        filePath = None
        for response in msg:
            if isinstance(response, tuple):
                mail = email.message_from_bytes(response[1])
                subject = decode_header(mail["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
                sender = mail.get("From")

                provId = self.parseAddress(sender)
                senderId = self.__db.SaveSender(provId, "None", sender)                    
                if mail.is_multipart():
                    filePath = self.saveMultipartMail(mail)

                else:
                    content_type = mail.get_content_type()
                    body = mail.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        filePath = self.saveNonMultipartMail(body, subject)
                if content_type == "text/html":
                    filePath = self.saveNonMultipartMail(body, subject, True)

        self.__db.SaveEmail(senderId, filePath, subject, datetime.datetime.now())

    def saveMultipartMail(self, mail):
        filePaths = []
        for part in mail.walk():
            filePath = None
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            try:
                body = part.get_payload(decode=True).decode()
            except:
                pass
            if "attachment" in content_disposition:
                filename = part.get_filename()
                if filename:
                    if not os.path.isdir("files"):
                        os.mkdir("files")
                    filePath = os.path.join("files", filename)
                    with open(filePath, "wb") as mailFile:
                        mailFile.write(part.get_payload(decode=True))
            else:
                with open(filePath, "wb") as mailFile:
                    mailFile.write(body)

            if filePath != None:
                filePaths.append(filePath)
        return [filePaths]
    
    def saveNonMultipartMail(self, body, subject, html = False):
        ext = "txt"
        if html:
            ext = "html"
        filename = f"{subject[:50]}.{ext}"
        filepath = os.path.join(subject, filename)
        with open(filepath, "w") as mailFile:
            mailFile.write(body)
        return [filepath]

    def getSettings(self):
        with open('settings.json', 'r') as json_file:
            self.__settings = json.load(json_file)

    def imapConnect(self):
        self.__imap = imaplib.IMAP4_SSL(self.__settings['imap'])
        self.__imap.login(self.__settings['user'], self.__settings['pass'])

    def imapDisconnect(self):
        self.__imap.close()
        self.__imap.logout()

    def parseAddress(self, sender):
        print(sender)
        exts = sender.split("@")[1].split('.')
        provider = exts[0]
        proId = self.__db.GetProvider(provider)
        if proId == None:
            return self.__db.SaveProvider(provider, exts[1:])
        return self.__db.GetProvider(provider)

EmailFetch()