#!/usr/bin/env python3

from imp import *

def main():
    expression = Expression.from_str('y - 2 >= x + 5 and z * 2 < 10')
    print(expression)


if __name__ == "__main__":
    main()
