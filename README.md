# Interpolation string for Python!

## What?

It allows use to use Ruby style interpolation string in Python so `print(" #{3 + 4} ")` will print ` 7 ` (yes exactly like in Ruby).

It even comes with testcases (though read the comment in `tests.py`). To run them `python interpolation.py` (if it prints nothing => success, otherwise => failure).

## Limitations

### Known ones

If you do `'#{3} %s' % 3` it will fail :) Because internally this module use `%s` to format strings. It could be easily fixed by changing the implementation from:

    new_format_string % interpolations_expressions

to

    ''.join(str(x) for x in (strings bits & interpolations_expressions)  # or using concatenation with +

so `%s` wouldn't be used internally. I didn't do it because it's funky to use interpolation and `%` operator at the same time (let's say it's left as an easy exercise to the reader).

### Wanted ones

You can only put one expression per `#{}` and no statement because it's more 'Pythonic' (cf. lambdas).

## Improvements?

Well plenty of them are possible, the first one that comes to mind is do make this work on several files (i.e. interpolate strings that are in imports as well). I guess it's not really hard, but it's just a toy project, nothing serious, so whatever.

## Why?

To play with the ast module.
