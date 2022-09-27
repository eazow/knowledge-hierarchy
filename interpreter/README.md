### Testing

```
env PYTHONPATH="." pytest
```

```
================================ test session starts =================================
platform darwin -- Python 3.7.3, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: $workspace/knowledge-hierarchy/interpreter
plugins: cov-2.11.1, mock-3.5.1
collected 25 items

tests/test_arithmetic_expressions.py .........                                 [ 36%]
tests/test_interpreter.py s.s...                                               [ 60%]
tests/test_lexer.py ......                                                     [ 84%]
tests/test_procedure.py ...                                                    [ 96%]
tests/test_utils.py .                                                          [100%]

=========================== 23 passed, 2 skipped in 0.08s ============================
```