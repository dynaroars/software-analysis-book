#!/usr/bin/env python3

from imp import *

def main():

    program = Program([
        Assign(Name("x"), BinaryOp(Name("x"), Operator.ADD, Constant(10))),
    ])
    print(program)


if __name__ == "__main__":
    main()
