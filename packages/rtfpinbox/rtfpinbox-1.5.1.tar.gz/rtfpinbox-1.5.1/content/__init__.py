class Content(object):
    # -- Methods
    def __init__(self, message, html, links, meta):
        """ Constructor function """
        super().__init__()
        self.message = message
        self.html = html
        self.links = links
        self.meta = meta
