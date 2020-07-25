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
        messages = int(messages[0])

        for i in range(messages, messages-2, -1):
            res, msg = self.__imap.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    subject = decode_header(msg["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    sender = msg.get("From")

                    provId = self.ParseAddress(sender)
                    senderId = self.__db.SaveSender(provId, "None", sender)                    
                    # if the email message is multipart
                    if msg.is_multipart():
                        # iterate over email parts
                        body = None
                        filepath = None
                        for part in msg.walk():
                            # extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                # get the email body
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                # print text/plain emails and skip attachments
                                print(body)
                            elif "attachment" in content_disposition:
                                filename = part.get_filename()
                                if filename:
                                    if not os.path.isdir("files"):
                                        os.mkdir("files")
                                    filepath = os.path.join("files", filename)
                                    open(filepath, "wb").write(part.get_payload(decode=True))
                        self.__db.SaveEmail(senderId, filepath, subject, body, datetime.datetime.now())

                    else:
                        # extract content type of email
                        content_type = msg.get_content_type()
                        # get the email body
                        body = msg.get_payload(decode=True).decode()
                        if content_type == "text/plain":
                            # print only text email parts
                            print(body)
                    if content_type == "text/html":
                        # if it's HTML, create a new HTML file and open it in browser
                        if not os.path.isdir(subject):
                            # make a folder for this email (named after the subject)
                            os.mkdir(subject)
                        filename = f"{subject[:50]}.html"
                        filepath = os.path.join(subject, filename)
                        # write the file
                        open(filepath, "w").write(body)
                        # open in the default browser
                        webbrowser.open(filepath)

        self.imapDisconnect()
        self.__db.CloseConnection()

    def getSettings(self):
        with open('settings.json', 'r') as json_file:
            self.__settings = json.load(json_file)

    def imapConnect(self):
        self.__imap = imaplib.IMAP4_SSL(self.__settings['imap'])
        self.__imap.login(self.__settings['user'], self.__settings['pass'])

    def imapDisconnect(self):
        self.__imap.close()
        self.__imap.logout()

    def ParseAddress(self, sender):
        print(sender)
        exts = sender.split("@")[1].split('.')
        provider = exts[0]
        proId = self.__db.GetProvider(provider)
        if proId == None:
            return self.__db.SaveProvider(provider, exts[1:])
        return self.__db.GetProvider(provider)

EmailFetch()