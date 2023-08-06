from datetime import date
from email.message import EmailMessage

from emails import Email
from Headers import Headers
from Content import Content
from Demographics import Demographics
import nltk

nltk.download('wordnet')
from nltk.corpus import wordnet

"""This is the inbox Class. It contains the ID of the inbox, the Name of the inbox and A list of the emails in the 
inbox. """


class Inbox(object):
    # -- Methods
    def __init__(self, id, name):
        """ Constructor function """
        super().__init__()
        self.ID = id
        self.name = name
        self.demographics = None
        self.email_list = []
        self._size = 0
        self._maxdate = 0
        self._mindate = 0

    def add_email(self, message):
        """ Create an email object and add it to the inbox. Required a message object. Will throw
        error if input is not a message """
        if isinstance(message, EmailMessage) is False:
            raise TypeError("This is not a EmailMessage object. Please Check Type and try again.")
        else:
            date = None
            sentby = None
            subject = None
            sentto = None
            content_type = None
            message_id = None
            dkim_signature = None
            mime_version = None
            others = {}
            received = []
            content = None
            for item in message.items():
                if item[0].lower() == "date":
                    date = item[1]
                elif item[0].lower() == "received":
                    received.append(item[1])
                elif item[0].lower() == "subject":
                    subject = item[1]
                elif item[0].lower() == "from":
                    sentby = item[1]
                elif item[0].lower() == "to":
                    sentto = item[1]
                elif item[0].lower() == "content-type":
                    content_type = item[1]
                elif item[0].lower() == "dkim-signature":
                    dkim_signature = item[1]
                elif item[0].lower() == "message-id":
                    message_id = item[1]
                elif item[0].lower() == "mime-version":
                    mime_version = item[1]
                else:
                    if item[0] in others.keys():
                        others[item[0]].append(item[1])
                    else:
                        others[item[0]] = [item[1]]

            headers = Headers(sentby, sentto, subject, received, date, content_type, message_id, dkim_signature,
                              mime_version)
            headers.allothers = others
            newEmail = Email(self.getsize(), headers.date, headers.sentby, subject, headers, content)
            self.email_list.append(newEmail)
            self.increasesize()
            self.setmaxmindate()

    def bysender(self, sender):
        """ Finds and returns list of messages sent by sender. """
        senderlist = []
        for message in self.email_list:
            if "@" in sender:
                if sender == message.sentby.address:
                    senderlist.append(message)
            else:
                if sender in message.sentby.proper_name:
                    senderlist.append(message)
        return senderlist

    def bydate(self, start_date, end_date, inc):
        """ Finds and returns list of messages between 2 dates. If inc is true Is inclusive, else nonInclusive. Will
        throw errors if inputs are not dates or if dates are out of bounds. """
        if isinstance(start_date, date) is False or isinstance(end_date, date) is False:
            raise TypeError("Search Terms must be date objects.")

        if self.getmindate() > start_date > self.getmaxdate or self.getmindate() > end_date > self.getmaxdate:
            raise ValueError(
                f'Date out of range. Earliest Date in inbox: {self.getmindate()}. Latest Date in inbox: {self.getmaxdate()}.')
        else:
            if inc is True:
                datelist = []
                for message in self.email_list:
                    if start_date <= message.date <= end_date:
                        datelist.append(message)
                return datelist
            else:
                datelist = []
                for message in self.email_list:
                    if start_date < message.date < end_date:
                        datelist.append(message)
                return datelist



    def bynumber(self, start_num, end_num, inc):

        """ Finds and returns list of messages between 2 indices. Is inclusive. Will throw errors
        if inputs are out of bounds. """

        if 0 > start_num or end_num >= self.getsize():
            raise ValueError(f'Indices out of range. Must be number between 0 and {self.getsize() - 1}.')
        else:
            if inc is True:
                numlist = []
                for message in self.email_list:
                    if start_num <= message.number <= end_num:
                        numlist.append(message)
                return numlist
            else:
                numlist = []
                for message in self.email_list:
                    if start_num < message.number < end_num:
                        numlist.append(message)
                return numlist


    def bysubject(self, keywords):

        """ Finds and returns list of messages containing keyword/s. """

        sublist = []
        if isinstance(keywords, str):
            for messages in self.email_list:
                if keywords in messages.subject:
                    sublist.append(messages)

        elif isinstance(keywords, list):
            for messages in self.email_list:
                if all(keyword in messages.subject for keyword in keywords):
                    sublist.append(messages)
        return sublist

    def bysubjectsynonym(self, keyword):

        """ Finds and returns list of messages containing synonyms of keyword. """

        if isinstance(keyword, str):
            wl = keyword.split(" ")
            if len(wl) != 1:
                raise ValueError("This function only accepts single word input.")
            else:
                syndict = {}

                for synset in wordnet.synsets(keyword):
                    for lemma in synset.lemma_names():
                        for messages in self.email_list:
                            if lemma in messages.subject and lemma != keyword:
                                if lemma in syndict.keys():
                                    syndict[lemma].append(messages)
                                else:
                                    syndict[lemma] = [messages]
                return syndict
        else:
            raise TypeError("This function only accepts single word strings.")

    def inboxheadersearch(self, keyword):
        headerlist = []
        for message in self.email_list:
            if keyword in message.headers.allothers.keys():
                headerlist.append(message)
        return headerlist

    def removeemail(self, num):

        """ Deletes email from inbox by index. Will throw error if index is out of bounds. """

        if 0 > num > len(self.getsize()):
            raise ValueError(f'Indices out of range. Must be number between 0 and {self.getsize()}.')
        else:
            self.email_list.pop(num)
            self.decreasesize()
            self.setmaxmindate()

    def getsize(self):

        """ Returns number of emails in inbox. """

        return self._size

    def increasesize(self):

        """ Increase number of emails in inbox. """

        self._size = self._size + 1

    def decreasesize(self):

        """ Decrease number of emails in inbox. """

        self._size = self._size - 1

    def setmaxmindate(self):

        """ Finds the earliest and latest dates of emails in inbox. """

        datelist = []
        for message in self.email_list:
            if message.date is None:
                raise TypeError(f"Date field of message number {message.number} contains NoneType."
                                f" Check if the date was properly inputted.")
            else:
                datelist.append(message.date)
        self._maxdate = max(datelist)
        self._mindate = min(datelist)

    def getmaxdate(self):

        """ Returns the latest date of emails in inbox. """

        return self._maxdate

    def getmindate(self):

        """ Returns the earliest date of emails in inbox. """

        return self._mindate
