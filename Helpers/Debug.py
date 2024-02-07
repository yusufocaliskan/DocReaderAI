import pprint
from textwrap import indent


class Debug:

    def __init__(self, doc):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(doc)
        return
