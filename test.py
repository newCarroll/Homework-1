#!/usr/bin/env python3

import Interpreter as itr
import unittest


class TestMethods(unittest.TestCase):

    def test_wc(self):
        interpreter = itr.Interpreter()
        interpreter.set_text('echo 123')
        result = interpreter.parse_pipe()
        self.assertEqual('123 \n', result)

        interpreter = itr.Interpreter()
        interpreter.set_text('echo "Hello"')
        result = interpreter.parse_pipe()
        self.assertEqual('Hello \n', result)

    def test_var(self):
        interpreter = itr.Interpreter()
        interpreter.set_text('i=4')
        interpreter.parse_pipe()
        interpreter.set_text('echo $i')
        result = interpreter.parse_pipe()
        self.assertEqual('4 \n', result)
        interpreter.set_text('echo "$i"')
        result = interpreter.parse_pipe()
        self.assertEqual('4 \n', result)
        interpreter.set_text('echo \'$i\'')
        result = interpreter.parse_pipe()
        self.assertEqual('$i \n', result)

        interpreter.set_text('echo $j')
        result = interpreter.parse_pipe()
        self.assertEqual(' \n', result)

    def test_pipe(self):
        interpreter = itr.Interpreter()
        interpreter.set_text('echo 123 | wc | wc')
        result = interpreter.parse_pipe()
        self.assertEqual('  1   3   9\n', result)

    def test_grep(self):
        interpreter = itr.Interpreter()
        interpreter.set_text('echo hello | grep h')
        result = interpreter.parse_pipe()
        self.assertEqual('hello \n', result)
        interpreter.set_text('echo hello | grep H')
        result = interpreter.parse_pipe()
        self.assertEqual('', result)
        interpreter.set_text('echo hello | grep -w h')
        result = interpreter.parse_pipe()
        self.assertEqual('', result)
        interpreter.set_text('echo hello h | grep -w h')
        result = interpreter.parse_pipe()
        self.assertEqual('hello h \n', result)
        interpreter.set_text('echo hello | grep -i h')
        result = interpreter.parse_pipe()
        self.assertEqual('hello \n', result)
        interpreter.set_text('echo hello | grep -i H')
        result = interpreter.parse_pipe()
        self.assertEqual('hello \n', result)

        f = open('test_file.txt', 'w+')
        f.write('ts\nq\nw\ne\ntsst\na\ns\nd\nts\n1\n2\n3')
        f.close()
        interpreter.set_text('echo hello | grep -A 2 ts test_file.txt')
        result = interpreter.parse_pipe()
        self.assertEqual('ts\nq\nw\ntsst\na\ns\nts\n1\n2\n', result)
        interpreter.set_text('grep ts test_file.txt')
        result = interpreter.parse_pipe()
        self.assertEqual('ts\ntsst\nts\n', result)
        interpreter.set_text('grep -i -w Ts test_file.txt')
        result = interpreter.parse_pipe()
        self.assertEqual('ts\nts\n', result)

        interpreter.set_text('echo abcdfghijk | grep a[b-f]*f')
        result = interpreter.parse_pipe()
        self.assertEqual('abcdfghijk \n', result)




if __name__ == '__main__':
    unittest.main()
