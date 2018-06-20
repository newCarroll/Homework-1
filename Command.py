#!/usr/bin/env python3

from sys import getsizeof
from pathlib import Path
import subprocess
import os
import io
import re


class Exit:
    def __init__(self, arguments, instream):
        instream.close()

    def execute(self):
        exit()


class Cd:
    def __init__(self, arguments, instream):
        self.arguments = arguments
        self.input_stream = instream
        instream.close()

    def execute(self):
        outstream = io.StringIO()
        if len(self.arguments) == 0 and self.input_stream.getvalue():
            return outstream
        elif len(self.arguments) > 1:
            print('cd: too many arguments.')
            raise Exception()
        else:
            new_directory = Path(self.arguments[0].text)
        if len(self.arguments) == 0:
            new_directory = Path.home()
        if new_directory.is_dir():
            os.chdir(new_directory)
        else:
            print('cd: {}: Not a directory.'.format(new_directory))
        return outstream


class Ls:
    def __init__(self, arguments, instream):
        instream.close()
        self.arguments = arguments

    def execute(self):
        outstream = io.StringIO()
        lists_of_files = {}
        current_dir = os.getcwd()

        if len(self.arguments) == 0:
            dirlist = os.listdir(current_dir)
            lists_of_files.update({current_dir: dirlist})
        else:
            text_arguments = []
            for arg in self.arguments:
                text_arguments.append(arg.text)
            for dir in sorted(text_arguments):
                if dir == '~':
                    dir = Path.home()
                try:
                    dirlist = os.listdir(dir)
                except Exception:
                    print('ls: cannot access: {}: '
                          'No such file or directory.'.format(dir),
                          file=outstream, end=os.linesep)

                    return outstream
                lists_of_files.update({dir: dirlist})
        plur = (len(lists_of_files) > 1)
        for (directory, files) in lists_of_files.items():
            if plur:
                print(directory, file=outstream, end=os.linesep)
            for file in files:
                if file[0] != '.':
                    print(file, file=outstream, end=os.linesep)
            if plur:
                print(file=outstream)

        return outstream


class Wc:
    def __init__(self, arguments, instream):
        self.input_stream = instream
        self.arguments = arguments

    def execute(self):
        # проверка наличия аргумента:
        # если его нет - считываем из потока
        if len(self.arguments) == 0:
            stream_value = self.input_stream.getvalue()
            self.input_stream.close()
            lines = stream_value.split('\n')
            count_line = 0
            count_word = 0
            count_byte = 0
            if lines[-1] == '':
                lines = lines[:-1]
            for line in lines:
                count_line += 1
                count_word += len(line.split())
                b = getsizeof(line) - getsizeof('')
                count_byte += b
            outstream = io.StringIO()
            print('{:>3} {:>3} {:>3}'.format(count_line,
                                             count_word, count_byte),
                  file=outstream, end='\n')

            return outstream

        else:
            filename = self.arguments[0].text
            try:
                file = open(filename, 'r')
            except IOError:
                print('wc: ' + filename + ': No such file')
                raise Exception()
            else:
                with file:
                    count_line = 0
                    count_word = 0
                    count_byte = 0
                    for line in file:
                        count_line += 1
                        count_word += len(line.split())
                        b = getsizeof(line) - getsizeof('')
                        count_byte += b
                    outstream = io.StringIO()
                    print('{:>3} {:>3} {:>3} {:>6}'.format(count_line,
                                                           count_word,
                                                           count_byte,
                                                           filename),
                          file=outstream, end='\n')

                    return outstream


class Cat:
    def __init__(self, arguments, instream):
        self.input_stream = instream
        self.arguments = arguments

    def execute(self):
        # проверка наличия аргумента, если его нет - считываем из потока
        if len(self.arguments) == 0:
            stream_value = self.input_stream.getvalue()
            self.input_stream.close()
            lines = stream_value.split('\n')
            outstream = io.StringIO()
            for line in lines:
                print(line, file=outstream, end='')
                return outstream

        else:
            filename = self.arguments[0].text
            try:
                file = open(filename, 'r')
            except IOError:
                print('cat: ' + filename + ': No such file')
            else:
                outstream = io.StringIO()
                with file:
                    for line in file:
                        print(line, file=outstream, end='')
            return outstream


