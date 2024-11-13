# This file is part of SmplGen. Copyright (C) 2024 Christian Rauch.
# Distributed under terms of the GPL3 license.


import sys
import argparse
from generator import Generator


class CommandLineInterface:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-n', '--entries', type=int, help='number of entries', default=1)
        self.parser.add_argument('-i', '--input-file', type=str, help='input pattern file')
        self.parser.add_argument('-o', '--output-file', type=str, help='output file')
        self.parser.add_argument('pattern', nargs='?', type=str, help='pattern', default=None)

    def parse(self): 
        args = self.parser.parse_args()
        
        if args.input_file:
            with open(args.input_file, 'r') as file:
                pattern = file.read().strip()
        else:
            pattern = args.pattern
        
        if pattern in [None, ""]: raise Exception("Pattern not specified")
        
        g = Generator(pattern, args.entries)
        generated_string = g.generate()

        if not args.output_file:
            print(generated_string)
        else:
            with open(args.output_file, 'w') as file:
                file.write(generated_string)


if __name__ == '__main__':
    parser = CommandLineInterface()
    parser.parse()