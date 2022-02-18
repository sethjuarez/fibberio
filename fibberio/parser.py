from dataclasses import dataclass
from typing import Dict
from parsimonious.grammar import Grammar, NodeVisitor
from parsimonious.nodes import Node

_srcebnf = r"""
source      = signature / expr
signature   = symbol args?
args        = beg_open argv* end_open
expr        = range type_expr?
range       = range_open spot comma spot range_close
range_open  = beg_open / beg_closed
range_close = end_open / end_closed
argv        = symbol equals sarg comma?
sarg        = number / symbol
beg_open    = ws? "(" ws?
end_open    = ws? ")" ws?
beg_closed  = ws? "[" ws?
end_closed  = ws? "]" ws?
comma       = ws? "," ws?
equals      = ws? "=" ws?
type_expr   = ws? "->" ws? type
type        = int / float
int         = "int"
float       = "float" paren?
paren       = beg_open digits end_open
spot        = number / "*"
ws          = ~r"\s*"
symbol      = ~r"[a-z A-Z _][a-z A-Z 0-9 _]*"
digits      = ~r"\d+"
number      = ~r"[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?"
"""


@dataclass
class ParseResult:
    start_open: bool
    end_open: bool
    val_type: str
    precision: int
    start: float
    end: float
    name: str
    argsv: Dict

    def __init__(
        self,
        start_open: bool = False,
        end_open: bool = False,
        precision: int = 0,
        start: float = 0,
        end: float = 0,
        val_type: str = "int",
        name: str = "__range",
        floor: bool = False,
        ceil: bool = False,
        argsv: Dict = {},
    ) -> None:
        self.start_open = start_open
        self.end_open = end_open
        self.precision = precision
        self.start = start
        self.end = end
        self.val_type = val_type
        self.name = name
        self.floor = floor
        self.ceil = ceil
        self.argsv = argsv


class ItemVisitor(NodeVisitor):
    def visit_signature(self, node, visited_children):
        sym, arg = visited_children
        p = ParseResult()
        p.name = sym
        p.argsv = {}
        if type(arg) != Node:
            for k, v in arg[0]:
                p.argsv[k] = v
        return p

    def visit_args(self, node, visited_children):
        _, va, _ = visited_children
        return va

    def visit_argv(self, node, visited_children):
        k, _, v, _ = visited_children
        return k, v

    def visit_marg(self, node, visited_children):
        sy, _, va = visited_children
        return sy, va

    def visit_sarg(self, node, visited_children):
        itm = visited_children[0]
        if type(itm) == str:
            return itm
        else:
            # number
            return itm[0]

    def visit_symbol(self, node, visited_children):
        return node.text.strip()

    def visit_expr(self, node, visited_children):
        rg, tp = visited_children
        p = ParseResult()
        p.start_open = rg[0]
        p.end_open = rg[3]

        # check first spot
        if type(rg[1]) == Node:
            p.floor = True
        else:
            p.start = rg[1][0]
            p.val_type = "float" if rg[1][1] else "int"

        # check second spot
        if type(rg[2]) == Node:
            p.ceil = True
        else:
            p.end = rg[2][0]
            p.val_type = "float" if rg[2][1] else "int"

        # override type (if specified)
        if type(tp) != Node:
            p.val_type = tp[0][0]
            p.precision = tp[0][1]

        return p

    def visit_range(self, node, visited_children):
        op, n1, _, n2, cl = visited_children
        return op, n1, n2, cl

    def visit_range_open(self, node, visited_children):
        return node.text.strip() == "("

    def visit_range_close(self, node, visited_children):
        return node.text.strip() == ")"

    def visit_type_expr(self, node, visited_children):
        _, _, _, t = visited_children
        return t

    def visit_spot(self, node, visited_children):
        return visited_children[0]

    def visit_type(self, node, visited_children):
        return visited_children[0]

    def visit_int(self, node, visited_children):
        return "int", 0

    def visit_float(self, node, visited_children):
        _, p = visited_children
        return "float", p[0]

    def visit_paren(self, node, visited_children):
        _, d, _ = visited_children
        return d

    def visit_digits(self, node, visited_children):
        # inferred type is int
        return int(node.text)

    def visit_number(self, node, visited_childern):
        # inferred type is "float" if "."
        return float(node.text), "." in node.text

    def generic_visit(self, node, visited_children):
        return visited_children or node


class ItemParser:
    def __init__(self):
        self.grammar = Grammar(_srcebnf)

    def parse(self, source: str) -> ParseResult:
        if source.strip() == "*":
            p = ParseResult()
            p.ceil = True
            p.floor = True
            return p
        else:
            g = self.grammar.parse(source)
            sv = ItemVisitor()
            p = sv.visit(g)
            return p[0]
