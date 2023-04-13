import json
import os
import time
from multiprocessing import Lock
from datetime import datetime, timedelta

class LANA:

    # public:
    def log_action_begin(self, action):
        self._log_header(f"Starting {'Sub-' if len(self.action_stack) > 0 else ''}Action")

        self.action_stack.append(action)
        self._log_action_stack()

        self._log_header()

    def log_action_end(self, message):
        if len(self.action_stack) > 0:
            self.log(f"{message}")
            self.action_stack.pop()
            self._log_header(f"{'Sub-' if len(self.action_stack) > 0 else ''}Action Complete")
        else:
            self.log(f"Logging Error: No action to end")

    def log_action_single(self, current_action):
        self.log(current_action + "...")

    def log_execution_time(self, start_time, end_time):
        self.log(f"Time Taken: {round(end_time - start_time, 1)}s")

    def log_blank_line(self):
        if not self._prev_line_equals(""):
            self._write_line("")

    def log_json(self, data_description, data, prefix=True):
        self.log(data_description + ": ", prefix=prefix)
        initial_indent_level = self.indent_level
        self.increase_indent()

        for json_object in data:
            if type(data[json_object]) == dict:
                self.increase_indent()
                self.log_json(json_object, data[json_object], prefix=False)
                self.decrease_indent()
            elif type(data[json_object]) == list:
                self.log_no_prefix(json_object + ":")
                self.increase_indent()
                for item in data[json_object]:
                    self.log_json(json_object + f"[{data[json_object].index(item)}]", item, prefix=False)
                
                self.decrease_indent()
            else:
                self.log_no_prefix(f"{json_object}: {data[json_object]}")

        # for line in formatted_json.split('\n'):
        #     if line[-1:] == "{" or line[-1:] == "[":
        #         if line[-1:] == "[":
        #             self.log_no_prefix(line[:-1] + " [")
        #         if len(line) > 2:
        #             self.log_no_prefix(line[:-1])
        #         self.increase_indent()
        #     elif line[0] == "}"or line[0] == "]":
        #         self.decrease_indent()
        #     else:
        #         self.log_no_prefix(line)

        self.decrease_indent()
        if initial_indent_level != self.indent_level:
            self.log_no_prefix("Logging Error: Invalid JSON")
            self.indent_level = initial_indent_level

        self.log_blank_line()

    def log_no_prefix(self, message, indent_level=None):
        self.log(message, indent_level=indent_level, prefix=False)
        
    def log(self, message, indent_level=None, prefix=True):
        if indent_level == None:
            indent_level = self.indent_level
        
        prefix = self.log_prefix if prefix else ""
        offset = len(self.log_prefix) - len(prefix)

        self._write_line(prefix + " " * (offset + indent_level * self.indent_spaces) + f"{message}")

    def log_warning(self, message):
        # Log an fstring with a yellow color
        self.log(f"\033[93mWarning: {message}\033[0m")

    def increase_indent(self):
        self.indent_level += 1

    def decrease_indent(self):
        self.indent_level = max(0, self.indent_level - 1)

    # private: 
    def __init__(self, logfile=None):
        self.logfile = logfile if logfile else f"logs/LaNA_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        self.indent_level = 0
        self.indent_spaces = 4
        self.log_prefix = "[L.a.N.A.] "
        self.header_char = "-"
        self.header_size = 150
        self.logged_lines = []
        self.action_stack = []
        self.mutex = Lock()

        self._log_intro()

    def _log_intro(self):
        os.system("clear")
        self._log_header()
        self._write_line(f"Hiya, I'm 'The L.a.N.A. Debugger' (Legible And Not Annoying Debugger).")
        self._log_header()
        self.log_blank_line()

    def _log_action_stack(self):
        if len(self.action_stack) > 0:
            for action in self.action_stack:
                index = self.action_stack.index(action)
                
                # Determine formatting
                arrow = ''
                if index != 0:
                    if index == len(self.action_stack) - 1:
                        arrow = '  └>'
                    else:
                        arrow = '  ├>'

                self.log(f"{arrow}{action}...", indent_level=0, prefix=(index == 0))

    def _log_header(self, message=""):
        if (self._prev_line_equals("HEADER") or (self._prev_line_equals("") and self._prev_line_equals("HEADER", 2))):
            self.log_blank_line()

        self.logged_lines.append("HEADER")
        if message == "":
            self._write((self.header_char * self.header_size) + '\n')
        else:
            header_char_count = (self.header_size - len(message) - 2) // 2
            header_border = self.header_char * header_char_count
            self._write(header_border + " " + message + " " + header_border + '\n')

    def _prev_line_equals(self, string, offset=1):
        with self.mutex:
            if len(self.logged_lines) > 0:
                return self.logged_lines[-offset] == string
        return False

    def _write_line(self, raw_out):
        with self.mutex:
            self.logged_lines.append(raw_out)
        self._write(raw_out + '\n')

    def _write(self, raw_out):
        #with open(self.logfile, 'a') as log:
        #    log.write(f"{raw_out}")
        print(f"{raw_out}", end="")

#COLOUR!!
#BOX DRAWINGS!!
# def colour