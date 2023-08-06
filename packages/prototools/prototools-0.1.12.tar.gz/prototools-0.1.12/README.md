# `prototools`

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](./code_of_conduct.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

                       __       __            __  
        ___  _______  / /____  / /____  ___  / /__
       / _ \/ __/ _ \/ __/ _ \/ __/ _ \/ _ \/ (_-<
      / .__/_/  \___/\__/\___/\__/\___/\___/_/___/
     /_/ 


`prototools` is a set of tools that considerably reduce the amount of time 
spent writing console applications. 

# Installation

`prototools` is available on [PyPi](https://pypi.org/) (MIT license) 
and installation can be performed by running [pip](https://docs.python.org/es/3/installing/index.html)

```
python -m pip install prototools
```
To upgrade the package:
```
python -m pip install prototools --upgrade
```
> 📝 It's recommended to use virtual environment.

To delete the package:
```
python -m pip uninstall prototools
```

# Example

```python 
from prototools import Menu, float_input


def _user_input(f):
    x = float_input("First number: ")
    y = float_input("Second number: ")
    print(f"Result: {f(x, y)}")


def addition(x, y):
    return x + y


def substraction(x, y):
    return x - y


def multiplication(x, y):
    return x * y


def division(x, y):
    try:
        return x / y
    except ZeroDivisionError:
        return "Can't divide by zero"


def about():
    print("Just Another Simple Calculator")


def main():
    menu = Menu()
    menu.add_options(
        ("Addition", lambda: _user_input(addition)),
        ("Substraction", lambda: _user_input(substraction)),
        ("Multiplication", lambda: _user_input(multiplication)),
        ("Division", lambda: _user_input(division)),
        ("About", about),
    )
    menu.run()


if __name__ == "__main__":
    main()
```

    ┌─────────────────────────────────────────────────────────┐
    │                                                         │
    │                          Menu                           │
    │                                                         │
    │                                                         │
    │  1 - Addition                                           │
    │  2 - Substraction                                       │
    │  3 - Multiplication                                     │
    │  4 - Division                                           │
    │  5 - About                                              │
    │  6 - Exit                                               │
    │                                                         │
    │                                                         │
    └─────────────────────────────────────────────────────────┘
    >


# Documentation

You can read the documentation at [aquí](https://proto-tools.github.io/docs/)


# Contribution

You can contribute with ``prototools`` in so many ways (not just coding).
Every idea is welcome! You can suggest new features or report a bug when
you find it. Every contribution that you made it'll be mention in this 
project. 