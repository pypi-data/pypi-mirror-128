from datetime import datetime
import pytz

""" This is the email object Class. It contains the email Number, It's Date, Who sent it, It's subject, the headers and 
the content of the email """

class Email(object):
    # -- Methods
    def __init__(self, number, date, sentby, subject, headers, content):
        """ Constructor function """
        super().__init__()
        self.number = number
        self.date = date
        self.sentby = sentby
        self.subject = subject
        self.headers = headers
        self.content = content



