# NanamiLang - Chiaki Nanami Language

## Notice

Current implementation language - Python 3.  
In the future, there will be C++ implementation.

## Key points

2. The project main goal is to create a LISP language dialect with immutable data structures.
3. The project name was inspired by the character Chiaki Nanami from the game named Danganronpa v2.

## Data Types

1. **IMPORTANT**: all data types are **immutable**

### Base

1. **Undefined**
   1. Python - `reference() `returns `None`
   2. C++ - `reference()` returns `NULL`
2. **Macro**
   1. Python - `reference()` returns function object
   2. C++ - `reference()` returns function pointer
3. **Function**
   1. Python - `reference()` returns function object
   2. C++ - `reference()` returns function pointer
4. **Nil**
   1. Python - `reference()` returns `None`
   2. C++ - `reference()` returns `NULL`
5. **Boolean**
   1. Python - `reference()` returns `bool`
   2. C++ - `reference()` returns `bool`
6. **String**
   1. Python - `reference()` returns `str`
   2. C++ - `reference()` returns `std::string`
7. **Date**
   1. Python - `reference()` returns `datetime.datetime`
   2. C++ - `reference()` returns ...
8. **FloatNumber**
   1. Python - `reference()` returns `float`
   2. C++ - `reference()` returns `float`
9. **IntegerNumber**
   1. Python - `reference()` returns `int`
   2. C++ - `reference()` returns `int`
10. **Keyword**
    1. Python - `reference()` returns `str`
    2. C++ - `reference()` returns `std::string`

### Complex

1. **Set**
   1. Python - `reference()` returns `set`
   2. C++ - `reference()` returns `std::set`
2. **Vector**
   1. Python - `reference()` returns `list`
   2. C++ - `reference()` returns `std::vector`
3. **HashMap**
   1. Python - `reference()` returns `dict`
   2. C++ - `reference()` returns `std::unordered_map`

## Goals

1. Implement standard library similar to Clojure (maybe using `toolz` project)
2. Port the project to C++ language once API gets stabilized (and make it possible to compile built AST using `llvm`)
3. Being compatible with the most Clojure programs written without Java built-in classes or external libraries in use.

## Collaborators

1. @jedi2light - (aka. Stoian Minaiev) - Creator & Maintainer of the project.
2. @buzzer13 - the project contains `AST.mktree()` method that was initially written by that person.

## Documentation

Each package, module, class or function has its own docstring.  
Also, lang-level (types, functions, macro) documentation available [here](https://nanamilang.readthedocs.io/en/latest/).

## Usage

0. Ensure that you have `GNU Make` installed on your system, then go to the project root and run `make install`.
   1. Alternatively, you can install `nanamilang` from PyPi repository, just run `pip3 install nanamilang` command.
1. Check whether your `~/.local/bin` and `~/.local/lib` directories are present in your `$PATH` environment variable.
2. `nanamilang-eval.py` reads the file (if it exists), evaluates it and returns corresponding value to system at exit.
3. `nanamilang-repl.py` will allow you to type expressions and evaluate them in real mode. But for now, REPL has limits.

## Examples

```python3
from nanamilang import datatypes, program

source = '(+ 2 2 (* 2 2))'
program: program.Program = program.Program(str(source))
program.format() # => "(+ 2 2 (* 2 2))"
program.ast() # => get encapsulated AST instance
program.tokenized() # => collection of a Token instances

result: datatypes.Base = program.evaluate() # => <IntegerNumber>: 8
```

## License and credits

**NanamiLang is licensed under GNU GPL version 2, was initially made by @jedi2light (aka Stoian Minaiev), October 2021**