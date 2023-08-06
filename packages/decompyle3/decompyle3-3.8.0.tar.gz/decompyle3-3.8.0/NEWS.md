3.8.0
=====

* Sync version number with corresponding uncompile6 version. The big change in 3.7.7 was using xdis >= 6.x
* use `expr_stmt` instead of `call_stmt` when that is what is meant
* remove float version tests
* better, but not perfect, `list .. if` comprehensions
* PyPy 3.8 testing support
* Start PyPy 3.7 and PyPy 3.8 decompilation support


3.7.7
=====

* Better handling of invalid bytecode magic
* Python 3.8 "try" with a "return" in "finally". Issue #67
* Support running from 3.9 and 3.10 although we do not support those bytecodes

3.7.6
=====

* Fix fragment comprehension bugs
* Makefile tolerance for pyston
* Revise for xdis 6.0.0 - in  Python version comparisions use tuples instead of floats

3.7.5
=====

Fix various bugs in fragment semantic actions. This mostly got stale with disuse, and make usable again now that it is used in trepan3k.


3.7.4
=====

First PyPI release. Version number is set to roughly the corresponding uncompyle6 version.
