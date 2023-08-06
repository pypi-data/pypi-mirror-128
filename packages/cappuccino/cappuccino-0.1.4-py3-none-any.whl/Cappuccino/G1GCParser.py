import re
from tqdm import tqdm
import Cappuccino.GCParser as GCP

class G1GCParser(GCP.JavaGCParser):
    """Parser for G1GC GC Logs"""
    STRING = "2021-10-06T10:32:34.341-0500: 23.215: Total time for which application threads were stopped: 0.0120506 seconds, Stopping threads took: 0.0000788 seconds"
    PATTERNS = ["(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}(-|\+)\d{4}): (\d+\.\d+): Total time for which application threads were stopped: (?P<total_time_stopped_seconds_float>\d+\.\d+) seconds, Stopping threads took: (?P<stopping_threads_time_seconds_float>\d+\.\d+) seconds",
                "(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}(-|\+)\d{4}): (\d+\.\d+): \[(?P<operation>[a-zA-Z -]*)\]",
                "(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}(-|\+)\d{4}): (\d+\.\d+): \[(?P<operation>[a-zA-Z -]*), (?P<wait_time_seconds_float>\d+\.\d+) secs\]",
                "(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}(-|\+)\d{4}): (\d+\.\d+): \[(?P<operation>[a-zA-Z -]*), (?P<wait_time_seconds_float>\d+\.\d+) secs\]",
                "(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}(-|\+)\d{4}): (\d+\.\d+): \[(?P<operation>[a-zA-Z -]*), (?P<wait_time_seconds_float>\d+\.\d+) secs\]",
                "(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}(-|\+)\d{4}): (\d+\.\d+): \[(?P<operation>[a-zA-Z -]*)\((?P<pause_type>[a-zA-Z -1]*)\) \((?P<collection_type>[a-zA-Z -]*)\) \((?P<collection_phase>[a-zA-Z -]*)\), (?P<wait_time_seconds_float>\d+\.\d+) secs\].*",
                "(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}(-|\+)\d{4}): (\d+\.\d+): \[(?P<operation>[a-zA-Z -]*)\((?P<pause_type>[a-zA-Z -1]*)\) \((?P<collection_type>[a-zA-Z -]*)\), (?P<wait_time_seconds_float>\d+\.\d+) secs\].*",
                "(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}(-|\+)\d{4}): (\d+\.\d+): \[(?P<operation>[a-zA-Z -]*)\((?P<pause_type>[a-zA-Z -1]*)\) \((?P<collection_type>[a-zA-Z -]*)\)",
                "(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}(-|\+)\d{4}): (\d+\.\d+): \[(?P<operation>[a-zA-Z -]*)\((?P<pause_type>[a-zA-Z -1]*)\)",
                ".*, (?P<wait_time_seconds_float>\d+\.\d+) secs\].*",
                " *\[Parallel Time: (?P<parallel_time_milliseconds_float>\d+\.\d+) ms, GC Workers: (?P<gc_workers_int>\d+)\]",
                " *\[Times: user=(?P<user_time_seconds_float>\d+\.\d+) sys=(?P<system_time_seconds_float>\d+\.\d+), real=(?P<real_time_seconds_float>\d+\.\d+) secs\]",
                #" *\[(?P<tasks>[a-zA-Z -]*): (?P<time_milliseconds_float>\d+\.\d+) ms\]",
                #" *\[Eden: (?P<eden_initial_used_value>\d+\.\d+)(?P<eden_initial_used_unit>\w)\((?P<eden_initial_capacity_value>\d+\.\d+)(?P<eden_initial_capacity_unit>\w)\)->(?P<eden_final_used_value>\d+\.\d+)(?P<eden_final_used_unit>\w)\((?P<eden_final_capacity_value>\d+\.\d+)(?P<eden_final_capacity_unit>\w)\) Survivors: (?P<survivor_initial_value>\d+\.\d+)(?P<survivor_initial_unit>\w)->(?P<survivor_final_value>\d+\.\d+)(?P<survivor_final_unit>\w) Heap: (?P<m>\d+\.\d+)(?P<n>\w)\((?P<o>\d+\.\d+)(?P<q>\w)\)->(?P<r>\d+\.\d+)(?P<s>\w)\((?P<t>\d+\.\d+)(?P<u>\w)\)\]"
                " *\[Eden: (?P<eden_initial_used_value>\d+\.\d+)(?P<eden_initial_used_unit>\w)\((?P<eden_initial_capacity_value>\d+\.\d+)(?P<eden_initial_capacity_unit>\w)\)->(?P<eden_final_used_value>\d+\.\d+)(?P<eden_final_used_unit>\w)\((?P<eden_final_capacity_value>\d+\.\d+)(?P<eden_final_capacity_unit>\w)\) Survivors: (?P<survivor_initial_value>\d+\.\d+)(?P<survivor_initial_unit>\w)->(?P<survivor_final_value>\d+\.\d+)(?P<survivor_final_unit>\w) Heap: (?P<heap_initial_used_value>\d+\.\d+)(?P<heap_initial_used_unit>\w)\((?P<heap_initial_capacity_value>\d+\.\d+)(?P<heap_initial_capacity_unit>\w)\)->(?P<heap_final_used_value>\d+\.\d+)(?P<heap_final_used_unit>\w)\((?P<heap_final_capacity_value>\d+\.\d+)(?P<heap_final_capacity_unit>\w)\)\]"
                ]

    def __init__(self, input_file):
        GCP.JavaGCParser.__init__(self, input_file)

    def run(self):
        """Parse the GC Log"""

        gc_flag = False

        num_lines = sum(1 for line in open(self.input_file, 'r'))
        with open(self.input_file) as f:
            for i, line in enumerate(tqdm(f, total=num_lines, desc=self.input_file.split('/')[-1])):

                if self.is_first_line(line):

                    if gc_flag:
                        self.data.append(
                            {key: GCP.JavaGCParser.convert_value(key, value) for key, value in dictionary.items()})

                    dictionary = {}

                    if self.is_pause(line):
                        gc_flag = True
                    else:
                        gc_flag = False


                for pattern in self.PATTERNS:
                    regex = re.compile(pattern)
                    capture = regex.match(line)
                    if capture:
                        #if Cappuccino.process_task(capture.groupdict()):
                        #    dictionary.update(Cappuccino.process_task(capture.groupdict()))
                        if self.is_size_change_line(line):
                            size_dict = GCP.JavaGCParser.process_size_changes_line(capture.groupdict())
                            dictionary.update(GCP.JavaGCParser.process_size_changes_line(capture.groupdict()))
                        else:
                            dictionary.update(capture.groupdict())



                        if not gc_flag and self.is_first_line(line):
                            self.data.append({key: GCP.JavaGCParser.convert_value(key,value) for key, value in dictionary.items()})
                        break
