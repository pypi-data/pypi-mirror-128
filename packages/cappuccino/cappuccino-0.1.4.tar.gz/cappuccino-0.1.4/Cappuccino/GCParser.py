import re
import datetime
from enum import Enum

import pandas as pd

class GCType(str, Enum):
    G1GC = 'G1GC'
    CMS = 'CMS'
    Parallel = 'Parallel'

class JavaGCParser():

    def __init__(self, input_file):
        self.input_file = input_file

        self.initiating_heap_occupancy_percent = None # -XX:InitiatingHeapOccupancyPercent: Percentage of the (entire) heap occupancy to start a concurrent GC cycle.
        self.max_heap_size = None # Set maximum heap size
        self.algorithm = None # GC Algorithm
        self.starting_flags = {}

        self.determine_gc_alg()

        self.data = []

    def run(self):
        """Parse the GC Log"""
        pass

    def to_df(self):
        """ Concerts list of GC Log data into a dataframe"""
        return pd.DataFrame(self.data)

    def determine_gc_algorithm(self):
        """

        :return:
        """
        with open(self.input_file) as f:
            for line in f:
                m = re.match('^CommandLine flags: .*', line, flags=0)
                if m:
                    if re.match(".*-XX:\+UseG1GC.*", line, flags=0):
                        algorithm = GCType.G1GC

                    elif re.match(".*-XX:\+UseConcMarkSweepGC.*", line, flags=0):
                        algorithm = GCType.CMS

                    elif re.match(".*-XX:\+UseParallelGC.*", line, flags=0):
                        algorithm = GCType.Parallel



    def determine_gc_alg(self):
        """

        :return:
        """
        with open(self.input_file) as f:
            for line in f:
                m = re.match('^CommandLine flags: .*', line, flags=0)
                if m:
                    if re.match(".*-XX:\+UseG1GC.*", line, flags=0):
                        self.algorithm = 'G1GC'
                        self.initiating_heap_occupancy_percent = self.get_long_field(line, '-XX:InitiatingHeapOccupancyPercent', 45)
                        self.max_heap_size = self.get_long_field(line, '-XX:MaxHeapSize')
                        if self.initiating_heap_occupancy_percent and self.max_heap_size:
                            self.occupancy_threshold = int(self.max_heap_size * (self.initiating_heap_occupancy_percent / 100.0) / 1048576.0)

                    elif re.match(".*-XX:\+UseConcMarkSweepGC.*", line, flags=0):
                        self.algorithm = 'CMS'
                        self.initiating_heap_occupancy_percent = self.get_long_field(line, '-XX:CMSInitiatingOccupancyFraction')
                        self.max_heap_size = self.get_long_field(line, '-XX:MaxHeapSize')
                        if self.initiating_heap_occupancy_percent and self.max_heap_size:
                            self.occupancy_threshold = int(self.max_heap_size * (self.initiating_heap_occupancy_percent / 100.0) / 1048576.0)

                    elif re.match(".*-XX:\+UseParallelGC.*", line, flags=0):
                        self.algorithm = "ParalellGC"

                    self.get_starting_flags(line)

                    return

    def get_starting_flags(self, line:str):
        """

        :param line:
        :return:
        """
        flags = line.replace('CommandLine flags: ', '').split(' ')
        for flag in flags:
            field = self.get_flag_name(flag)
            if field:
                self.starting_flags[field] = self.get_long_field(flag, field)


    def get_long_field(self, line:str, field:str, def_value=None):
        """

        :param line:
        :param field:
        :param def_value:
        :return:
        """
        if '+' in field:
            return True
        else:
            m = re.match(f".*{field}=([0-9a-zA-Z_/]+).*", line, flags=0)
            if m:
                value = m.group(1)
                if value.isnumeric():
                    return int(value)
                else:
                    return value
            else:
                return True

    def get_flag_name(self, string:str):
        """

        :param string:
        :return:
        """
        m = re.match(f"-XX:([a-zA-Z]+)=", string, flags=0)
        if m:
            return m.group(1)
        else:
            string = string.replace('-XX:', '')
            return string


    @staticmethod
    def convert_value(key, value):
        if 'float' in key:
            return float(value)
        if 'timestamp' in key:
            dt = datetime.datetime.strptime(value[:-5],"%Y-%m-%dT%H:%M:%S.%f")
            return datetime.datetime.strptime(value[:-5],"%Y-%m-%dT%H:%M:%S.%f")
        if '_int' in key:
            return int(value)
        else:
            return value

    @staticmethod
    def convert_key(key, value):
        if 'float' in key:
            return float(value)
        if 'timestamp' in key:
            return datetime.datetime.strptime(value[:-5],"%Y-%m-%dT%H:%M:%S.%f")
        if '_int' in key:
            return int(value)
        else:
            return value

    @staticmethod
    def process_task(d:dict):
        new_key = None
        new_value = None

        for key, value in d.items():
            if 'tasks' in key:
                new_key = f"{d['tasks']}_milliseconds_float".lower().replace(' ', '_')
            if 'time_' in key:
                new_value = float(value)

            if new_key and new_value:
                return {new_key: new_value}


    @staticmethod
    def process_size_changes_line(d:dict):
        dictionary = {}
        for key, value in d.items():
            if 'value' in key:
                unit_key =  key.replace('_value', '_unit')
                if d[unit_key] == 'G':
                    new_value = float(value) * 1000
                    new_unit = 'M'
                elif d[unit_key] == 'K':
                    new_value = float(value) / 1000
                    new_unit = 'M'
                elif d[unit_key] == 'B':
                    new_value = float(value) / (1000*1000)
                    new_unit = 'M'
                else:
                    new_value = float(value)
                    new_unit = d[unit_key]

                dictionary.update({key: new_value, unit_key: new_unit})

        return dictionary

    def is_size_change_line(self, line):
        if "Eden" in line:
            return True

    def is_first_line(self, line):
        PATTERN = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}(-|\+)\d{4}.*"
        m = re.match(PATTERN, line, flags=0)
        if m:
            return True

    def is_pause(self, line):
        if 'GC pause' in line:
            return True
