from typing import List
from enum import Enum
import parse
import z3
from z3.z3 import ExprRef, BoolRef, ArithRef
from parse import expr_from_str as expr

class Statement:
    def __init__(self):
        pass

class Program:
    def __init__(self, statements: List[Statement]):
        self.statements = statements
    def __str__(self):
        return "\n".join([str(s) for s in self.statements])

# Statements

class Assign(Statement):
    def __init__(self, identifier: str, value: ExprRef):
        if isinstance(value, z3.BoolRef):
            self.target = z3.Bool(identifier)
        elif isinstance(value, z3.ArithRef):
            self.target = z3.ToReal(z3.Int(identifier))
        self.value = value
    def __str__(self):
        return "{} = {}".format(self.target, self.value)
   
class IfThenElse(Statement):
    def __init__(self, test: ExprRef, body: List[Statement], orelse: List[Statement]):
        self.test = test
        self.body = body
        self.orelse = orelse
    def __str__(self):
        out = "if {} then {}".format(self.test, "; ".join(self.body))
        if self.orelse:
            out += "else {}".format("; ".join(self.orelse))
        return out

class WhileLoop(Statement):
    def __init__(self, test: ExprRef, body: List[Statement]):
        self.test = test
        self.body = body
    def __str__(self):
        b = [" {};".format(s) for s in self.body].join()
        return "while {} then {}".format(self.test, b)
