#!/usr/bin/env python3

import VariablesParser as vp
import Command
import io


class PipeParser:
    """
    класс, который обрабатывает часть пайплайна
    то есть все между "|", вызывая нужные команды
    """
    def __init__(self):
        self.var_parser = vp.VarParser()
        # имена наличествующих команд
        self.__commands = ['wc', 'echo', 'cat', 'pwd', 'exit', 'ls', 'cd', 'grep']

    def parse(self, command, input_stream, arguments=None):
        """
        :param command: список токенов в части пайпа
        :param input_stream: входящий поток
        :return: поток с результатом данного пайпа
        """
        if arguments is None:
            command = self.var_parser.set_values(command)
            command_name = command[0].text
        else:
            command_name = 'grep'
            command = ['empty']

        if command_name in self.__commands:

            if command_name == 'echo':
                new_command = Command.Echo(command[1:], input_stream)
            elif command_name == 'pwd':
                new_command = Command.Pwd(command[1:], input_stream)
            elif command_name == 'exit':
                new_command = Command.Exit(command[1:], input_stream)
            elif command_name == 'wc':
                new_command = Command.Wc(command[1:], input_stream)
            elif command_name == 'ls':
                new_command = Command.Ls(command[1:], input_stream)
            elif command_name == 'cd':
                new_command = Command.Cd(command[1:], input_stream)
            elif command_name == 'grep':
                new_command = Command.Grep(args=command[1:], instreams=input_stream, clarguments=arguments)
            else:
                new_command = Command.Cat(command[1:], input_stream)

            return new_command.execute()

        else:
            if (command[0].text.find('=') > 0
                    and command[0].quot == 'NOT_QUOTING'):

                input_stream.close()
                self.var_parser.parse(command)
                outstream = io.StringIO()
                return outstream
            else:
                command_name = Command.ShellProcess(command, input_stream)
                return command_name.execute()