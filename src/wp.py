from z3.z3 import ExprRef, BoolRef, ArithRef
from imp import *
from parse import expr_from_str as expr

def wp(stmt: Statement, post: ExprRef) -> ExprRef:
    if isinstance(stmt, Assign):
        # get the target from the assignment statement

        # solve for the target in the postcondition

        # "target = value"; "target {op} expr" -> "value {op} expr"
        if isinstance(post, BoolRef):
            pass
        elif isinstance(post, ArithRef):
            pass
        pass
    else:
        raise NotImplementedError("unsupported statement type: {}".format(type(stmt)))

    return expr('False')
