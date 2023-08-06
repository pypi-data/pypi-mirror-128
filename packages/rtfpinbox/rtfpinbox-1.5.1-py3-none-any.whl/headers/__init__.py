from datetime import datetime
import pytz
from email.utils import parsedate_to_datetime

"""This is the Header class. It contains the headers."""


class Headers(object):
    # -- Methods
    def __init__(self, sentby, sentto, subject, received, date, content_type, message_id, dkim_signature, mime_version):
        """ Constructor function """
        super().__init__()
        self.sentby = self.formatsentby(sentby)
        self.sentto = sentto
        self.subject = subject
        self.received = received
        self.date = self.format_date(date)
        self.content_type = content_type
        self.message_id = message_id
        self.dkim_signature = dkim_signature
        self.mime_version = mime_version
        self.allothers = {}

    def format_date(self, item):

        """ This method takes the string date and turns it into a date object. """
        date = parsedate_to_datetime(item)
        date2 = date.astimezone(pytz.utc)
        return date2

    def headersearch(self, keyword):

        if keyword in self.allothers.keys():
            return self.allothers[keyword]
        else:
            return None

    def formatsentby(self, sentby):
        s = sentby.split( " <" )
        return SentBy( s[0].replace( '"', '' ),
                       s[1][0:-1] )


class SentBy( object ):
    # -- Methods
    def __init__(self, proper_name, address):
        """ Constructor function """
        super().__init__()
        self.proper_name = proper_name
        self.address = address