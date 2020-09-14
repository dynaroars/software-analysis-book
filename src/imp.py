from typing import List
from enum import Enum
import ast

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
    @staticmethod
    def from_ast(e):
        e = e.body if isinstance(e, ast.Expression) else e
        ftable = {
            ast.BoolOp: BoolOp.from_ast,
            ast.Compare: Compare.from_ast,
            ast.BinOp: BinOp.from_ast,
            ast.Name: Name.from_ast,
            ast.Num: Constant.from_ast,
        }
        if not type(e) in ftable:
            raise NotImplementedError("unsupported ast expression type: {}".format(e))
        return ftable[type(e)](e)
    @staticmethod
    def from_str(s):
        e = ast.parse(s, mode='eval')
        assert isinstance(e, ast.Expression), "s must evaluate to an ast.Expression"
        return Expression.from_ast(e.body)

class Name(Expression):
    def __init__(self, name: str):
        self.name = name
    def __str__(self):
        return self.name
    @staticmethod
    def from_ast(e):
        assert isinstance(e, ast.Name), "e must be ast.Name"
        return Name(e.id)

class Operator(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"

class BinOp(Expression):
    ast_op_table = {
        ast.Add: Operator.ADD,
        ast.Sub: Operator.SUB,
        ast.Mult: Operator.MUL,
        ast.Div: Operator.DIV
    }
    def __init__(self, left: Expression, op: Operator, right: Expression):
        self.left = left
        self.op = op
        self.right = right
    def __str__(self):
        return "({} {} {})".format(self.left, self.op.value, self.right)
    @staticmethod
    def from_ast(binop: ast.BinOp):
        if type(binop.op) not in BinOp.ast_op_table:
            raise NotImplementedError("unsupported operator: {}".format(binop.op))
        return BinOp(
            Expression.from_ast(binop.left),
            BinOp.ast_op_table[type(binop.op)],
            Expression.from_ast(binop.right))

class BoolOperator(Enum):
    AND = "and"
    OR = "or"

class BoolOp(Expression):
    def __init__(self, op: BoolOperator, vals: List[Expression]):
        self.op = op
        self.vals = vals
    def __str__(self):
        return " {} ".format(self.op.value).join(map(str, self.vals))
    @staticmethod
    def from_ast(boolop: ast.BoolOp):
        op = BoolOperator.AND if isinstance(boolop.op, ast.And) else BoolOperator.OR
        return BoolOp(op, [Expression.from_ast(e) for e in boolop.values])

class CompareOperator(Enum):
    EQ = "=="
    NEQ = "!="
    LT = "<"
    LTE = "<="
    GT = ">"
    GTE = ">="

class Compare(Expression):
    ast_op_table = {
        ast.Eq: CompareOperator.EQ,
        ast.NotEq: CompareOperator.NEQ,
        ast.Lt: CompareOperator.LT,
        ast.LtE: CompareOperator.LTE,
        ast.Gt: CompareOperator.GT,
        ast.GtE: CompareOperator.GTE
    }
    def __init__(self, left: Expression, ops: List[CompareOperator], cmps: List[Expression]):
        self.left = left
        self.ops = ops
        self.cmps = cmps
    def __str__(self):
        l = str(self.left)
        r = [" {} {}".format(op.value, cm) for op, cm in zip(self.ops, self.cmps)]
        return l + "".join(r)
    @staticmethod
    def from_ast(cmpop: ast.Compare):
        for op in cmpop.ops:
            if type(op) not in Compare.ast_op_table:
                raise NotImplementedError("unsupported operator: {}".format(op))
        return Compare(
            Expression.from_ast(cmpop.left),
            [Compare.ast_op_table[type(op)] for op in cmpop.ops],
            [Expression.from_ast(e) for e in cmpop.comparators])

class Constant(Expression):
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return str(self.val)
    @staticmethod
    def from_ast(num: ast.Num):
        return Constant(num.n)

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
