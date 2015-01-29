import csv, codecs, cStringIO
import uuid

class PaginationMixin():
    def get_paginate_by(self, queryset):
        if self.request.user.pagelength == None:
            return self.request.user.pagelength
        else:
            return 30

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([unicode(s).encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def get_file_location(instance=None, filename=""):

    destination = ""

    if instance:
        destination += instance.__class__.__name__.lower()

    destination += "/"
    ext = filename.split(".")[-1]
    destination += "{0}.{1}".format(uuid.uuid4(), ext)

    return destination