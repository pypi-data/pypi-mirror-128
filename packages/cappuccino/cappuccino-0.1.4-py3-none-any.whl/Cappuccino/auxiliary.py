import Cappuccino.G1GCParser as G1GC
import Cappuccino.CMSParser as CMS
import re

def get_gc_parser(input_file):
        """

        :return:
        """
        with open(input_file) as f:
            for line in f:
                m = re.match('^CommandLine flags: .*', line, flags=0)
                if m:
                    if re.match(".*-XX:\+UseG1GC.*", line, flags=0):
                        return G1GC.G1GCParser(input_file=input_file)

                    elif re.match(".*-XX:\+UseConcMarkSweepGC.*", line, flags=0):
                        return CMS.CMSParser(input_file=input_file)

                    elif re.match(".*-XX:\+UseParallelGC.*", line, flags=0):
                        return None

                    return None