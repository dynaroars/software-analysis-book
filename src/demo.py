#!/usr/bin/env python3

from parse import expr_from_str as expr
import operator
import z3
from imp import *
from z3 import *
from wp import wp

def main():
    assign = Assign('x', expr('4'))
    post = expr('x == 4')
    a = wp(assign, post)
    print(a)


if __name__ == "__main__":
    main()
