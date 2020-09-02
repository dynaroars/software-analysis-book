from typing import List
from enum import Enum

class Statement:
    def __init__(self):
        pass

class Program:
    def __init__(self, statements: List[Statement]):
        self.statements = statements
    def __str__(self):
        return "\n".join([str(s) for s in self.statements])


# Expressions


class Expression:
    def __init__(self):
        pass

class Name(Expression):
    def __init__(self, name: str):
        self.name = name
    def __str__(self):
        return self.name

class Operator(Enum):
    ADD = "+"
    SUB = "-"
    AND = "&&"
    OR = "||"
    EQ = "=="
    NEQ = "!="
    LT = "<"
    LTE = "<="
    GT = ">"
    GTE = ">="

class BinaryOp(Expression):
    def __init__(self, left: Expression, op: Operator, right: Expression):
        self.left = left
        self.op = op
        self.right = right
    def __str__(self):
        return "({} {} {})".format(self.left, self.op.value, self.right)

class Constant(Expression):
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return str(self.val)

# Statements

class Assign(Statement):
    def __init__(self, target: Expression, value: Expression):
        self.target = target
        self.value = value
    def __str__(self):
        return "{} = {}".format(self.target, self.value)

class IfThenElse(Statement):
    def __init__(self, test: Expression, body: List[Statement], orelse: List[Statement]):
        self.test = test
        self.body = body
        self.orelse = orelse
    def __str__(self):
        out = "if {} then {}".format(self.test, "; ".join(self.body))
        if self.orelse:
            out += "else {}".format("; ".join(self.orelse))
        return out

class WhileLoop(Statement):
    def __init__(self, test: Expression, body: List[Statement]):
        self.test = test
        self.body = body
    def __str__(self):
        b = [" {};".format(s) for s in self.body].join()
        return "while {} then {}".format(self.test, b)

class Assert(Statement):
    def __init__(self, test: Expression):
        self.test = test
    def __str__(self):
        return "assert {}".format(self.test)
