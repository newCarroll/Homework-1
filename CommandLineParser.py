import Command


class CommandLineParser:

    def __init__(self, args):
        if args['grep'] is not None:
            new_command = Command.Grep()
            text = []
            with open(args['<file>'], 'r') as f:
                for line in f:
                    text.append(line)

            output_stream = new_command.grep(args['<pattern>'],
                                             text, args['-i'],
                                             args['-w'], args['-A'])
            result = output_stream.getvalue()
            print(result, end='')
            output_stream.close()
