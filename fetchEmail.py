import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import json
import sqlite3

settings = {}
with open('settings.json', 'r') as json_file:
    settings = json.load(json_file)

imap = imaplib.IMAP4_SSL(settings['imap'])
imap.login(settings['user'], settings['pass'])

status, messages = imap.select("INBOX")
messages = int(messages[0])

imap.close()
imap.logout()