class Pwd:
    def __init__(self, arguments, instream):
        instream.close()
        self.arguments = arguments

    def execute(self):
        cwd = os.getcwd()
        outstream = io.StringIO()
        print(cwd, file=outstream, end='\n')
        return outstream


class Echo:
    def __init__(self, arguments, instream):
        instream.close()
        self.arguments = arguments

    def execute(self):
        outstream = io.StringIO()
        for arg in self.arguments:
            print(arg.text, file=outstream, end=' ')
        print(file=outstream, end='\n')
        return outstream

class Grep:
    def __init__(self, args=None, instreams=None, clarguments=None):
        self.input_stream = instreams
        self.arguments = args
        self.keys = ["-i", "-w", "-A"]
        self.clargs = clarguments

    def print_lines(self, i, line, outstream, text_for_search, n=None):
        print(line, file=outstream, end='')
        if n is not None:
            n = int(n)
            if n < 0:
                print('n must be non-negative')
                raise Exception

            for added_line in text_for_search[i + 1:min(len(text_for_search), i + n + 1)]:
                print(added_line, file=outstream, end='')

    def grep(self, pattern, text, i=False, w=False, n=None):
        
        outstream = io.StringIO()
        for j, line in enumerate(text):
            if w:
                pattern = r'\b' + pattern + r'\b'
            try:
                if i:
                    if re.search(pattern, line, re.IGNORECASE):
                        self.print_lines(j, line, outstream, text, n)
                else:
                    if re.search(pattern, line):
                        self.print_lines(j, line, outstream, text, n)
            except Exception:
                pass
        return outstream

    def parse_input_string(self):
        is_parsing_keys = True
        flag_w = False
        flag_i = False
        remaining_arguments = []
        input_keys = []
        pos_a = -1
        n = None

        # всегда есть хоть 1 аргумент - шаблон
        if len(self.arguments) == 0:
            print("Error: no input template")
            raise Exception

        for i, arg in enumerate(self.arguments):
            if arg.text in self.keys:
                if is_parsing_keys:
                    if arg.text == '-A':
                        pos_a = i
                    input_keys.append(arg.text)
                else:
                    print("All keys must be before template (and file)")
                    raise Exception

            else:
                if pos_a != -1 and i == pos_a + 1:
                    if arg.text.isdigit():
                        n = int(arg.text)
                    else:
                        print("-A requires int n")
                        raise Exception
                else:
                    is_parsing_keys = False
                    remaining_arguments.append(arg.text)

        if "-i" in input_keys:
            flag_i = True
        if "-w" in input_keys:
            flag_w = True

        return flag_i, flag_w,\
            n, remaining_arguments

    def execute(self):
        if self.clargs is None:
            flag_i, flag_w, n, args = self.parse_input_string()
            text = []
        else:
            flag_i, flag_w, n = self.clargs['-i'], self.clargs['-w'], self.clargs['-A']
            args = [self.clargs['<pattern>'], self.clargs['<file>']]
            text = []


        if len(args) == 0:
            print("There is no template")
            raise Exception

        if len(args) == 1:
            stream_value = self.input_stream.getvalue()
            lines = stream_value.split('\n')
            for line in lines:
                text.append(line + '\n')
            template = args[0]

        elif len(args) == 2:
            template = args[0]
            filename = args[1]
            try:
                f = open('1.txt','r')
                for line in f:
                    text.append(line)
                f.close()
            except Exception:
                print(filename + ': No such file')

        else:
            print("Too many arguments")
            return

        self.input_stream.close()
        try:
            return self.grep(template, text, flag_i, flag_w, n)
        except Exception:
            return


class ShellProcess:
    """
    при наличии неидентифицированной
    команды запускается shell process
    """
    def __init__(self, pipe_part, instream):
        self.command = pipe_part[0].text
        instream.close()
        self.arguments = pipe_part[1:]

    def execute(self):
        shell_arguments = ''
        for arg in self.arguments[:-1]:
            shell_arguments += arg.text + ' '
        if len(self.arguments) > 0:
            shell_arguments += self.arguments[-1].text
        outstream = io.StringIO()
        try:
            if shell_arguments == '':
                output = subprocess.check_output([self.command],
                                                 universal_newlines=True)
            else:
                output = subprocess.check_output([self.command,
                                                  shell_arguments],
                                                 universal_newlines=True)
        except subprocess.CalledProcessError:
             return
        else:
            print(output, file=outstream, end='')
        return outstream
