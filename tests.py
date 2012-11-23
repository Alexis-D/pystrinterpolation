#!/usr/bin/env python
#-*- coding: utf-8 -*-

import interpolation
import unittest

# the two following constants may seem ugly, but this is the only way to avoid writing literal strings.
EMPTY_STRING = str()
HELLO_WORLD = str().join(chr(c) for c in [104, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100])
HELLO_WORLD_NL = str().join(chr(c) for c in [104, 101, 108, 108, 111, 44, 10, 119, 111, 114, 108, 100])

class StringInterpolaterTest(unittest.TestCase):
    def test_no_format(self):
        self.assertEqual(EMPTY_STRING, '')
        self.assertEqual(HELLO_WORLD, 'hello, world')

    def test_simple_expressions(self):
        self.assertEqual(str(5), '#{2 + 3}')
        self.assertEqual(str(5), '#{ 2 + 3}')
        self.assertEqual(str(5), '#{2 + 3 }')
        self.assertEqual(str(5), '#{ 2 + 3 }')
        self.assertEqual(HELLO_WORLD, '#{ "hello," + " world" }')
        self.assertEqual(str(21), '#{ (lambda a, b: a * b)(3, 7) }')
        self.assertEqual(str(47), '#{ {42: 47}[0x2a] }')

    def test_multiple_expressions(self):
        self.assertEqual(HELLO_WORLD, '#{"hello"}, #{"world"}')
        self.assertEqual(str(37), '#{ 1 + 2 }#{ len("helloww") }')
        self.assertEqual(str(37), '#{sum(1 for x in range(3))}#{ 0b1010 ^ 0b1101 }')

    def test_multiple_lines(self):
        self.assertEqual(HELLO_WORLD_NL, '#{"hello"},\n#{"world"}')
        self.assertEqual(HELLO_WORLD, '#{"hello"\n}, #{"world"}')
        self.assertEqual(HELLO_WORLD, '#{"hello"\n }, #{"world"}')
        self.assertEqual(HELLO_WORLD, '#{ \n "hello" \n }, #{"world"}')

    def test_errors(self):
        with self.assertRaises(NameError):
            '#{ var }'

        with self.assertRaises(AttributeError):
            '#{ "".no_such_method() }'

    def test_recursive_interpolation(self):
        self.assertEqual(HELLO_WORLD, '''#{ "#{ 'hello' }"}, #{ "#{ 'world'}"}''')

    def runTest(self):
        self.test_no_format()
        self.test_simple_expressions()
        self.test_multiple_expressions()
        self.test_multiple_lines()
        self.test_errors()
        self.test_recursive_interpolation()

        # Sadly malformed expression are not tested because it's  a  bit  tricky
        # as a malformed expressions raise  an  error  when  the  AST  is  being
        # visited, so well before these unit tests are ran. I guess it could be
        # testable in some way (better implementation),  but  well  this  really
        # hacky project already comes with a  few  testcases  so  you  shouldn't
        # complain :).

if __name__ == '__main__':
    StringInterpolaterTest().runTest()
