#!/usr/bin/python3

def url_encode_all(url):
    return "".join("%{0:0>2}".format(format(ord(char), "x")) for char in url)

def url_encode_unsafe(url):
    return urllib.parse.quote(url, safe='')

# Simple interface class
class Interface ():
    def __init__ (self):
        self.red = '\033[91m'
        self.green = '\033[92m'
        self.white = '\033[37m'
        self.yellow = '\033[93m'
        self.bold = '\033[1m'
        self.end = '\033[0m'

    def header(self):
        print('\n    >> Advanced Web Attacks and Exploitation')
        print('    >> Interface Class\n')

    def info (self, message):
        print(f"[{self.white}*{self.end}] {message}")

    def warning (self, message):
        print(f"[{self.yellow}!{self.end}] {message}")

    def error (self, message):
        print(f"[{self.red}x{self.end}] {message}")

    def success (self, message):
        print(f"[{self.green}✓{self.end}] {self.bold}{message}{self.end}")

# Instantiate our interface class
global output
output = Interface()

# Output examples
output.header()
output.info('Informational Message')
output.warning('Warning Message')
output.error('Error Message')
output.success('Success Message')