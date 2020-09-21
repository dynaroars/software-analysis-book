from typing import List
import ast
import operator
import z3

ast_table = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.USub: operator.neg,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.And: z3.And,
    ast.Or: z3.Or,
}

def expr_from_str(s: str):
    e = ast.parse(s, mode='eval')
    assert isinstance(e, ast.Expression), "s must evaluate to an ast.Expression"
    expr = expr_from_ast(e.body)
    expr = z3.simplify(expr)
    return expr

def expr_from_ast(n):
    if type(n) in ast_table:
        return ast_table[type(n)]

    elif isinstance(n, ast.Name):
        return z3.Int(n.id)

    elif isinstance(n, ast.NameConstant):
        return z3.BoolVal(n.value)

    elif isinstance(n, ast.Num):
        return z3.RealVal(n.n)

    elif isinstance(n, ast.BoolOp):
        op = expr_from_ast(n.op)
        vals = [expr_from_ast(v) for v in n.values]
        return op(vals)

    elif isinstance(n, ast.BinOp):
        op = expr_from_ast(n.op)
        left = expr_from_ast(n.left)
        right = expr_from_ast(n.right)
        return op(left, right)

    elif isinstance(n, ast.UnaryOp):
        op = expr_from_ast(n.op)
        val = expr_from_ast(n.operand)
        return op(val)

    elif isinstance(n, ast.Compare):
        assert len(n.ops) == 1 and len(n.comparators) == 1, ast.dump(n)
        op = expr_from_ast(n.ops[0])
        left = expr_from_ast(n.left)
        right = expr_from_ast(n.comparators[0])
        return op(left, right)

    else:
        raise NotImplementedError("unsupported ast expression type: {}".format(n))
