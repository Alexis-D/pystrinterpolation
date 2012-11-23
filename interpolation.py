#!/usr/bin/env python
#-*- coding: utf-8 -*-

import ast
import parser
import string


class StringInterpolaterError(Exception):
    """Raised if an interpolation string is invalid."""


class StringInterpolater(ast.NodeTransformer):
    """This NodeTransformer adds the interpolation functionnality to Python
    strings.
    """

    def visit_Str(self, node):
        # implementation:
        # if a literal string is not interpolated at all, return itself
        # else, tranform "a #{b} #{c}." to 'a %s %s' % (b, c)

        src = node.s

        new_string  = ''  # will store the new format string
        data = []  # will store the expression included in the string
        index = 0  # current index in the string

        while index < len(src):
            format_index = src.find('#{', index)
            expr_index = format_index + 2

            if format_index == -1:  # no #{ found
                break

            # consume the possible whitespace after #{
            while src[expr_index] in string.whitespace:
                expr_index += 1

            # add the non-interpolated part of the string to the format string
            new_string += src[index:format_index]

            try:
                parser.expr(src[expr_index:])

                # here we _want_ an exception to be raised, otherwise:
                # it means that the interpolated string has a syntax error like
                # this: "#{2 + 3"
                self._raise(node, 'Unclosed for #{}')

            except SyntaxError as e:
                # the expresion may span on multiple lines, so we're fiddling a
                # bit with indices in order to find the matching }
                end_format_index = expr_index

                while e.lineno > 1:
                    nl = src.find('\n', end_format_index)
                    end_format_index = nl + 1
                    e.lineno -= 1

                end_format_index += e.offset - 1  # -1 because offset starts at 1

                # we may have some whitespace after the expression
                while src[end_format_index] in string.whitespace:
                    end_format_index += 1

                if src[end_format_index] != '}':
                    self._raise(node, 'Malformed format expression.')

                new_string += '%s'  # to put the interpolated value
                expr = src[expr_index:end_format_index]

                if not expr:
                    self._raise(node, 'Empty expression is not allowed.')

                data.append(ast.parse(expr).body[0].value)  # parse & store the expression
                index = end_format_index + 1  # advance our position in the string

        new_string += src[index:]  # the end of the format string

        if not data:  # no interpolation
            return node

        # magic
        return ast.BinOp(
            ast.Str(''.join(new_string)),
            ast.Mod(),
            ast.Tuple(data, ast.Load())
            )

    def _raise(self, node, error):
        raise StringInterpolaterError('Encountered invalid interpolation '
                'string at line %s, column %s.\n%s' %
                (node.lineno, node.col_offset + 1, error)) from None


def interpolate_strings(src):
    """Add interpolations to string contained in src.

    Args:
        src: the source to update.

    Returns:
        An ast.Module ready to be compiled.
    """
    tree = StringInterpolater().visit(ast.parse(src))
    ast.fix_missing_locations(tree)
    return tree


def run(filename):
    """Run filename adding string interpolation ability to literal strings.

    Args:
        filename: the name of the file to run.
    """
    with open(filename) as f:
        tree = interpolate_strings(f.read())
        compiled = compile(tree, filename, 'exec')
        exec(compiled, {'__name__': '__main__', '__file__': filename})


if __name__ == '__main__':
    run('tests.py')
