from Cappuccino.GCParser import JavaGCParser


class CMSParser(JavaGCParser):
    """Parser for CMS GC Logs"""

    def __init__(self, input_file):
        JavaGCParser.__init__(self, input_file)

    def run(self):
        """Parse the GC Log"""
        pass