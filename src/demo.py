#!/usr/bin/env python3

import parse

def main():
    s = 'y - 2 >= x + 5 and z * 2 < 10'
    expr = parse.from_str(s)
    print('parsing expression:')
    print(s)
    print('=====')
    print(expr)


if __name__ == "__main__":
    main()
