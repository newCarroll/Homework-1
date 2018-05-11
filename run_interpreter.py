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
import CommandLineParser as clp
from docopt import docopt


def begin_interpreter():
    interpreter = itr.Interpreter()

    while True:
        text = input('interpreter> ')
        if not text:
            continue

        interpreter.set_text(text)
        result = interpreter.parse_pipe()
        if result:
            print(result, end='')


def run(args):
    commands = ['wc', 'cat', 'grep', 'ls', 'cd', 'pwd', 'echo']
    for command in commands:
        if command in args.keys() and args[command]:
            clp.CommandLineParser(args)
            exit()

    begin_interpreter()


if __name__ == '__main__':
    arguments = docopt(__doc__)
    run(arguments)
