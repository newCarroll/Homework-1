##!/usr/bin/env python3

"""Interpreter.

Usage:
  run_interpreter.py grep [-i] [-w] [-A=<n>] <pattern>  <file>
  run_interpreter.py (-h | --help)
  run_interpreter.py

Options:
  -h --help     Show this screen. Command string takes only grep command.
  -i            Ignore case.
  -w            Search whole words.
  -A=<n>        Write n string after every mapped string [n default 0].

"""

import Interpreter as itr
from docopt import docopt


def begin_interpreter(arguments=None):

    interpreter = itr.Interpreter(arguments)
    if arguments['grep']:
        result = interpreter.parse_pipe()
        if result:
            print(result, end='')
    else:
        while True:
            print('interpreter> ', end='')
            text = input()
            if not text:
                continue

            interpreter.set_text(text)
            result = interpreter.parse_pipe()
            if result:
                print(result, end='')


if __name__ == '__main__':
    arguments = docopt(__doc__)
    begin_interpreter(arguments)
